select *
from {{ ref('stg_transactions') }}
where transaction_ts > current_timestamp
