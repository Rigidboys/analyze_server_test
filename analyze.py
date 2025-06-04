from db_crud import *
import pandas as pd

def load_df():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_table")
    rows = cursor.fetchall()

    # 컬럼명 자동 추출
    col = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=col)

    cursor.close()
    conn.close()
    return df

def get_purchase_trend():
    df = load_df()
    return df.groupby('time_stamp')['product_number'].sum().sort_index()

def get_volume_by_customer():
    df = load_df()
    return df.groupby('office_name')['product_number'].sum().sort_values(ascending=False)

def get_margin_and_sales_by_type():
    df = load_df()
    df['margin'] = df['product_price'] * df['product_number']
    result = df.groupby('customer_kind')['margin'].sum()
    return result

def get_periodic_summary():
    df = load_df()
    df['date'] = pd.to_datetime(df['time_stamp'], unit='s')  # timestamp가 int형일 경우
    df['month'] = df['date'].dt.to_period('M')
    return df.groupby('month')['product_price'].agg(['sum', 'count'])

def get_payment_compliance_rate():
    df = load_df()
    df['due_date'] = pd.to_datetime(df['due_date'])
    df['payment_date'] = pd.to_datetime(df['payment_date'])
    df['on_time'] = df['payment_date'] <= df['due_date']
    return df['on_time'].mean()  # 비율로 반환
