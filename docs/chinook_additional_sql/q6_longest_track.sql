SELECT 
	t.TrackId,
    t.Name,
    t.Milliseconds
FROM track t
ORDER BY t.Milliseconds DESC, t.TrackId
LIMIT 20