import ssl

import paramiko
import pymongo
from pymongo import MongoClient
import logging

from sshtunnel import SSHTunnelForwarder, BaseSSHTunnelForwarderError

log = logging


class Mongodb_SSH_Connect:

    @staticmethod
    def connect_mongo_db_ssh(host_ip, ssh_username, ssh_password):
        """
        Method to connect mongo db using hostName, key certificate and ca certificate file.
        """
        log.info("Method to connect mongo db using hostName, key certificate and ca certificate file")
        try:
            server = SSHTunnelForwarder(
                host_ip,
                ssh_username=ssh_username,
                ssh_password=ssh_password,
                remote_bind_address=('127.0.0.1', 27017),
            )
            server.start()
            server._check_is_started()

            client = MongoClient(
                host='127.0.0.1',
                port=server.local_bind_port
                # ssl=True,
                # ssl_certfile=key_certFile,
                # ssl_cert_reqs=ssl.CERT_REQUIRED,
                # ssl_ca_certs=ca_certFile
            )
            # --sslAllowInvalidHostnames
            return client
        except paramiko.ssh_exception.AuthenticationException:
            log.error('Could not open connection to gateway')
            raise paramiko.ssh_exception.AuthenticationException("Could not open connection to gateway")
        except (BaseSSHTunnelForwarderError, ValueError, AssertionError, TypeError):
            log.error('Failed to make ssh connection, ssh username and password are incorrect')
            raise BaseSSHTunnelForwarderError('Failed to make ssh connection, ssh username and password are incorrect')
        except pymongo.err.InternalError:
            log.error("failed to establish database connection, invalid credentials")
            raise pymongo.err.InternalError("failed to establish database connection, invalid credentials")
        except Exception as e:
            log.error('Failed to establish database connection- Exception occurred: %s', format(e))
            raise Exception('Failed to establish database connection- Exception occurred: %s', format(e))

