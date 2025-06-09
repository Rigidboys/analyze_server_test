from flask import *
from flask_cors import CORS
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