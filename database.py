import mysql.connector
from dotenv import dotenv_values

config_env = {
    **dotenv_values(".env.secret")
}

# MySQL connection details
DB_NAME = config_env.get("DB_NAME")
TABLE_NAME = config_env.get("TABLE_NAME")

config = {
    "host": config_env.get("DB_HOST"),
    "user": config_env.get("DB_USER"),
    "password": config_env.get("DB_PASSWORD")
}
def init_db():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Create DB if not exists
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    print(f"Database `{DB_NAME}` ready.")

    conn.database = DB_NAME

    # Create Table if not exists
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            face_name VARCHAR(50) NOT NULL UNIQUE,
            face LONGBLOB NOT NULL
        )
    """)
    print(f"Table `{TABLE_NAME}` ready inside `{DB_NAME}`.")
    conn.commit()
    cursor.close()
    conn.close()

def get_connection():
    conn = mysql.connector.connect(database=DB_NAME, **config)
    return conn

def get_next_face_counter():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT MAX(id) FROM {TABLE_NAME}")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result[0] is not None else 0
