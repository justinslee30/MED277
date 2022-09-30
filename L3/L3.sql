select '****NEW-NOTE****' || text AS text_note from noteevents
where trim(lower(category)) = 'physician'
and trim(lower(description)) = 'physician resident admission note'
ORDER BY RANDOM()
limit 1