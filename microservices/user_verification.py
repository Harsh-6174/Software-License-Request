from database.db_connection import get_connection

def user_exists(employee_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM employees WHERE LOWER(id) = LOWER(%s)", (employee_id,))

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count > 0