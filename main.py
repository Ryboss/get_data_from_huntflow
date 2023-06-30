from download_from_excel import get_data_from_excel
from connect import (
    get_vacancies, insert_candidates, get_candidates, insert_candidates_to_vacancy, get_statuses,
)

# https://dev-100-api.huntflow.dev/v2/accounts/17/applicants/97/vacancy"
# Запуск всех функций
if __name__ == "__main__":
    # token = input("Введите токен для обрашения к API")
    token = "fb2e5a5705b244f3d5719cdb7fb2700e0ef0620888ea6e2f72100d5ca55e7885"
    vacancies = get_vacancies(token)  # Получение вакансий
    candidates_data = get_data_from_excel("Тестовая база.xlsx")  # Получение кандидатов из Excel
    len_candidates = insert_candidates(candidates_data, token)  # Добавление кандидатов в базу
    candidates = get_candidates(token=token, download_candidates=candidates_data, count_candidate=len_candidates)  # Получение 4-х последних кандидтов, которых мы добавили
    statuses = get_statuses(token)
    insert_candidates_to_vacancy(candidates, vacancies, token, statuses)

