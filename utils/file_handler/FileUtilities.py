import os
import shutil
import logging

log = logging


class FileUtilities:

    def __init__(self):
        pass

    @staticmethod
    def get_cwd():
        current_dir = os.getcwd()
        log.info("Get the current working directory")
        return current_dir

    @staticmethod
    def delete_file_if_present_on_path(file_path):
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                log.error("Error while deleting file ", file_path)
                raise Exception("Error while deleting file ", file_path)
        else:
            log.info("Can not delete the file as it doesn't exists")

    @staticmethod
    def delete_file_in_dir(download_folder):
        for filename in os.listdir(download_folder):
            file_path = os.path.join(download_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                log.error('Failed to delete %s. Reason: %s' % (file_path, e))

    @staticmethod
    def join_path(basePath, *paths):
        log.info("Method to construct the path with given folders")
        return os.path.join(basePath, *paths)

    @staticmethod
    def get_realPath():
        log.info("Method to get the real path")
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def get_dirName():
        log.info("Method to get the directory name")
        return os.path.dirname(os.path.dirname(__file__))


# if __name__ == '__main__':
#     fu = FileUtilities()
#     jpath = fu.join_path(fu.get_cwd(), "currentFolder", "sample.txt")
#     print(jpath)
#     print(fu.get_realPath())
#     print(fu.get_dirName())
