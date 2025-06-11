from flask import *
from flask_cors import CORS
from analyze import *
from db_crud import *

app = Flask(__name__)
CORS(app)

@app.route('/api/monthly_totals', methods=['GET'])
def monthly_totals():
    try:
        return jsonify(get_monthly_totals())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/total_sales', methods=['GET'])
def total_sales():
    try:
        return jsonify({"total_sales": get_total_sales()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/total_purchases', methods=['GET'])
def total_purchases():
    try:
        return jsonify({"total_purchases": get_total_purchases()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/total_paid', methods=['GET'])
def total_paid():
    try:
        return jsonify({"total_paid": get_total_paid_amount()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/unpaid', methods=['GET'])
def unpaid():
    try:
        return jsonify({"unpaid": get_unpaid_amount()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/margin_by_product', methods=['GET'])
def margin_by_product():
    try:
        return jsonify(get_margin_rate_by_product())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/avg_margin_rate', methods=['GET'])
def avg_margin_rate():
    try:
        return jsonify({"average_margin_rate": get_average_margin_rate()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/payment_reliability', methods=['GET'])
def payment_reliability():
    try:
        return jsonify({"payment_reliability": get_payment_reliability_by_customer()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5000)