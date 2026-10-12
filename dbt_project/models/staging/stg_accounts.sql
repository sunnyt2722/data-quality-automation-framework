{{ config(materialized='view') }}

SELECT
    account_id,
    customer_id,
    account_type,
    balance,
    status
FROM {{ ref('accounts') }}