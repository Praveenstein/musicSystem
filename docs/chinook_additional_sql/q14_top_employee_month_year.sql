SELECT
	c.SupportRepId AS employee_id,
    CONCAT(e.FirstName, " ", e.LastName) AS employee_name,
    COUNT(i.InvoiceId) AS total_sales    
FROM invoice i
INNER JOIN customer c
	ON i.CustomerId = c.CustomerId
INNER JOIN employee e
	ON c.SupportRepId = e.EmployeeId
WHERE YEAR(i.InvoiceDate) = 2012 AND MONTH(i.InvoiceDate) = 08
GROUP BY c.SupportRepId
ORDER BY total_sales DESC, c.SupportRepId