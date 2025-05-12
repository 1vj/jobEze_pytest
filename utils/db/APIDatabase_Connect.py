import mysql.connector
import logging
log = logging


class APIDatabase_Connect:

    @staticmethod
    def connect_to_database(database_name, db_user, db_pass, host):
        """
        Method to connect the database through API
        """
        log.info("MySQL connection is closed")
        try:
            db_connection = mysql.connector.connect(
                host=host,
                user=db_user,
                password=db_pass,
                database=database_name,
                port=3306
            )
            cursor = db_connection.cursor()
            return [cursor, db_connection]
        except Exception as e:
            log.error("Error while connecting to MySQL", e)

    @staticmethod
    # Perform insert, delete and update operation with mysql query.
    def alter_data_into_db_table(cursor, db_connection, sql_query):
        """
        Method to update the database through API
        :param cursor:
        :param db_connection:
        :param sql_query:
        :return:
        """
        log.info("Altered data mysql query - {}".format(sql_query))
        cursor.execute(sql_query)
        db_connection.commit()

    @staticmethod
    # Fetch single data from database. (Select operation)
    def fetch_single_data_from_table(cursor, sql_query):
        """
        Method to fetch the single row data from db
        """
        cursor.execute(sql_query)
        result = cursor.fetchone()
        return result

    @staticmethod
    # Fetch multiple data from database.
    def fetch_multiple_data_from_table(cursor, sql_query):
        """
        Method to fetch the multiple row data from db
        """
        cursor.execute(sql_query)
        result = cursor.fetchall()
        return result

    @staticmethod
    # Perform Drop, create database operation with this.
    def execute_mysql_query_db(cursor, sql_query):
        """
        Method to execute the sql query
        """
        log.info("Execute mysql query - {}".format(sql_query))
        cursor.execute(sql_query)

    @staticmethod
    # Close connection with database.
    def close_database_connection(cursor, db_connection):
        """
        Method to close the DB connection
        """
        log.info("Closing MySQL connection...")
        cursor.close()
        db_connection.close()
        log.info("MySQL connection is closed")



