from fastapi import FastAPI
from database.db_connection import get_connection

app = FastAPI()

@app.get("/check-user")
def check_user(employee_id : str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM employees WHERE LOWER(id) = LOWER(%s)", (employee_id,))

    count = cur.fetchone()["count"]

    cur.close()
    conn.close()

    return {
        "exists" : count > 0
    }