ads_by_filters = """
select
    *,
    coalesce(ACOS(SIN(latitude * 3.14159 / 180) * SIN({latitude} * 3.14159 / 180) + COS(latitude * 3.14159 / 180) * COS({latitude} * 3.14159 / 180) * COS((longitude - {longitude}) * 3.14159 / 180)), 99999) as distance
from web.ads
where 1 = 1
    {conditions}
ORDER BY distance asc
limit {offset}, {per_page};
"""


total_by_filters = """
select
    count(*)
from web.ads
where 1 = 1
    {conditions}
"""


# TODO: Make query that would search in title/description/make/models/etc
ads_by_search = """
"""

makes_for_filter = """
SELECT make
FROM (
    SELECT
        make,
        count(*) counter
    FROM web.ads
    WHERE make <> ''
    GROUP BY make
    ORDER BY counter desc
    LIMIT 50
) m
ORDER BY make asc
;
"""
