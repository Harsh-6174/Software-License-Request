import psycopg2, os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"),
        cursor_factory=RealDictCursor
    )


def save_pending_manager_request(employee_id, software, thread_id, status = "pending_manager"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO software_requests 
        (employee_id, software, status, thread_id)
        VALUES (%s, %s, %s, %s)
    """, (employee_id, software, status, thread_id))

    conn.commit()
    conn.close()

def get_manager_pending_requests():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT employee_id, software, thread_id, status
        FROM software_requests WHERE status = 'pending_manager'
        ORDER BY created_at ASC
    """)

    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_employee_requests(employee_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT software, status, created_at, updated_at
        FROM software_requests WHERE employee_id = %s
        ORDER BY created_at ASC
    """, (employee_id,))

    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result