import os


def test_env_vars():
    """Test that environment variables have been set"""

    assert "NEO4J_URI" in os.environ
    assert "NEO4J_USERNAME" in os.environ
    assert "NEO4J_PASSWORD" in os.environ


def test_driver_initiated(conn):
    """Test that driver is working"""
    assert conn is not None
