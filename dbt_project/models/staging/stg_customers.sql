select
    cast(customer_id as integer) as customer_id,
    trim(first_name) as first_name,
    trim(last_name) as last_name,
    lower(trim(email)) as email,
    upper(trim(country_code)) as country_code,
    cast(created_at as date) as created_at
from {{ ref('customers') }}
