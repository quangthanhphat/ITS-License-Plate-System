from Database.db import get_connection, close_connection


def add_violation(
    vehicle_id,
    violation_type,
    image_path
):
    """
    Thêm vi phạm mới
    """

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor()

    query = """
    INSERT INTO violations
    (vehicle_id, violation_type, image_path)
    VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(
            query,
            (
                vehicle_id,
                violation_type,
                image_path
            )
        )

        conn.commit()

        return True

    except Exception as e:
        print(f"Lỗi thêm vi phạm: {e}")
        return False

    finally:
        cursor.close()
        close_connection(conn)


def get_all_violations():
    """
    Lấy toàn bộ vi phạm
    """

    conn = get_connection()

    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM violations
    ORDER BY violation_time DESC
    """

    cursor.execute(query)

    violations = cursor.fetchall()

    cursor.close()
    close_connection(conn)

    return violations


def get_violations_by_vehicle(vehicle_id):
    """
    Lấy danh sách vi phạm của một xe
    """

    conn = get_connection()

    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM violations
    WHERE vehicle_id = %s
    ORDER BY violation_time DESC
    """

    cursor.execute(query, (vehicle_id,))

    violations = cursor.fetchall()

    cursor.close()
    close_connection(conn)

    return violations