SELECT
    t.AlbumId,
    a.Title,
    COUNT(DISTINCT plt.PlaylistId) AS number_of_playlist
FROM playlisttrack plt
INNER JOIN track t
	ON plt.TrackId = t.TrackId
INNER JOIN album a
	ON t.AlbumId = a.AlbumId
GROUP BY t.AlbumId
ORDER BY number_of_playlist DESC, t.AlbumId
LIMIT 20