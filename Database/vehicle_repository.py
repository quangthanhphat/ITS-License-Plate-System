from Database.db import get_connection, close_connection


def get_vehicle_by_plate(license_plate):
    """
    Tìm xe theo biển số
    """

    conn = get_connection()

    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM vehicles
    WHERE license_plate = %s
    """

    cursor.execute(query, (license_plate,))

    vehicle = cursor.fetchone()

    cursor.close()
    close_connection(conn)

    return vehicle


def get_all_vehicles():
    """
    Lấy tất cả xe
    """

    conn = get_connection()

    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM vehicles
    """

    cursor.execute(query)

    vehicles = cursor.fetchall()

    cursor.close()
    close_connection(conn)

    return vehicles


def add_vehicle(
    license_plate,
    owner_name,
    vehicle_type
):
    """
    Thêm xe mới
    """

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor()

    query = """
    INSERT INTO vehicles
    (license_plate, owner_name, vehicle_type)
    VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(
            query,
            (
                license_plate,
                owner_name,
                vehicle_type
            )
        )

        conn.commit()

        return True

    except Exception as e:
        print(f"Lỗi thêm xe: {e}")
        return False

    finally:
        cursor.close()
        close_connection(conn)
def get_vehicle_by_id(vehicle_id):

    conn = get_connection()

    if conn is None:
        return None

    cursor = conn.cursor(
        dictionary=True
    )

    query = """
    SELECT *
    FROM vehicles
    WHERE id = %s
    """

    try:

        cursor.execute(
            query,
            (vehicle_id,)
        )

        return cursor.fetchone()

    except Exception as e:

        print(
            f"Loi tim xe: {e}"
        )

        return None

    finally:

        cursor.close()
        close_connection(conn)