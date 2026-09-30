select
    cast(transaction_id as integer) as transaction_id,
    cast(customer_id as integer) as customer_id,
    cast(amount as decimal(18,2)) as amount,
    upper(trim(currency)) as currency,
    upper(trim(status)) as status,
    cast(transaction_ts as timestamp) as transaction_ts
from {{ ref('transactions') }}
