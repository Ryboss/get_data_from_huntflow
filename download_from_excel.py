# API_TOKEN fb2e5a5705b244f3d5719cdb7fb2700e0ef0620888ea6e2f72100d5ca55e7885
# Забираем данные из Excel !
# Забираем данныые из файлов
# Выгрузка по вакансии
# Закидываем в Апи !
# Возобновление загрузки

import openpyxl


def get_data_from_excel(file_path: str):
    """
    Получение данных из Excel
    """

    # Открываем Excel файл
    workbook = openpyxl.load_workbook(file_path)

    # Получаем активный лист
    sheet = workbook.active

    # Создаем словарь для хранения данных по каждому пользователю
    data = {}
    candidate_list = []
    # Проходимся по каждой строке в листе
    for row in sheet.iter_rows(min_row=2):  # Начинаем со 2-й строки, чтобы пропустить заголовки
        # Заполняем поля по каждому кандидату
        data["full_name"] = " ".join(row[1].value.split())
        data["position"] = row[0].value
        data["money"] = row[2].value
        data["comments"] = row[3].value
        data["status"] = row[4].value
        candidate_list.append(data)
        data = {}

    # Закрываем файл
    workbook.close()


    # Выводим информацию по каждому пользователю
    return candidate_list