import psycopg2
from psycopg2 import sql

# Параметры подключения к базе данных
DB_NAME = "medDb"
DB_USER = "postgres"
DB_PASSWORD = "12"
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_to_db():
    """Подключение к базе данных."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def fetch_data(table_name):
    """Получение данных из таблицы."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return columns, rows
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            return None, None
    return None, None

def fetch_medical_records():
    """Получение данных из MedicalRecord с расшифровкой внешних ключей."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    mr.record_id,
                    p.first_name || ' ' || p.last_name AS patient_name,
                    d.first_name || ' ' || d.last_name AS doctor_name,
                    ms.service_name,
                    mr.diagnosis,
                    mr.record_date
                FROM MedicalRecord mr
                LEFT JOIN Patient p ON mr.patient_id = p.patient_id
                LEFT JOIN Doctor d ON mr.doctor_id = d.doctor_id
                LEFT JOIN MedicalService ms ON mr.service_id = ms.service_id
            """
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return columns, rows
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            return None, None
    return None, None

def insert_medical_record(data):
    """Добавление новой записи в таблицу MedicalRecord."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO MedicalRecord (patient_id, doctor_id, service_id, diagnosis, treatment, record_date, next_visit_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data["patient_id"],
                data["doctor_id"],
                data["service_id"],
                data["diagnosis"],
                data["treatment"],
                data["record_date"],
                data["next_visit_date"]
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении данных: {e}")
            return False
    return False

def update_medical_record(record_id, data):
    """Обновление записи в таблице MedicalRecord."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                UPDATE MedicalRecord
                SET patient_id = %s, doctor_id = %s, service_id = %s, diagnosis = %s, treatment = %s, record_date = %s, next_visit_date = %s
                WHERE record_id = %s
            """
            cursor.execute(query, (
                data["patient_id"],
                data["doctor_id"],
                data["service_id"],
                data["diagnosis"],
                data["treatment"],
                data["record_date"],
                data["next_visit_date"],
                record_id
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении данных: {e}")
            return False
    return False

def fetch_patients():
    """Получение списка пациентов."""
    return fetch_data("patient")

def fetch_doctors():
    """Получение списка врачей."""
    return fetch_data("doctor")

def fetch_services():
    """Получение списка медицинских услуг."""
    return fetch_data("medicalservice")

def delete_medical_record(record_id):
    """Удаление записи из таблицы MedicalRecord."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM MedicalRecord WHERE record_id = %s"
            cursor.execute(query, (record_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка при удалении данных: {e}")
            return False
    return False

def insert_patient(data):
    """Добавление нового пациента."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO patient (first_name, last_name, date_of_birth, gender, phone_number, email, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data["first_name"],
                data["last_name"],
                data["date_of_birth"],
                data["gender"],
                data["phone_number"],
                data["email"],
                data["address"]
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении пациента: {e}")
            return False
    return False

def insert_doctor(data):
    """Добавление нового врача."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO doctor (first_name, last_name, specialization, phone_number, email)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data["first_name"],
                data["last_name"],
                data["specialization"],
                data["phone_number"],
                data["email"]
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении врача: {e}")
            return False
    return False

def insert_medical_service(data):
    """Добавление новой медицинской услуги."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO medicalservice (service_name, description, price)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (
                data["service_name"],
                data["description"],
                data["price"]
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении услуги: {e}")
            return False
    return False

def fetch_patient_by_id(patient_id):
    """Получение данных о пациенте по ID."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM Patient WHERE first_name = %s"
            cursor.execute(query, (patient_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"Ошибка при получении данных о пациенте: {e}")
            return None
    return None

def fetch_doctor_by_id(doctor_id):
    """Получение данных о враче по ID."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM Doctor WHERE first_name = %s"
            cursor.execute(query, (doctor_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"Ошибка при получении данных о враче: {e}")
            return None
    return None

def fetch_service_by_id(service_id):
    """Получение данных об услуге по ID."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM MedicalService WHERE service_name = %s"
            cursor.execute(query, (service_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"Ошибка при получении данных об услуге: {e}")
            return None
    return None


def generate_report(report_name, params=None):
    """Генерация отчета."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            if report_name == "patient_count_by_period":
                cursor.execute("SELECT get_patient_count_by_period(%s, %s)", (params["start_date"], params["end_date"]))
            elif report_name == "doctor_patient_count":
                cursor.execute("SELECT * FROM get_doctor_patient_count()")
            elif report_name == "inactive_patients":
                cursor.execute("SELECT * FROM get_inactive_patients()")
            elif report_name == "total_cost_for_patient":
                cursor.execute("SELECT get_total_cost_for_patient(%s)", (params["patient_id"],))
            elif report_name == "most_popular_services":
                cursor.execute("SELECT * FROM get_most_popular_services(%s)", (params["limit"],))
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return columns, rows
        except Exception as e:
            print(f"Ошибка при генерации отчета: {e}")
            return None, None
    return None, None