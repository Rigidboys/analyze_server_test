from db_crud import *
import pandas as pd
import os

ALLOWED_TABLES = set(os.getenv("ALLOWED_TABLES", "").split(','))

def load_df(table_name):
    if not table_name.isidentifier():
        raise ValueError("테이블명이 유효하지 않습니다.")
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"허용되지 않은 테이블명입니다: {table_name}")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM `{table_name}`")
    rows = cursor.fetchall()

    # 컬럼명 자동 추출
    col = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=col)

    cursor.close()
    conn.close()
    return df

def get_monthly_totals():
    df = load_df('purchase')
    df['purchased_date'] = pd.to_datetime(df['purchased_date'], errors='coerce')
    df = df.dropna(subset=['purchased_date', 'purchase_amount', 'purchase_price', 'purchase_or_sale'])

    # 총액 계산
    df['total'] = df['purchase_amount'] * df['purchase_price']
    df['year_month'] = df['purchased_date'].dt.to_period('M').astype(str)

    # 월 + 구분별 집계
    grouped = df.groupby(['year_month', 'purchase_or_sale'])['total'].sum().unstack(fill_value=0).reset_index()

    # 컬럼명 표준화
    grouped.rename(columns={
        '매출': 'sales_total',
        '매입': 'purchase_total'
    }, inplace=True)

    return grouped.to_dict(orient='records')

def get_sales_by_customer():
    df = load_df('purchase')

    # 매출만 필터링
    df = df[df['purchase_or_sale'] == '매출']
    df = df.dropna(subset=['customer_name', 'purchase_amount', 'purchase_price'])

    # 매출액 계산
    df['sales'] = df['purchase_amount'] * df['purchase_price']

    # 고객사별 합계
    result = df.groupby('customer_name')['sales'].sum().reset_index()

    return result.to_dict(orient='records')

def get_sales_by_product():
    df = load_df('purchase')

    df = df[df['purchase_or_sale'] == '매출']
    df = df.dropna(subset=['product_name', 'purchase_amount', 'purchase_price'])

    df['sales'] = df['purchase_amount'] * df['purchase_price']
    result = df.groupby('product_name')['sales'].sum().reset_index()

    return result.to_dict(orient='records')

def get_total_sales():
    df = load_df('purchase')
    df = df[(df['purchase_or_sale'] == '매출') & df['purchase_amount'].notna() & df['purchase_price'].notna()]
    return int((df['purchase_amount'] * df['purchase_price']).sum())

def get_total_purchases():
    df = load_df('purchase')
    df = df[(df['purchase_or_sale'] == '매입') & df['purchase_amount'].notna() & df['purchase_price'].notna()]
    return int((df['purchase_amount'] * df['purchase_price']).sum())

def get_total_paid_amount():
    df = load_df('purchase')
    df = df[df['is_payment'] == 1]
    df = df.dropna(subset=['paid_payment'])

    total_paid = int(df['paid_payment'].sum())
    return total_paid

def get_unpaid_amount():
    df = load_df('purchase')
    df = df[(df['purchase_or_sale'] == '매출') & (df['is_payment'] == 0)]
    df = df.dropna(subset=['purchase_amount', 'purchase_price'])
    unpaid = int((df['purchase_amount'] * df['purchase_price']).sum())
    return unpaid

def get_margin_rate_by_product():
    sales_df = load_df('purchase')
    product_df = load_df('product')

    # 매출 필터
    sales_df = sales_df[sales_df['purchase_or_sale'] == '매출']
    sales_df = sales_df.dropna(subset=['product_name', 'purchase_amount', 'purchase_price'])

    # 제품별 매출액 계산
    sales_df['sales'] = sales_df['purchase_amount'] * sales_df['purchase_price']

    # 제품별 수량 집계
    product_sales = sales_df.groupby('product_name').agg({
        'purchase_amount': 'sum',
        'sales': 'sum'
    }).reset_index()

    # 원가 join
    merged = pd.merge(product_sales, product_df[['product_name', 'production_price']], on='product_name', how='left')
    merged = merged.dropna(subset=['production_price'])

    # 총 원가 = 판매수량 * 단가
    merged['cost'] = merged['purchase_amount'] * merged['production_price']

    # 마진율 계산
    merged['margin_rate'] = ((merged['sales'] - merged['cost']) / merged['sales']) * 100
    merged['margin_rate'] = merged['margin_rate'].round(2)

    return merged[['product_name', 'sales', 'cost', 'margin_rate']].to_dict(orient='records')

def get_average_margin_rate():
    data = get_margin_rate_by_product()
    rates = [item['margin_rate'] for item in data if item['margin_rate'] is not None]
    if not rates:
        return 0.0
    return round(sum(rates) / len(rates), 2)

def get_payment_reliability_by_customer():
    df = load_df('purchase')

    # 매출만 분석 대상
    df = df[df['purchase_or_sale'] == '매출']
    df = df.dropna(subset=['customer_name', 'payment_period_end', 'is_payment'])

    # 기준일: 오늘 날짜
    today = pd.Timestamp.now()

    # 수금 마감일이 오늘보다 지난 경우 = 기한 도래
    df['overdue'] = df['payment_period_end'] < today

    # 기한 도래 + 수금 미완료 → 신뢰도 낮음
    df['on_time'] = (df['overdue'] == False) | (df['is_payment'] == 1)

    # 고객사별 수금 신뢰도 비율 계산
    grouped = df.groupby('customer_name')['on_time'].mean().reset_index()
    grouped['reliability_rate'] = (grouped['on_time'] * 100).round(2)
    result = grouped[['customer_name', 'reliability_rate']]

    return result.to_dict(orient='records')
