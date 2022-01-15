get_all_makes = """
    SELECT make 
    FROM ( 
        SELECT make, count(*) counter 
        FROM ads
        WHERE make <> '' 
        GROUP BY make 
        ORDER BY counter 
        desc LIMIT 50 
    ) m 
    ORDER BY make asc
"""


get_popular_makes = """
select distinct make
from web.ads
where make <> ''
order by make asc
"""


get_ads = """
select *
from web.ads
where 1 = 1
    {condition}
limit 25
"""
