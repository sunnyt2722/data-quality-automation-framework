select
    c.customer_id,
    c.first_name,
    c.last_name,
    count(t.transaction_id) as transaction_count,
    coalesce(sum(case when t.status = 'COMPLETED' then t.amount else 0 end), 0) as completed_amount
from {{ ref('stg_customers') }} c
left join {{ ref('stg_transactions') }} t on c.customer_id = t.customer_id
group by 1,2,3
