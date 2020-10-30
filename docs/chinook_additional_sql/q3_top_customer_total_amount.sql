SELECT 
	i.CustomerId,
    CONCAT(c.FirstName, " ", c.LastName) AS name,
    SUM(i.Total) AS total_amount
FROM invoice i
INNER JOIN customer c
	ON i.CustomerId = c.CustomerId
GROUP BY i.CustomerId
ORDER BY total_amount DESC, i.CustomerId