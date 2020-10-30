SELECT
	t.TrackId,
    t.Name,
    t.GenreId,
    COUNT(il.InvoiceId) AS number_of_purchases
FROM track t
INNER JOIN invoiceline il
	ON t.TrackId = il.TrackId
GROUP BY t.TrackId
ORDER BY t.GenreId, number_of_purchases DESC, t.TrackId