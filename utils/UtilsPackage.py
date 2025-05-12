from testrail import TestRail
from utils.db.APIDatabase_Connect import APIDatabase_Connect
from utils.db.Mongodb_API_Connect import Mongodb_API_Connect
from utils.db.Mongodb_SSH_Connect import Mongodb_SSH_Connect
from utils.db.SSHDatabase_Connect import SSHDatabase_Connect
from utils.file_handler.FileReader import FileReader
from utils.file_handler.FileUtilities import FileUtilities
from utils.pyauto.PyautoWinHandler import PyautoWinHandler
from utils.service_api.ServiceAPI import ServiceAPI
from utils.ssh.SSH_Remote_Connect import SSH_Remote_Connect


class UtilsPackage(

    FileReader,
    FileUtilities,
    ServiceAPI,
    SSH_Remote_Connect,
    APIDatabase_Connect,
    SSHDatabase_Connect,
    Mongodb_API_Connect,
    Mongodb_SSH_Connect,
    PyautoWinHandler,
    TestRail

):
    pass
