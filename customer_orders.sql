SELECT o.order_id, o.shipping_limit_date, c.customer_state, p.payment_value
FROM fact_orders o
JOIN dim_customer c ON o.customer_id = c.customer_id
JOIN payment_dim p ON o.order_id = p.order_id;
