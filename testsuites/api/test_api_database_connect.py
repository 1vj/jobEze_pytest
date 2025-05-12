import unittest
import logging
from unittest.mock import patch, MagicMock
from utils.db.APIDatabase_Connect import APIDatabase_Connect   # Replace with the actual path of your class

log = logging.getLogger(__name__)


class TestAPIDatabaseConnect(unittest.TestCase):

    @patch('mysql.connector.connect')
    def test_connect_to_database(self, mock_connect):
        """Test the database connection method."""
        # Mock the connection and cursor objects
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Call the connect_to_database method
        cursor, connection = APIDatabase_Connect.connect_to_database(
            database_name="test_db",
            db_user="test_user",
            db_pass="test_pass",
            host="localhost"
        )

        # Check if mysql.connector.connect is called with the right arguments
        mock_connect.assert_called_once_with(
            host="localhost",
            user="test_user",
            password="test_pass",
            database="test_db",
            port=3306
        )

        # Verify cursor and connection returned correctly
        self.assertEqual(cursor, mock_cursor)
        self.assertEqual(connection, mock_connection)
        log.info("Connection is successful to the database")

    @patch('mysql.connector.connect')
    def test_alter_data_into_db_table(self, mock_connect):
        """Test the alter_data_into_db_table method."""
        # Mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Call the connect method to simulate a connection
        cursor, connection = APIDatabase_Connect.connect_to_database(
            database_name="test_db",
            db_user="test_user",
            db_pass="test_pass",
            host="localhost"
        )

        # Prepare SQL query
        sql_query = "INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com')"

        # Call the method
        APIDatabase_Connect.alter_data_into_db_table(cursor, connection, sql_query)

        # Check if execute is called with correct SQL query
        mock_cursor.execute.assert_called_once_with(sql_query)

        # Check if commit is called after executing the query
        mock_connection.commit.assert_called_once()

    @patch('mysql.connector.connect')
    def test_fetch_single_data_from_table(self, mock_connect):
        """Test fetching a single row from the database."""
        # Mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Simulate the result of fetchone
        mock_cursor.fetchone.return_value = ('John Doe', 'john@example.com')

        # Call the connect method to simulate a connection
        cursor, connection = APIDatabase_Connect.connect_to_database(
            database_name="test_db",
            db_user="test_user",
            db_pass="test_pass",
            host="localhost"
        )

        # SQL query for fetching
        sql_query = "SELECT * FROM users WHERE id=1"

        # Call the fetch method
        result = APIDatabase_Connect.fetch_single_data_from_table(cursor, sql_query)
        log.info("Able to fetch the single record")
        log.info(f"{result}")

        # Verify if execute was called with the correct query
        mock_cursor.execute.assert_called_once_with(sql_query)

        # Check if the fetchone method was called
        mock_cursor.fetchone.assert_called_once()

        # Verify the result returned by fetchone
        self.assertEqual(result, ('John Doe', 'john@example.com'))

    @patch('mysql.connector.connect')
    def test_fetch_multiple_data_from_table(self, mock_connect):
        """Test fetching multiple rows from the database."""
        # Mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Simulate the result of fetchall
        mock_cursor.fetchall.return_value = [
            ('John Doe', 'john@example.com'),
            ('Jane Doe', 'jane@example.com')
        ]

        # Call the connect method to simulate a connection
        cursor, connection = APIDatabase_Connect.connect_to_database(
            database_name="test_db",
            db_user="test_user",
            db_pass="test_pass",
            host="localhost"
        )

        # SQL query for fetching
        sql_query = "SELECT * FROM users"

        # Call the fetch method
        result = APIDatabase_Connect.fetch_multiple_data_from_table(cursor, sql_query)
        log.info("Able to fetch the multiple records")
        log.info(f"{result}")

        # Verify if execute was called with the correct query
        mock_cursor.execute.assert_called_once_with(sql_query)

        # Check if the fetchall method was called
        mock_cursor.fetchall.assert_called_once()

        # Verify the result returned by fetchall
        self.assertEqual(result, [
            ('John Doe', 'john@example.com'),
            ('Jane Doe', 'jane@example.com')
        ])

    @patch('mysql.connector.connect')
    def test_close_database_connection(self, mock_connect):
        """Test the close_database_connection method."""
        # Mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Call the connect method to simulate a connection
        cursor, connection = APIDatabase_Connect.connect_to_database(
            database_name="test_db",
            db_user="test_user",
            db_pass="test_pass",
            host="localhost"
        )

        # Call the close method
        APIDatabase_Connect.close_database_connection(cursor, connection)

        # Verify if cursor.close and connection.close were called
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
