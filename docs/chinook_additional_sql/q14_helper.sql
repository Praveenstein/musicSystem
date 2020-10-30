SELECT
	i.InvoiceId,
    i.InvoiceDate,
    c.SupportRepId
FROM invoice i
INNER JOIN customer c
	ON i.CustomerId = c.CustomerId
WHERE YEAR(i.InvoiceDate) = 2012 AND MONTH(i.InvoiceDate) = 08
