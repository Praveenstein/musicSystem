SELECT DISTINCT
	t.Name,
    g.Name
FROM track t
INNER JOIN genre g
	ON t.GenreId = g.GenreId
WHERE t.Name IN (SELECT
					t.Name
				FROM track t
				GROUP BY t.Name
				HAVING COUNT(DISTINCT t.GenreId) > 1
				ORDER BY COUNT(DISTINCT t.GenreId) DESC, t.TrackId)
ORDER BY t.Name
LIMIT 20