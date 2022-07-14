// Cypher Queries used to load data using LOAD CSV function.
// Create Customer, AccountNumber and CardNumber node
// Create relationships for Customer and AccountNumber, and Customer and CardNumber.

LOAD CSV WITH HEADERS FROM "https://gist.githubusercontent.com/maruthiprithivi/f11bf40b558879aca0c30ce76e7dec98/raw/f6800464bf4125b8dd218bc6168447a129205fdc/customers.csv" as row
MERGE (n :Customer {cif: row.CIF, firstName: row.FirstName, lastName: row.LastName, age: row.Age, jobTitle: row.JobTitle })
MERGE (a :AccountNumber {accountNumber: row.AccountNumber})
MERGE (c :CardNumber {cardNumber: row.CardNumber})
MERGE (n)-[:HAS_ACCOUNT]->(a)
MERGE (n)-[:HAS_CARD]->(c);


// Load Purchases data and connect it to CardNumber
LOAD CSV WITH HEADERS FROM "https://gist.githubusercontent.com/maruthiprithivi/f11bf40b558879aca0c30ce76e7dec98/raw/f6800464bf4125b8dd218bc6168447a129205fdc/purchases.csv" as row
MERGE (m :Merchant {merchantName: row.Merchant})
WITH m, row
MATCH (c :CardNumber {cardNumber: row.CardNumber})
MERGE (c)-[:PURCHASED_AT {transactionId: toInteger(row.TransactionID), transactionDateTime: datetime(replace(row.PurchaseDatetime, ' ', 'T')), amount: toFloat(row.Amount)}]->(m);

// Load Transfer data and connect it to AccountNumber
LOAD CSV WITH HEADERS FROM "https://gist.githubusercontent.com/maruthiprithivi/f11bf40b558879aca0c30ce76e7dec98/raw/f6800464bf4125b8dd218bc6168447a129205fdc/transfers.csv" as row
MATCH (s :AccountNumber {accountNumber: row.SenderAccountNumber})
MATCH (r :AccountNumber {accountNumber: row.ReceiverAccountNumber})
MERGE (s)-[:TRANSFERRED_TO {transactionId: toInteger(row.TransactionID), transactionDateTime: datetime(replace(row.TransferDatetime, ' ', 'T')), amount: toFloat(row.Amount)}]->(r);

