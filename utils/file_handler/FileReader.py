import logging
import os
import time
import zipfile

import allure
import pytest

log = logging


class FileReader:

    def __init__(self):
        pass

    def read_file(self, filePath, mode='r'):
        """
        Read data from the given file
        """
        log.info("Read the given file  {}".format(filePath))
        with open(filePath, mode) as data_file:
            list_data = data_file.readlines()
        return list_data

    def write_file(self, filePath, listData, mode='w'):
        """
        write given data to the  file
        """
        log.info("Write the given data to this file  {}".format(filePath))
        with open(filePath, mode) as out_data:
            for data in listData:
                out_data.write(data)

    def get_all_files_in_directory_and_subdirectories(self, directory):
        """
        Method to get the list of files from given directory
        """
        files = list()
        result = list()
        for (dirpath, dirnames, filenames) in os.walk(directory):
            files += [os.path.join(dirpath, file) for file in filenames]
        for file in files:
            path = str(file).split('/')
            # the IDE automatically added .gitingore files unwantedly
            if path[path.__len__() - 1].__contains__('.') and path[path.__len__() - 1] != '.gitignore':
                result.append(path[path.__len__() - 1])
        return result
