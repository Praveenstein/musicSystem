SELECT
    e.ReportsTo AS manager_id,
    CONCAT(m.FirstName, " ", m.LastName) AS manager_name,
    SUM(i.Total) AS total_revenue
FROM invoice i
INNER JOIN customer c
	ON i.CustomerId = c.CustomerId
INNER JOIN employee e
	ON c.SupportRepId = e.EmployeeId
INNER JOIN employee m
	ON e.ReportsTo = m.EmployeeId
WHERE YEAR(i.InvoiceDate) = 2012 AND MONTH(i.InvoiceDate) = 08
GROUP BY manager_id
ORDER BY total_revenue DESC