import os, asyncpg
from dotenv import load_dotenv

load_dotenv()

async def get_connection():
    return await asyncpg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"),
    )

async def save_pending_request(
    employee_id,
    software,
    thread_id,
    status="pending_manager"
):
    conn = await get_connection()
    try:
        await conn.execute(
            """
            INSERT INTO software_requests
            (employee_id, software, status, thread_id)
            VALUES ($1, $2, $3, $4)
            """,
            employee_id,
            software,
            status,
            thread_id
        )
    finally:
        await conn.close()

async def get_pending_requests(role):
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT employee_id, software, thread_id, status
            FROM software_requests
            WHERE status = $1
            ORDER BY created_at ASC
            """,
            f"pending_{role}"
        )
        return [dict(row) for row in rows]
    finally:
        await conn.close()

async def get_employee_requests(employee_id):
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT software, status, created_at, updated_at
            FROM software_requests
            WHERE employee_id = $1
            ORDER BY created_at ASC
            """,
            employee_id
        )
        return [dict(row) for row in rows]
    finally:
        await conn.close()

async def update_request_status(
    thread_id,
    new_status,
    rejected_by=None,
    rejection_reason=None
):
    conn = await get_connection()
    try:
        result = await conn.execute(
            """
            UPDATE software_requests
            SET status = $1,
                rejected_by = $2,
                rejection_reason = $3,
                updated_at = NOW()
            WHERE thread_id = $4
            """,
            new_status,
            rejected_by,
            rejection_reason,
            thread_id
        )

        if result.endswith("0"):
            print(f"No record found for thread_id: {thread_id}")
    finally:
        await conn.close()