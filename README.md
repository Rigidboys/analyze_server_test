# 📊 매출/매입 분석 서버

Flask + Pandas 기반의 DB 분석 서버입니다.  
`purchase`, `product`, `customer` 테이블을 기반으로 다양한 매출/수금/마진/신뢰도 분석을 제공합니다.

---

## ✅ 기능 요약

| 기능                    | 설명 |
|-------------------------|------|
| 월별 매입/매출 총액     | 월별 합계 집계 |
| 고객사별 매출액         | `customer_name` 기준 매출 |
| 제품별 매출 비율        | `product_name` 기준 매출 |
| 총 매출/매입/수금/미수금 | KPI 지표 반환 |
| 제품별 마진율 분석      | 제품별 판매원가/이익 계산 |
| 평균 마진율             | 전체 마진율 평균값 |
| 고객사별 수금 신뢰도    | 납기일 기준 수금 준수율 분석 |

---

## 📦 API 목록

> Base URL: `http://localhost:5000`

| Method | Endpoint                     | 설명 |
|--------|------------------------------|------|
| GET    | `/api/total_sales`           | 총 매출액 반환 |
| GET    | `/api/total_purchases`       | 총 매입액 반환 |
| GET    | `/api/total_paid`            | 수금 완료 총액 |
| GET    | `/api/unpaid`                | 미수금 총액 |
| GET    | `/api/margin_by_product`     | 제품별 마진율 |
| GET    | `/api/avg_margin_rate`       | 평균 마진율 |
| GET    | `/api/sales_by_customer`     | 고객사별 매출 |
| GET    | `/api/sales_by_product`      | 제품별 매출 |
| GET    | `/api/monthly_totals`        | 월별 매출/매입 집계 |
| GET    | `/api/payment_reliability`   | 고객사별 수금 신뢰도 |

---

## ⚙️ 설치 방법

```bash
git clone <this-repo>
cd <this-repo>
pip install -r requirements.txt
