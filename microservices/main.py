from fastapi import FastAPI
from database.db_connection import get_connection

app = FastAPI()

@app.get("/check-user")
async def check_user(employee_id: str):
    conn = await get_connection()
    try:
        count = await conn.fetchval(
            """
            SELECT COUNT(*)
            FROM employees
            WHERE LOWER(id) = LOWER($1)
            """,
            employee_id
        )
    finally:
        await conn.close()

    return {
        "exists": count > 0
    }