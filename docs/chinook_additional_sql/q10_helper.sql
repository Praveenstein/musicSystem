SELECT
    t.Name,
    COUNT(DISTINCT t.GenreId) AS number_of_genre
FROM track t
GROUP BY t.Name
HAVING number_of_genre > 1
ORDER BY number_of_genre DESC, t.TrackId

