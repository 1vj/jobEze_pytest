import time
import logging
import paramiko
import pymysql
from config.TestConfig import TestConfig
from sshtunnel import SSHTunnelForwarder, BaseSSHTunnelForwarderError

log = logging


class SSHDatabase_Connect:

    @staticmethod
    def connect_to_database(database, host_ip, ssh_username, ssh_password):
        """
        Method to connect database through SSH connect
        """
        time.sleep(10)
        try:
            # SSHTunnelForwarder is used to remotely access the server securely
            server = SSHTunnelForwarder(
                host_ip,
                ssh_username=ssh_username,
                ssh_password=ssh_password,
                remote_bind_address=('127.0.0.1', 3306),
            )
            server.start()
            server._check_is_started()
            db = pymysql.connect(
                host='127.0.0.1',
                port=server.local_bind_port,
                user=TestConfig.mc_db_user,
                password=TestConfig.mc_db_pass,
                db=database,
                max_allowed_packet=67108864,
                charset='utf8'
            )
            server_database_array = [server, db]
            return server_database_array
        except paramiko.ssh_exception.AuthenticationException:
            log.error('Could not open connection to gateway')
            raise paramiko.ssh_exception.AuthenticationException("Could not open connection to gateway")
        except (BaseSSHTunnelForwarderError, ValueError, AssertionError, TypeError):
            log.error('[ERROR]Failed to make ssh connection, ssh username and password are incorrect')
            raise BaseSSHTunnelForwarderError('Failed to make ssh connection, ssh username and password are incorrect')
        except pymysql.err.InternalError:
            log.error("failed to establish database connection, invalid credentials")
            raise pymysql.err.InternalError("failed to establish database connection, invalid credentials")
        except Exception as e:
            log.error('Failed to establish database connection- Exception occurred: %s', format(e))
            raise Exception('Failed to establish database connection- Exception occurred: %s', format(e))

    @staticmethod
    def connect_to_database_remote(db_name, jump_ip, jump_username, jump_password, remote_ip, remote_key):
        """
        Method to connect db through SSH(jump server)
        """
        time.sleep(10)
        try:
            # SSHTunnelForwarder is used to remotely access the server securely
            tunnel = SSHTunnelForwarder(
                (jump_ip, 22),
                ssh_pkey=remote_key,
                ssh_username=jump_username,
                ssh_password=jump_password,
                remote_bind_address=(remote_ip, 3306),
            )
            tunnel.start()
            tunnel._check_is_started()
            db = pymysql.connect(
                host='127.0.0.1',
                port=tunnel.local_bind_port,
                user=TestConfig.az_db_user,
                password=TestConfig.az_db_pass,
                db=db_name,
                charset='utf8'
            )
            server_database_array = [tunnel, db]
            return server_database_array
        except paramiko.ssh_exception.AuthenticationException:
            log.error('Could not open connection to gateway')
            raise paramiko.ssh_exception.AuthenticationException("Could not open connection to gateway")
        except (BaseSSHTunnelForwarderError, ValueError, AssertionError, TypeError):
            log.error('[ERROR]Failed to make ssh connection, ssh username and password are incorrect')
            raise BaseSSHTunnelForwarderError('Failed to make ssh connection, ssh username and password are incorrect')
        except pymysql.err.InternalError:
            log.error("failed to establish database connection, invalid credentials")
            raise pymysql.err.InternalError("failed to establish database connection, invalid credentials")
        except Exception as e:
            log.error('Failed to establish database connection- Exception occurred: %s', format(e))
            raise Exception('Failed to establish database connection- Exception occurred: %s', format(e))


    @staticmethod
    def fetch_single_data_from_database(db, query):
        """
        Method to execute the db query to fetch the first data
        """
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            log.info("Get value from database is %s", row)
            return row

    @staticmethod
    def fetch_multiple_data_from_database(db, query):
        """
        Method to execute the db query to fetch the Multiple row of data
        """
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        log.info("Get multiple value from database %s", rows)
        return rows

    @staticmethod
    def close_database_connection(db, server):
        """
        Method to close the DB connection
        """
        try:
            db.close()
            server.close()
            log.info('[INFO]Closing Connection to database')
        except Exception as e:
            log.error('[ERROR]Unable to close database connection')
            raise Exception('Unable to close database connection - ', e)
