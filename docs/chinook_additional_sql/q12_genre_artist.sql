SELECT DISTINCT 
	art.Name AS artist ,
	g.Name AS genre	   
FROM track t
INNER JOIN genre g
	ON t.GenreId = g.GenreId
INNER JOIN album a
	ON t.AlbumId = a.AlbumId
INNER JOIN artist art
	ON a.ArtistId = art.ArtistId
-- WHERE a.ArtistId = 6 
ORDER BY a.ArtistId
LIMIT 20