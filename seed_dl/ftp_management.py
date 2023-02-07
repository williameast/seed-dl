#!/usr/bin/env python3

import ftplib
import os
import re


class SeedboxFTP:
    def __init__(self, hostname, username, password, port=22):
        """Constructor Method"""
        # Set connection object to None (initial value)
        self.connection = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    def connect(self):
        try:
            self.connection = ftplib.FTP(self.hostname, self.username, self.password)
        except Exception as e:
            raise Exception(e)
            print("FTP connection failed.")
        finally:
            print(f"Connected sucessfully to {self.hostname} as {self.username}.")

    def disconnect(self):
        """Close the FTP connection"""
        self.connection.close()
        print(f"Disconnected from {self.hostname} sucessfully.")

    def changeWorkingDirectory(self, remotePath):
        try:
            self.connection.cwd(remotePath)
            # print(f"changed remote directory to {remotePath}")
        except Exception as e:
            raise Exception(e)

    def printWorkingDirectory(self):
        self.connection.dir()

    def nlstSafe(self, directory, stripParentFolder):
        """
        creates a directory tree for all directories and file in directory.
        Note that this replaces the nlst() command in the ftplib, because this
        was not able to parse square brackets, and the ftp server could not handle
        escaped strings, for whatever reason. this function basically mimics nlst()
        option stripParentFolder arg lets you have just the file names, not with their path
        """
        out = []

        if stripParentFolder:
            for i in self.connection.mlsd(directory):
                out.append(i[0])
        else:
            for i in self.connection.mlsd(directory):
                out.append(os.path.join(directory, i[0]))

        return out

    # This is the upload function. Very unstable as it stands, and has no proper error handling.
    # TODO add error handling, conditionally producing the response message only in a verbose mode.
    def Upload(self, localFile):
        fileObject = open(localFile, "rb")
        file2BeSavedAs = localFile
        ftpCommand = "STOR %s" % file2BeSavedAs
        ftpResponseMessage = self.connection.storbinary(ftpCommand, fp=fileObject)
        print(ftpResponseMessage, localFile)
        fileObject.close()

    def checkTorrentfileDownloadedRemote(self, torrentfile, directory):
        try:
            return torrentfile in self.nlstSafe(directory, stripParentFolder=True)
        except ftplib.error_perm as e:
            print(e)
            return False

    def checkTorrentFileDownloadedLocal(self, directoryRemote, directoryLocal, torrentCache):
        '''
        1) establish which torrents in the Server are not in the cache.
        2) establish which torrents in the Server are not in present locally.'''

        remoteTorrentlist = self.nlstSafe(directoryRemote, stripParentFolder=True)
        localTorrentlist = os.listdir(directoryLocal)

        for torrent in remoteTorrentlist:
            if torrent not in localTorrentlist:
                pass
            pass
        pass

    def isFtpDir(self, name, guess_by_extension=True):
        """simply determines if an item listed on the ftp server is a valid directory or not"""

        # if the name has a "." in the fourth or fifth to last position, its probably a file extension
        # this is MUCH faster than trying to set every file to a working directory, and will work 99% of time.
        if guess_by_extension is True:
            if len(name) >= 4:
                if name[-4] == ".":
                    return False

        original_cwd = self.connection.pwd()  # remember the current working directory
        try:
            self.connection.cwd(name)  # try to set directory to new name
            self.connection.cwd(original_cwd)  # set it back to what it was
            return True

        except ftplib.error_perm:
            return False

        except Exception:
            return False

    def makeParentDir(self, fpath):
        """ensures the parent directory of a filepath exists"""
        dirname = os.path.dirname(fpath)
        while not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
                print("created directory {0}".format(dirname))
            except OSError as e:
                print(e)
                self.makeParentDir(dirname)

    def downloadRemoteFile(self, name, dest, overwrite):
        """downloads a single file from an ftp server"""
        self.makeParentDir(dest.lstrip("/"))
        if not os.path.exists(dest) or overwrite is True:
            try:
                with open(dest, "wb") as f:
                    self.connection.retrbinary("RETR {0}".format(name), f.write)
                print("downloaded: {0}".format(dest))
            except FileNotFoundError:
                print("FAILED: {0}".format(dest))
        else:
            print("already exists: {0}".format(dest))

    def fileNameMatchPattern(self, pattern, name):
        """returns True if filename matches the pattern"""
        if pattern is None:
            return True
        else:
            return bool(re.match(pattern, name))

    def cloneRemoteDir(self, name, overwrite, guess_by_extension, pattern):
        """replicates a directory on an ftp server recursively"""

        for item in self.nlstSafe(name, stripParentFolder=False):
            if self.isFtpDir(item, guess_by_extension):
                self.cloneRemoteDir(item, overwrite, guess_by_extension, pattern)
            else:
                if self.fileNameMatchPattern(pattern, name):
                    self.downloadRemoteFile(item, item, overwrite)
                else:
                    pass

    def downloadRemoteDir(
        self,
        path,
        destination,
        pattern=None,
        overwrite=False,
        guess_by_extension=True,
    ):
        path = path.lstrip("/") # TODO adapt to pathlib
        original_directory = (
            os.getcwd()
        )  # remember working directory before function is executed
        os.chdir(destination)  # change working directory to ftp mirror directory

        self.cloneRemoteDir(
            path,
            pattern=pattern,
            overwrite=overwrite,
            guess_by_extension=guess_by_extension,
        )

        os.chdir(
            original_directory
        )  # reset working directory to what it was before function exec

