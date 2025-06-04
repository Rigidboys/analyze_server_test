from flask import *
from flask_cors import CORS
import pandas as pd
import pymysql
from analyze import *
from db_crud import *

app = Flask(__name__)
CORS(app)

@app.route('/analyze/purchase_trend', methods=['GET'])
def analyze_purchase_trend():
    try:
        result = get_purchase_trend()
        # result.index = result.index.astype(str)
        return jsonify(result.reset_index().to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze/volume_by_customer', methods=['GET'])
def analyze_volume_by_customer():
    try:
        result = get_volume_by_customer()
        return jsonify(result.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze/sales_by_type', methods=['GET'])
def analyze_sales_by_type():
    try:
        result = get_margin_and_sales_by_type()
        return jsonify(result.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze/periodic_summary', methods=['GET'])
def analyze_periodic_summary():
    try:
        result = get_periodic_summary()
        result.index = result.index.astype(str)
        return jsonify(result.reset_index().to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze/payment_compliance', methods=['GET'])
def analyze_payment_compliance():
    try:
        result = get_payment_compliance_rate()
        return jsonify({'compliance_rate': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5000)











# run = True
# while(run):
#     sel = eval(input("1. 전체 조회\n2. 삽입\n3. 테이블 구조\n4. 조회\n400. 종료\n>>"))
#     if sel == 1:
#         cursor.execute("SELECT * FROM test_table")
#         rows = cursor.fetchall()
#         for row in rows:
#             print(row)
#     if sel == 2:
#         office_name = input("회사명: ")
#         master_name = input("대표자명: ")
#         p_name = input("제품명: ")
#         price = eval(input("가격: "))
#         number = eval(input("수량: "))
#         kind = input("고객 유형")
#         p_number = input("전화번호: ")

#         values = (     
#             office_name,
#             master_name,
#             p_name,
#             price,
#             number,
#             kind,
#             str(p_number)
#         )

#         insert_data(cursor, conn, values)
#         print("삽입 완료!")

#     if sel == 3:
#         cursor.execute("DESC test_table")
#         columns = cursor.fetchall()
#         for col in columns:
#             print(col)
#     if sel == 4:
#         print("조회할 데이터 타입을 입력해주세요")
#         select = eval(input("1. 시간\n2. 상호명\n3. 대표명\n4. 제품명\n5. 구매자종류\n>>"))

#         if select == 1:
#             date = input("날짜(YYYY-MM-DD)를 입력해주세요: ")
#             sql = "SELECT * FROM test_table WHERE DATE(time_stamp) = %s"
#             cursor.execute(sql, (date,))
#             rows = cursor.fetchall()
#             for row in rows:
#                 print(row)
#         if select == 2:
#             name = input("상호명을 입력해주세요: ")
#             sql = "SELECT * FROM test_table WHERE office_name = %s"
#             cursor.execute(sql, (name,))
#             rows = cursor.fetchall()
#             for row in rows:
#                 print(row)
#     if sel == 400:
#         break