select category, count(*) as c from noteevents 
group by category 
order by c desc

select description, count(*) as c from noteevents
where trim(lower(description)) like '%admission%'
group by description
order by c desc

select '****NEW-NOTE****' || text AS text_note from noteevents
where trim(lower(category)) = 'physician'
and trim(lower(description)) = 'physician resident admission note'
limit 1