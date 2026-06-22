from Database.db import get_connection, close_connection


def add_violation(vehicle_id, violation_type, image_path):
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
    conn = get_connection()

    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM violations
    ORDER BY violation_time DESC
    """

    try:
        cursor.execute(query)
        return cursor.fetchall()

    except Exception as e:
        print(f"Lỗi lấy vi phạm: {e}")
        return []

    finally:
        cursor.close()
        close_connection(conn)


def get_violations_by_vehicle(vehicle_id):
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

    try:
        cursor.execute(
            query,
            (vehicle_id,)
        )

        return cursor.fetchall()

    except Exception as e:
        print(f"Lỗi lấy vi phạm theo xe: {e}")
        return []

    finally:
        cursor.close()
        close_connection(conn)
def get_all_violations():

    conn = get_connection()

    if conn is None:
        return []

    cursor = conn.cursor(
        dictionary=True
    )

    query = """
    SELECT *
    FROM violations
    ORDER BY violation_id DESC
    """

    try:

        cursor.execute(query)

        return cursor.fetchall()

    except Exception as e:

        print(
            f"Loi lay violations: {e}"
        )

        return []

    finally:

        cursor.close()
        close_connection(conn)
def get_violations_by_plate(
    license_plate
):

    conn = get_connection()

    if conn is None:
        return []

    cursor = conn.cursor(
        dictionary=True
    )

    query = """
    SELECT
        v.license_plate,
        v.owner_name,
        v.vehicle_type,
        vl.violation_id,
        vl.violation_type,
        vl.violation_time,
        vl.image_path
    FROM violations vl
    JOIN vehicles v
        ON vl.vehicle_id = v.id
    WHERE v.license_plate = %s
    ORDER BY vl.violation_time DESC
    """

    try:

        cursor.execute(
            query,
            (license_plate,)
        )

        return cursor.fetchall()

    except Exception as e:

        print(
            f"Loi tra cuu: {e}"
        )

        return []

    finally:

        cursor.close()
        close_connection(conn)