SELECT
	t.AlbumId,
    a.Title,
    COUNT(DISTINCT il.InvoiceId) AS number_of_purchases
FROM invoiceline il
INNER JOIN track t
	ON il.TrackId = t.TrackId
INNER JOIN album a
	ON t.AlbumId = a.AlbumId
GROUP BY t.AlbumId
ORDER BY number_of_purchases DESC, t.AlbumId
LIMIT 20