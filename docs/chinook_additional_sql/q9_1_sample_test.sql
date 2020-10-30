SELECT
   plt.PlaylistId,
   plt.TrackId,
   t.AlbumId
FROM playlisttrack plt
INNER JOIN track t
	ON plt.TrackId = t.TrackId
WHERE t.AlbumId = 322
