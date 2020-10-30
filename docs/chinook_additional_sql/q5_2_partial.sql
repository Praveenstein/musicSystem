WITH new_table AS(

	SELECT
		t.TrackId,
		t.GenreId,
		COUNT(il.InvoiceId) AS number_of_purchases
	FROM track t
	INNER JOIN invoiceline il
		ON t.TrackId = il.TrackId
	GROUP BY t.TrackId
	ORDER BY t.GenreId, number_of_purchases DESC, t.TrackId),
new_table_2 AS
		(SELECT
			g.GenreId AS c1,
            join_table.TrackId AS c2,
            join_table.number_of_purchases AS c3
		FROM genre g
		INNER JOIN (SELECT 	*
							FROM new_table
                            WHERE g.GenreId = new_table.GenreId
                            LIMIT 2) AS join_table
				ON g.GenreId = join_table.GenreId)
SELECT c1, c2, c3 FROM new_table_2
