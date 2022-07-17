# Steps followed in the exercise

## Key problems / questions to solve

1. Top 5 customers in terms of card purchases (max. amount)

2. Top 5 merchant in terms of card purchases (max. amount)

3. Customers with most account transfers

4. Top merchant in terms of card purchases for an age band - 20-30yrs

5. Identify purchases within one hour of transfer to that account.


### Assumptions:

- All transactions are made in US dollars.
- Data model is modelled for the questions above.
- Certain information are excluded on purpose for eg. Country.

## Running a docker Neo4j-Entreprise

Run the below command replacing `$HOME` with the directory where the data files needs to be placed.

```
docker run \
    --name demoneo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/test \
    --env NEO4J_ACCEPT_LICENSE_AGREEMENT=yes \
    neo4j:enterprise
```

Logon to Neo4j Browser and make sure to create a database.
For this demo the have used db name `tester`

## Data model for the problem statement
Below is the data model, the json export can found at `datamodel/Bank_customer_transaction.json`
\
\
![Data Model](datamodel/Bank_customer_transaction.png)
\
\
Below are the considerations for the data model:
- Account and Card have been separated to enable future account and card additions to a customer
- Customer address can be separated out as separate entity but in this use case is limited need for address info, hence not loaded to graph database.
- Account and Card can have relationship link (for eg. sharing customer number) if there are more transfer to purchase relationship analysis.

## Script for Loading Data
Coding:
driver has the Driver class
loaddata to load data



Testing:

Conftest.py update the syspath
02 test update path

black & flake8

## Exploratory Queries
