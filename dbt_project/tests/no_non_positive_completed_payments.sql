SELECT
    payment_id,
    payment_amount,
    payment_status
FROM {{ ref('stg_payments') }}
WHERE payment_status = 'COMPLETED'
  AND (payment_amount <= 0 OR payment_amount IS NULL)