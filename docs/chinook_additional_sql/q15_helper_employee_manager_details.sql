SELECT
	CONCAT(e.FirstName, " ", e.LastName) AS emp,
    CONCAT(m.FirstName, " ", m.LastName) AS manager
FROM employee e
INNER JOIN employee m
	ON e.ReportsTo = m.EmployeeId
LIMIT 20