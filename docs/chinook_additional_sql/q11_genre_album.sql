SELECT DISTINCT
	a.title AS album,
	g.Name AS genre	  
FROM track t
INNER JOIN album a
	ON t.AlbumId = a.AlbumId
INNER JOIN genre g
	ON t.GenreId = g.GenreId
-- WHERE t.AlbumId = 102 OR t.AlbumId = 251 
ORDER BY t.AlbumId
LIMIT 20