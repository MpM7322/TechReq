import json
import csv
import xml.etree.ElementTree as ET
import yaml
import sqlite3
from techreq.database.techreq_db import get_connection
import os # для создания папки

def get_data_from_database(table_name: str) -> list:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Узнаём все связи, т. е внешние ключи, этой таблицы
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    foreign_keys = cursor.fetchall()

    # Получаем все строки из выбранной таблицы
    cursor.execute(f"SELECT * FROM {table_name}")
    table_rows = cursor.fetchall()

    result = []

    for row in table_rows:
        item = dict(row)

        for foreign_key in foreign_keys:
            column_name = foreign_key["from"] # Колонка в изначальной таблице, обращение по ключу "from"
            other_table = foreign_key["table"] # Связанная таблица, обращение по ключу "table"
            other_column = foreign_key["to"] # Колонка в связанной таблице, обращение по ключу "to"

            related_id = item.pop(column_name) # Получаем ID связанной записи из другой таблицы

            if column_name.endswith("_id"): # Создание красивого ключа
                new_key = column_name[:-3]
            else:
                new_key = other_table

            if related_id is not None: # Ищем связанную запись, если ID не пустой
                cursor.execute(f"SELECT * FROM {other_table} WHERE {other_column} = ?", (related_id,))
                related_row = cursor.fetchone()

                if related_row is not None:
                    item[new_key] = dict(related_row)
                else:
                    item[new_key] = None

            else:
                item[new_key] = None

        result.append(item)

    conn.close()
    return result


def save_to_json(data: list, out_dir: str = "out"):
    os.makedirs(out_dir, exist_ok = True) # Создаём папку out, если она есть, то код не выдаст ошибку

    file_path = os.path.join(out_dir, "data.json") # .join склеивает название папки и имя файла

    with open(file_path, "w", encoding = "utf-8") as file: # "w" - режим чтения, сотрёт данные, если есть, создаст файл, если нет
        json.dump(data, file, ensure_ascii = False, indent = 4) # ensure_ascii = False отключает перевод неанглийских слов в специальные коды ; indent = 4 - форматирование с отступом 4 пробела



def save_to_yaml(data: list, out_dir: str = "out"):
    os.makedirs(out_dir, exist_ok = True) # Создаём папку out, если она есть, то код не выдаст ошибку

    file_path = os.path.join(out_dir, "data.yaml") # .join склеивает название папки и имя файла

    with open(file_path, "w", encoding = "utf-8") as file: # "w" - режим чтения, сотрёт данные, если есть, создаст файл, если нет
        yaml.safe_dump(data, file, allow_unicode = True, sort_keys = False) # allow_unicode = True даёт записывать кирилиццу ; sort_keys = False - запрещает сортировать поля по алфавиту



def build_xml_tags(parent_tag, data_dict):
    for key, value in data_dict.items():
        child_tag = ET.SubElement(parent_tag, str(key)) # создание дочернего тэга, 1 параметр - вложение тэга, 2 параметр - имя тэга

        if isinstance(value, dict): # проверка на дальнейшую вложенность
            build_xml_tags(child_tag, value)
        else:
            if value is None:
                child_tag.text = ""
            else:
                child_tag.text = str(value)

def save_to_xml(data: list, out_dir: str = "out"):
    os.makedirs(out_dir, exist_ok = True) # Создаём папку out, если она есть, то код не выдаст ошибку

    file_path = os.path.join(out_dir, "data.xml") # .join склеивает название папки и имя файла

    root = ET.Element("records")

    for record in data:
        record_tag = ET.SubElement(root, "record")
        build_xml_tags(record_tag, record)

    tree = ET.ElementTree(root) # Упаковываем всё в объект дерева, расставляет отступы

    ET.indent(tree, space = "    ") # Отступ в 4 пробела
    tree.write(file_path, encoding = "utf-8", xml_declaration = True) # xml_declaration = True - добавляет специальный технический заголовок XML



def to_csv_row(record: dict) -> dict:
    row = {}

    for key, value in record.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                new_column_name = f"{key}_{sub_key}" # Склеиваем имена ключей
                row[new_column_name] = sub_value
        else:
            row[key] = value # Невложенные поля оставляем так, как есть

    return row

def save_to_csv(data: list, out_dir: str = "out"):
    os.makedirs(out_dir, exist_ok = True) # Создаём папку out, если она есть, то код не выдаст ошибку

    file_path = os.path.join(out_dir, "data.csv") # .join склеивает название папки и имя файла

    csv_rows = []
    for record in data:
        csv_rows.append(to_csv_row(record)) # Превращаем каждую запись в плоскую строку

    headers = []
    for row in csv_rows:
        for key in row.keys():
            if key not in headers:
                headers.append(key)

    with open(file_path, "w", encoding = "utf-8-sig", newline = "") as file: # "utf-8-sig" - добавляет в начало файла невидимую метку BOM, которая говорит, что файл запсиан в utf-8
        writer = csv.DictWriter(file, fieldnames = headers, delimiter = ";") # Записыватель, который раскладывает словари по колонкам
        writer.writeheader() # Записывает в файл первую строчку таблицы с названиями из headers
        writer.writerows(csv_rows) # Выставляет значения под нужный заголовок



def export_all_formats(table_name: str, out_dir: str = "out"):
    data = get_data_from_database(table_name)
    save_to_json(data, out_dir)
    save_to_yaml(data, out_dir)
    save_to_xml(data, out_dir)
    save_to_csv(data, out_dir)

if __name__ == "__main__":
    export_all_formats("tickets")
    print("Готово! Все 4 файла созданы в папке out/")

