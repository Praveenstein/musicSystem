SELECT
	t.AlbumId,
    a.Title,
    SUM(t.Milliseconds) AS total_playtime
FROM track t
INNER JOIN album a
	ON t.AlbumId = a.AlbumId
GROUP BY t.AlbumId
ORDER BY total_playtime DESC, t.AlbumId
LIMIT 20
