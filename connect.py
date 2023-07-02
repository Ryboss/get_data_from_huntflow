import requests
from download_from_excel import delete_rows_in_excel


def get_candidates(token: str, download_candidates: list, count_candidate: int) -> list:
    """
    Получение кандидатов
    """

    candidates = requests.get(
        f"https://dev-100-api.huntflow.dev/v2/accounts/17/applicants?count={count_candidate}",
        headers={"Authorization": f"Bearer {token}"})
    result = []

    if candidates.status_code != 200:
        raise Exception("Кандидаты не получены")

    for i in download_candidates:
        for item in candidates.json().get("items"):
            full_name = f"{item.get('first_name')} {item.get('last_name')}"
            if item.get('middle_name', '') is not None:
                full_name += f" {item.get('middle_name', '')}"

            if full_name == i.get("full_name"):
                item["comment"] = i.get("comments")
                item["status"] = i.get("status")
                result.append(item)

    return result


def get_vacancies(token: str) -> dict:
    """
    Получение вакансий
    """

    request = requests.get("https://dev-100-api.huntflow.dev/v2/accounts/17/vacancies?count=30&page=1&mine=false&opened=false",
                           headers={"Authorization": f"Bearer {token}"})
    if request.status_code != 200:
        raise Exception("Вакансии не получены")
    return request.json().get("items")


def insert_candidates(candidates: list, token: str) -> int:
    """
    Добавление кандидата
    """

    for item in candidates:
        request = requests.post(
            "https://dev-100-api.huntflow.dev/v2/accounts/17/applicants",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": f"{item.get('full_name').split()[0]}",
                "last_name": f"{item.get('full_name').split()[1]}",
                "middle_name": f"{item.get('full_name').split()[2] if len(item.get('full_name').split()) > 2 else ''}",
                "money": item.get('money', None),
                "phone": item.get('phones', None)[0],
                "email": item.get('email', None),
                "skype": item.get('skype', None),
                "position": item.get('position', None),
                "company": item.get('company', None),
                "photo": item.get('photo', None),
                "birthday": item.get('birthdate', None),
                "externals": [
                    {
                        "auth_type": "NATIVE",
                        "data": {
                            "body": item.get('text', None)
                        },
                        "files": item.get('files', None)
                    }],
                "social": item.get("social", [])
                }
        )
        if request.status_code != 200:
            raise Exception("Кандидаты не созданы")

    return len(candidates)


def get_statuses(token: str) -> dict:
    """
    Получение стаутусов
    """

    result = {}
    request = requests.get(
        "https://dev-100-api.huntflow.dev/v2/accounts/17/vacancies/statuses",
        headers={"Authorization": f"Bearer {token}"})

    if request.status_code != 200:
        raise Exception("Статусы не получены")

    for item in request.json().get("items"):
        result[item.get("name")] = item.get("id")

    return result


def insert_candidates_to_vacancy(candidates: list, vacancies: dict, token: str, statuses: dict, file_path: str):
    """
    Добавление кандидатов на вакансии
    """

    for candidate in candidates:
        for item in vacancies:

            if candidate.get("position") == item.get("position"):
                params = {
                    "vacancy": item.get("id"),
                    "status": statuses.get(candidate.get("status")),
                    "comment": candidate.get("comment"),
                    "files": [],
                    "sms": {
                        "phone": candidate.get("phone", "") if candidate.get("phone", "") is not None else "",
                        "body": candidate.get("body", "")
                      }
                }
                if params.get("status") == 108:
                    params["fill_quota"] = item.get("id")

                request = requests.post(
                    f"https://dev-100-api.huntflow.dev/v2/accounts/17/applicants/{candidate.get('id')}/vacancy",
                    headers={"Authorization": f"Bearer {token}"},
                    json=params)

                if request.status_code != 200:
                    raise Exception("Кандидаты не занесены на вакансии")

                print(request.json())
                delete_rows_in_excel(file_path)