from flask import *
from flask_cors import CORS
from analyze import *
from db_crud import *
from logger import log_analysis, log_error

app = Flask(__name__)
CORS(app)

@app.route('/api/monthly_totals', methods=['GET'])
def monthly_totals():
    try:
        user_id, role = get_user_info_from_token()
        log_analysis('/api/monthly_totals', "월별 매출/매입 총액 조회")
        return jsonify(get_monthly_totals(user_id, role))
    except Exception as e:
        log_error('/api/monthly_totals', e)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/total_sales', methods=['GET'])
def total_sales():
    try:
        user_id, role = get_user_info_from_token()
        log_analysis('/api/total_sales', "총 매출액 조회")
        return jsonify({"total_sales": get_total_sales(user_id, role)})
    except Exception as e:
        log_error('/api/total_sales', e)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/total_purchases', methods=['GET'])
def total_purchases():
    try:
        user_id, role = get_user_info_from_token()
        log_analysis('/api/total_purchases', "총 매입액 조회")
        return jsonify({"total_purchases": get_total_purchases(user_id, role)})
    except Exception as e:
        log_error('/api/total_purchases', e)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/total_paid', methods=['GET'])
def total_paid():
    try:
        user_id, role = get_user_info_from_token()
        log_analysis('/api/total_paid', "총 지불액 조회")
        return jsonify({"total_paid": get_total_paid_amount(user_id, role)})
    except Exception as e:
        log_error('/api/total_paid', e)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/unpaid', methods=['GET'])
def unpaid():
    try:
        user_id, role = get_user_info_from_token()
        log_analysis('/api/unpaid', "미지불 금액 조회")
        return jsonify({"unpaid": get_unpaid_amount(user_id, role)})
    except Exception as e:
        log_error('/api/unpaid', e)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/margin_by_product', methods=['GET'])
def margin_by_product():
    try:
        user_id, role = get_user_info_from_token()
        log_analysis('/api/margin_by_product', "제품별 마진율 조회")
        return jsonify(get_margin_rate_by_product(user_id, role))
    except Exception as e:
        log_error('/api/margin_by_product', e)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/avg_margin_rate', methods=['GET'])
def avg_margin_rate():
    try:
        user_id, role = get_user_info_from_token()
        log_analysis('/api/avg_margin_rate', "평균 마진율 조회")
        return jsonify({"average_margin_rate": get_average_margin_rate(user_id, role)})
    except Exception as e:
        log_error('/api/avg_margin_rate', e)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/payment_reliability', methods=['GET'])
def payment_reliability():
    try:
        user_id, role = get_user_info_from_token()
        log_analysis('/api/payment_reliability', "고객사별 결제 신뢰도 조회")
        return jsonify({"payment_reliability": get_payment_reliability_by_customer(user_id, role)})
    except Exception as e:
        log_error('/api/payment_reliability', e)
        return jsonify({"error": "Internal server error"}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5000)