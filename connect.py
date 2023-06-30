import requests


def get_candidates(token: str, download_candidates: list, count_candidate: int) -> list:
    """
    Получение кандидатов
    """

    candidates = requests.get(
        f"https://dev-100-api.huntflow.dev/v2/accounts/17/applicants?count={count_candidate}",
        headers={"Authorization": f"Bearer {token}"})
    result = []

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
    return request.json().get("items")


def insert_candidates(candidates: dict, token: str) -> int:
    """
    Добавление кандидата
    """


    for item in candidates:
        # file_path = input(f"Введите путь к резюме {item.get('full_name')}")
        request = requests.post(
            "https://dev-100-api.huntflow.dev/v2/accounts/17/applicants",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": f"{item.get('full_name').split()[0]}",
                "last_name": f"{item.get('full_name').split()[1]}",
                "middle_name": f"{item.get('full_name').split()[2] if len(item.get('full_name').split()) > 2 else ''}",
                "money": item.get('money', None),
                "phone": item.get('phone', None),
                "email": item.get('email', None),
                "skype": item.get('skype', None),
                "position": item.get('position', None),
                "company": item.get('company', None),
                "photo": item.get('photo', None),
                "birthday": item.get('birthday', None),
                "externals": [
                    {
                      "auth_type": "NATIVE",
                      "account_source": 5,
                      "data": {
                        "body": "Resume text"
                      },
                      "files": [
                        1,
                        2,
                        3
                      ]
                    }
                  ],
                "social": item.get("social", [])
                }
        )

    return len(candidates)


def get_statuses(token: str) -> dict:
    """
    Получение стаутусов
    """

    result = {}
    request = requests.get(
        "https://dev-100-api.huntflow.dev/v2/accounts/17/vacancies/statuses",
        headers={"Authorization": f"Bearer {token}"})

    for item in request.json().get("items"):
        result[item.get("name")] = item.get("id")
    print(result)
    return result


def insert_candidates_to_vacancy(candidates: dict, vacancies: list, token: str, statuses: dict):
    """
    Добавление кандидатов на вакансии
    """

    for candidate in candidates:
        for item in vacancies:

            if candidate.get("position") == item.get("position"):
                print(candidate)
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
                print("***", request.status_code)
                print(request.json())