SELECT
	plt.TrackId,
    t.Name,
    COUNT(plt.PlaylistId) AS number_of_playlist
FROM playlisttrack plt
INNER JOIN track t
	ON plt.TrackId = t.TrackId
GROUP BY plt.TrackId
ORDER BY number_of_playlist DESC, plt.TrackId
LIMIT 20