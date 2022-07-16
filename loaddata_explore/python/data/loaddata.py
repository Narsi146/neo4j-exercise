import os
import pandas as pd
from dotenv import load_dotenv
from driver import Neo4jDriver


def add_customers(link, conn, db=None):
    """Adds customer nodes to the Neo4j graph as a batch job."""
    rows = pd.read_csv(link)
    query = """
            UNWIND $rows AS row
            MERGE (n :Customer {cif: row.CIF, firstName: row.FirstName, lastName: row.LastName, age: toInteger(row.Age), jobTitle: row.JobTitle })
            MERGE (a :AccountNumber {accountNumber: row.AccountNumber})
            MERGE (c :CardNumber {cardNumber: row.CardNumber})
            MERGE (n)-[:HAS_ACCOUNT]->(a)
            MERGE (n)-[:HAS_CARD]->(c)
            RETURN "Customers, Accounts and Cards merged" as Response
            ;
            """
    return insert_data(query, rows, conn, db)


def add_purchases(link, conn, db=None):
    """Adds customer nodes to the Neo4j graph as a batch job."""
    rows = pd.read_csv(link)
    query = """
            UNWIND $rows AS row
            MERGE (m :Merchant {merchantName: row.Merchant})
            WITH m, row
            MATCH (c :CardNumber {cardNumber: row.CardNumber})
            MERGE (c)-[:PURCHASED_AT {transactionId: toInteger(row.TransactionID), transactionDateTime: datetime(replace(row.PurchaseDatetime, ' ', 'T')), amount: toFloat(row.Amount)}]->(m)
            RETURN "Purchases merged" as Response
            ;
            """
    return insert_data(query, rows, conn, db)


def add_transfers(link, conn, db=None):
    """Adds customer nodes to the Neo4j graph as a batch job."""
    rows = pd.read_csv(link)
    query = """
            UNWIND $rows AS row
            MATCH (s :AccountNumber {accountNumber: row.SenderAccountNumber})
            MATCH (r :AccountNumber {accountNumber: row.ReceiverAccountNumber})
            MERGE (s)-[:TRANSFERRED_TO {transactionId: toInteger(row.TransactionID), transactionDateTime: datetime(replace(row.TransferDatetime, ' ', 'T')), amount: toFloat(row.Amount)}]->(r)
            RETURN "Transfers merged" as Response
            ;
            """
    return insert_data(query, rows, conn, db)


def insert_data(query, rows, conn=None, db=None):
    # Function to handle the updating the Neo4j database in batch mode.
    results = None
    try:
        results = conn.query(query, parameters={"rows": rows.to_dict("records")}, db=db)
    except e:
        print("Error querying the database", e)

    if results is None:
        print("Load Failed")
    else:
        print(results[0]["Response"])


if __name__ == "__main__":
    """ """
    load_dotenv()
    conn = Neo4jDriver(
        os.environ.get("NEO4J_URI"),
        os.environ.get("NEO4J_USERNAME"),
        os.environ.get("NEO4J_PASSWORD"),
    )

    db = os.environ.get("DB")

    # Load Customer Data
    customerDataLink = os.environ.get("CUSTOMERDATA")
    if customerDataLink:
        add_customers(customerDataLink, conn, "tester")

    # Load Purchase Data
    purchaseDataLink = os.environ.get("PURCHASEDATA")
    if purchaseDataLink:
        add_purchases(purchaseDataLink, conn, "tester")

    # Load Transfer Data
    transferDataLink = os.environ.get("TRANSFERDATA")
    if transferDataLink:
        add_transfers(transferDataLink, conn, "tester")

    conn.close()
