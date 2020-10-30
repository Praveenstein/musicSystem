SELECT 
	genre_ranked_table.TrackId,
    genre_ranked_table.track_name,
    genre_ranked_table.GenreId,
    genre_ranked_table.genre_name,
    genre_ranked_table.number_of_purchases
FROM (
		SELECT
			t.TrackId,
			t.Name AS track_name,
			t.GenreId,
			g.Name AS genre_name,
			COUNT(il.InvoiceId) AS number_of_purchases,
			ROW_NUMBER() OVER (PARTITION BY t.GenreId ORDER BY COUNT(il.InvoiceId) DESC) AS genre_rank
		FROM track t
		INNER JOIN invoiceline il
			ON t.TrackId = il.TrackId
		INNER JOIN genre g
			ON t.GenreId = g.GenreId
		GROUP BY t.TrackId) AS genre_ranked_table
WHERE genre_ranked_table.genre_rank < 3