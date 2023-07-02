from download_from_excel import get_data_from_excel
from connect import (
    get_vacancies, insert_candidates, get_candidates, insert_candidates_to_vacancy, get_statuses,
)

# Запуск всех функций
if __name__ == "__main__":
    # Получение токена для дальнейшей авторизации
    token = input("Введите токен для обрашения к API: ")
    file_path = input("Введите путь к таблице с кандидатами: ")

    vacancies = get_vacancies(token)  # Получение вакансий
    candidates_data = get_data_from_excel("Тестовая база.xlsx", token)  # Получение кандидатов из Excel
    len_candidates = insert_candidates(candidates_data, token)  # Добавление кандидатов в базу
    candidates = get_candidates(token=token, download_candidates=candidates_data,
                                count_candidate=len_candidates)  # Получение 4-х последних кандидтов, которых мы добавили
    statuses = get_statuses(token)  # Получение статусов кандидатов
    insert_candidates_to_vacancy(candidates, vacancies, token, statuses, "Тестовая база.xlsx")  # Добавлние кандидата на вакансию

