SELECT
	a.ArtistId,
    art.Name,
    COUNT(t.TrackId) AS number_of_tracks
FROM track t
INNER JOIN album a
	ON t.AlbumId = a.AlbumId
INNER JOIN artist art
	ON a.ArtistId = art.ArtistId
GROUP BY a.ArtistId
ORDER BY number_of_tracks DESC, a.ArtistId
LIMIT 20