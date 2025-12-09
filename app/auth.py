USERS = {
    "WE3729": {"password": "123", "role": "employee"},
    "WE2001": {"password": "123", "role": "manager"},
    "WE3001": {"password": "123", "role": "L1"},
    "WE3002": {"password": "123", "role": "L2"},
    "WE3003": {"password": "123", "role": "L3"},
}

def login():
    print("\n=== Login ===")
    emp_id = input("Employee ID: ").strip().upper()
    pwd = input("Password: ").strip()

    user = USERS.get(emp_id)

    if not user or user["password"] != pwd:
        print("Invalid credentials. Try again.")
        return login()

    print(f"Logged in as {emp_id} ({user['role']})")
    return {"employee_id": emp_id, "role": user["role"]}