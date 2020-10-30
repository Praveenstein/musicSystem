SELECT
	t.AlbumId,
    a.Title,
    COUNT(t.TrackId) AS number_of_tracks
FROM track t
INNER JOIN album a
	ON t.AlbumId = a.AlbumId
GROUP BY t.AlbumId
ORDER BY number_of_tracks DESC, t.AlbumId
LIMIT 20