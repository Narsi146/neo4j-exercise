import os


def query_data(query, conn=None, db=None):
    # Function to handle the updating the Neo4j database in batch mode.
    results = None
    results = conn.query(query, db=db)
    return results


def test_env_vars():
    """Test that environment variables have been set"""

    assert "DB" in os.environ
    assert "CUSTOMERDATA" in os.environ
    assert "TRANSFERDATA" in os.environ
    assert "PURCHASEDATA" in os.environ


def test_load_data():
    """Check whether are you able to load data"""
    # Update loaddata.py
    result = os.system(
        r"python ./data/loaddata.py"
    )
    assert result == 0


def test_customer_account_counts(conn):
    """Check whether are you able to load data"""
    query = """MATCH (n :Customer)-[r: HAS_ACCOUNT]->(a :AccountNumber)
    RETURN COUNT(n) as totalCustomers, COUNT(r) as totalRelationships, count(a) as totalAccounts;
    """
    result = query_data(query, conn, db=os.environ.get("DB"))
    assert result[0]["totalCustomers"] == 100
    assert result[0]["totalRelationships"] == 100
    assert result[0]["totalAccounts"] == 100


def test_transfer_account_counts(conn):
    """Check whether are you able to load data"""
    query = """MATCH (acct1 :AccountNumber)-[r: TRANSFERRED_TO]->(acct2 :AccountNumber)
    RETURN COUNT(distinct(acct1)) as sourceAcctCount, COUNT(r) as totalTransfers, count(distinct(acct2)) as destAcctCount;
    """
    result = query_data(query, conn, db=os.environ.get("DB"))
    assert result[0]["sourceAcctCount"] == 100
    assert result[0]["totalTransfers"] == 1000
    assert result[0]["destAcctCount"] == 100


def test_purchase_merchant_counts(conn):
    """Check whether are you able to load data"""
    query = """MATCH (c :CardNumber)-[r: PURCHASED_AT]->(m :Merchant)
    RETURN COUNT(distinct(c)) as totalCards, COUNT(r) as totalPurchases, count(distinct(m)) as merchantCount;
    """
    result = query_data(query, conn, db=os.environ.get("DB"))
    assert result[0]["totalCards"] == 100
    assert result[0]["totalPurchases"] == 10000
    assert result[0]["merchantCount"] == 30
