import requests

BASE_URL = "http://127.0.0.1:8000"

payload1 = {
    "patient_id": "P001",
    "age": 60,
    "gender": "male",
    "scr": 150,
    "egfr": 50,
    "acr": 120,
    "sbp": 150,
    "dbp": 95,
    "history": ["hypertension", "diabetes"]
}

payload2 = {
    "patient_id": "P001",
    "age": 60,
    "gender": "male",
    "scr": 170,
    "egfr": 40,
    "acr": 220,
    "sbp": 155,
    "dbp": 98,
    "history": ["hypertension", "diabetes"]
}


def print_response(title, response):
    print(f"\n===== {title} =====")
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response Text:", response.text)


def main():
    r1 = requests.post(f"{BASE_URL}/analyze", json=payload1)
    print_response("第一次分析", r1)

    r2 = requests.post(f"{BASE_URL}/analyze", json=payload2)
    print_response("第二次分析", r2)

    r3 = requests.get(f"{BASE_URL}/history/P001")
    print_response("查询历史记录", r3)

    r4 = requests.get(f"{BASE_URL}/history/P001/trend")
    print_response("查询趋势分析", r4)


if __name__ == "__main__":
    main()