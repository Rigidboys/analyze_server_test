import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'db': 'test_schema',
    'charset': 'utf8mb4'
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

def get_all_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_table")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_data_by_column(col, value):
    ALLOWED_COLUMNS = ['office_name', 'master_name', 'product_name', 'customer_kind', 'phone_number', 'time_stamp']
    if col not in ALLOWED_COLUMNS:
        raise ValueError("허용되지 않은 컬럼명입니다.")
    
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"SELECT * FROM test_table WHERE {col} = %s"
    cursor.execute(sql, (value,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
