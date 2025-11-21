from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1013@localhost:5432/store_db'
db = SQLAlchemy(app)

# جدول مشتری
class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # ارتباط با سفارش‌ها
    orders = db.relationship("Order", backref="customer", lazy=True)

# جدول سفارش
class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)  # تاریخ سفارش
    department = db.Column(db.String(100), nullable=False)        # بخش فروش
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)

# API برای گرفتن لیست مشتری‌ها
@app.route("/customers")
def get_customers():
    customers = Customer.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in customers])

# API برای گرفتن لیست سفارش‌ها
@app.route("/orders")
def get_orders():
    orders = Order.query.all()
    return jsonify([
        {
            "id": o.id,
            "order_date": o.order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "department": o.department,
            "customer": o.customer.name
        }
        for o in orders
    ])

if __name__ == "__main__":
    app.run(debug=True)
