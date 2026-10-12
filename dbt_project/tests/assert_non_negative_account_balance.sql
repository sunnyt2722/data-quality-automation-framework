SELECT
    account_id,
    balance
FROM {{ ref('stg_accounts') }}
WHERE balance < 0