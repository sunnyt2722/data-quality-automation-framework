{{ config(materialized='view') }}

SELECT
    payment_id,
    customer_id,
    payment_amount,
    payment_status
FROM {{ ref('payments') }}