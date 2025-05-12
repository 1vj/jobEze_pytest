import pytest
from unittest.mock import patch, MagicMock
from utils.db.SSHDatabase_Connect import SSHDatabase_Connect


# Test for connect_to_database
@patch("utils.db.SSHDatabase_Connect.pymysql.connect")
@patch("utils.db.SSHDatabase_Connect.SSHTunnelForwarder")
def test_connect_to_database(mock_tunnel, mock_pymysql):
    mock_server = MagicMock()
    mock_db = MagicMock()

    mock_tunnel.return_value = mock_server
    mock_pymysql.return_value = mock_db

    result = SSHDatabase_Connect.connect_to_database(
        database="test_db",
        host_ip="127.0.0.1",
        ssh_username="test_user",
        ssh_password="test_pass"
    )

    assert result == [mock_server, mock_db]
    mock_tunnel.assert_called_once()
    mock_db.cursor.assert_not_called()  # just connection test


# Test for connect_to_database_remote
@patch("utils.db.SSHDatabase_Connect.pymysql.connect")
@patch("utils.db.SSHDatabase_Connect.SSHTunnelForwarder")
def test_connect_to_database_remote(mock_tunnel, mock_pymysql):
    mock_server = MagicMock()
    mock_db = MagicMock()

    mock_tunnel.return_value = mock_server
    mock_pymysql.return_value = mock_db

    result = SSHDatabase_Connect.connect_to_database_remote(
        db_name="remote_db",
        jump_ip="10.10.10.10",
        jump_username="jump_user",
        jump_password="jump_pass",
        remote_ip="192.168.1.100",
        remote_key="/mock/path/to/key"
    )

    assert result == [mock_server, mock_db]


# Test for fetch_single_data_from_database
def test_fetch_single_data_from_database():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_db.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("data1",)]

    result = SSHDatabase_Connect.fetch_single_data_from_database(
        db=mock_db,
        query="SELECT name FROM users LIMIT 1"
    )

    assert result == ("data1",)


# Test for fetch_multiple_data_from_database
def test_fetch_multiple_data_from_database():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_db.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("row1",), ("row2",)]

    result = SSHDatabase_Connect.fetch_multiple_data_from_database(
        db=mock_db,
        query="SELECT name FROM users"
    )

    assert result == [("row1",), ("row2",)]


# Test for closing connections
def test_close_database_connection():
    mock_db = MagicMock()
    mock_server = MagicMock()

    SSHDatabase_Connect.close_database_connection(mock_db, mock_server)

    mock_db.close.assert_called_once()
    mock_server.close.assert_called_once()
