// 1. Top 5 customers in terms of card purchases (max. amount)
MATCH (cust :Customer)-[:HAS_CARD]->(card :CardNumber)-[p :PURCHASED_AT]->(m :Merchant)
RETURN DISTINCT cust.firstName+" "+cust.lastName AS customerName,sum(p.amount) AS totalPurchaseAmount
ORDER BY totalPurchaseAmount desc
LIMIT 5
;

// 2. Top 5 merchant in terms of card purchases (max. amount)
MATCH (card :CardNumber)-[p :PURCHASED_AT]->(m :Merchant)
RETURN DISTINCT m.merchantName, sum(p.amount) AS totalPurchaseAmount
ORDER BY totalPurchaseAmount desc
LIMIT 5
;

// 3. Customers with most account transfers
MATCH (acct1 :AccountNumber)-[t :TRANSFERRED_TO]->(acct2 :AccountNumber)
WITH acct1, count(t) AS transferCount
RETURN acct1, transferCount
ORDER BY transferCount
;

// 4. Top merchant in terms of card purchases for an age band - 20-30yrs
MATCH (cust :Customer)-[:HAS_CARD]->(:CardNumber)-[p :PURCHASED_AT]->(m :Merchant)
WHERE toInteger(cust.age) >=20 AND cust.age <= 30
RETURN DISTINCT m.merchantName AS merchant, sum(p.amount) AS totalPurchasedAmount
ORDER BY totalPurchasedAmount
LIMIT 1
;

// 5. Identify purchases within one hour of transfer to that account.
MATCH (acct1 :AccountNumber)-[trans :TRANSFERRED_TO]->(acct2 :AccountNumber)<-[:HAS_ACCOUNT]-(cust :Customer)-[:HAS_CARD]->(card :CardNumber)-[purch :PURCHASED_AT]->(m :Merchant)
WITH trans.transactionDateTime AS transferDateTime, purch.transactionDateTime AS purchaseDateTime, purch.amount AS purchaseAmount, purch.transactionId AS purchaseTransaction, m.merchantName AS merchantName
WHERE transferDateTime < purchaseDateTime < transferDateTime + duration({hours: 1})
RETURN purchaseTransaction, purchaseAmount, merchantName, "Verify Transaction" AS statusFlag
;

// The above query (5) can be improved a bit faster by adding potential relationship between accountnumber and card number that is shared by customer.