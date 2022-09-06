
-- ------ New Ads Daily Report -------- --

select
	s.source,
	`today - 7`,
	`today - 6`,
	`today - 5`,
	`today - 4`,
	`today - 3`,
	`today - 2`,
	`yesterday`,
	`today`,
	`Total Active`
	
from (
	select distinct source
	from parsers.ads
) as s
	
left join (
	select
		source,
		count(*) `today - 7`
	from parsers.ads
	where is_active = 1
		and date(uploaded) = subdate(current_date, 7)
	group by source
) as yesterday7
	on yesterday7.source = s.source

left join (
	select
		source,
		count(*) `today - 6`
	from parsers.ads
	where is_active = 1
		and date(uploaded) = subdate(current_date, 6)
	group by source
) as yesterday6
on yesterday6.source = s.source

left join (
	select
		source,
		count(*) `today - 5`
	from parsers.ads
	where is_active = 1
		and date(uploaded) = subdate(current_date, 5)
	group by source
) as yesterday5
	on yesterday5.source = s.source

left join (
	select
		source,
		count(*) `today - 4`
	from parsers.ads
	where is_active = 1
		and date(uploaded) = subdate(current_date, 4)
	group by source
) as yesterday4
	on yesterday4.source = s.source

left join (
	select
		source,
		count(*) `today - 3`
	from parsers.ads
	where is_active = 1
		and date(uploaded) = subdate(current_date, 3)
	group by source
) as yesterday3
	on yesterday3.source = s.source

left join (
	select
		source,
		count(*) `today - 2`
	from parsers.ads
	where is_active = 1
		and date(uploaded) = subdate(current_date, 2)
	group by source
) as yesterday2
	on yesterday2.source = s.source
	
left join (
	select
		source,
		count(*) `yesterday`
	from parsers.ads
	where is_active = 1
		and date(uploaded) = subdate(current_date, 1)
	group by source
) as yesterday
	on yesterday.source = s.source
	
left join (
	select
		source,
		count(*) `today`
	from parsers.ads
	where is_active = 1
		and date(uploaded) = subdate(current_date, 0)
	group by source
) as today
	on today.source = s.source
	
left join (
	select
		source,
		count(*) `Total Active`
	from parsers.ads
	where is_active = 1
	group by source
) as total
	on total.source = s.source

order by `today` desc