SELECT
	t.TrackId,
    t.Name AS track_name,
    t.GenreId,
    g.Name AS genre_name,
    COUNT(il.InvoiceId) AS number_of_purchases,
    ROW_NUMBER() OVER (PARTITION BY t.GenreId ORDER BY t.GenreId, COUNT(il.InvoiceId) DESC) AS genre_rank
FROM track t
INNER JOIN invoiceline il
	ON t.TrackId = il.TrackId
INNER JOIN genre g
	ON t.GenreId = g.GenreId
GROUP BY t.TrackId