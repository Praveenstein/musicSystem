SELECT
	*
FROM invoiceline il
INNER JOIN track t
	ON il.TrackId = t.TrackId
WHERE t.AlbumId = 257