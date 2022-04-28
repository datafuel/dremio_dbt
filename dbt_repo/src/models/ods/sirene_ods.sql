
with source as (
    SELECT * FROM {{ source('stg', 'sirene') }}
)

SELECT * FROM source