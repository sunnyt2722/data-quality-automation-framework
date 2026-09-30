select *
from {{ ref('stg_transactions') }}
where status = 'COMPLETED' and amount <= 0
