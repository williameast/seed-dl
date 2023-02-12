#!/usr/bin/env python3

import parsed_args
import torrent_management
import ftp_management
import tools
import os
import sys

if __name__ == "__main__":
    # handle the arguments passed in the command line.
    args = parsed_args.parseArgs()

    # load in the config data
    config = parsed_args.getConfigData()

    TORRENT_DIR = config["torrent_dir"]
    TARGET_DIR = config["target_dir"]
    DL_DIR = config["download_dir"]
    SEEDBOX_ADDR = config["seedbox_addr"]
    SEEDBOX_LOGIN = config["seedbox_login"]
    SEEDBOX_PW = config["seedbox_pw"]
    SEEDBOX_DL_FOLDER = config["ftp_remote_directory_for_completed_downloads"]
    SEEDBOX_WATCH_FOLDER = config["ftp_remote_watch_directory"]
    FILE_DIRECTORIES = config["file_directories"]




    ##############################
    # Arg Switchboard

    if sum(list(vars(args).values())) == 0: # what to do if no arguments are given
        args.upload = True
        args.checkserver = True
        args.download = True
        args.checklocal = True

    ########################################################################

    # if (args.upload or args.move or args.checkserver or args.list or args.print):
    torrents = torrent_management.listTorrents(directory=TARGET_DIR)

    if args.flushcache:
        try:
            os.remove("torrents.json")
            print("file removed.")
            sys.exit()
        except OSError as e:
            print("could not delete file", e.strerror)

    ########################################################################
    if (args.upload or args.download or args.checkserver):
        # This establishes the connection to the seedbox. Instantiates the SeedboxFTP object.
        try:
            sftp = ftp_management.SeedboxFTP(SEEDBOX_ADDR, SEEDBOX_LOGIN, SEEDBOX_PW)
            print(f"Attempting to connect to {SEEDBOX_ADDR}")
            sftp.connect()
            print("Connection established.")
        except Exception as e:
            print(type(e))

    ########################################################################
    if args.list:
        tools.showIncompleteFiles(torrents)

    ########################################################################
    if args.upload:
        # set CWD to Watch folder
        sftp.changeWorkingDirectory(remotePath=SEEDBOX_WATCH_FOLDER)

        # change local path to torrent dir, saving the old one.

        # HACK currently a hack to avoid the Permission Denied errors associated with the upload of the
        # .torrent file. in the future, I want to just use the torrent.path to upload the file.

        current_path = os.getcwd()
        os.chdir(TARGET_DIR)

        # loop through torrent list, and send them to the seedbox. currently, duplicates are auto-rejected.
        # TODO add check to prevent duplicate uploads after reinstantiation
        for torrent in torrents:
            if not torrent["torrent_uploaded_to_server"]:
                sftp.Upload(torrent["name"])
                torrent["torrent_uploaded_to_server"] = True
            if torrent["download_complete_on_server"]:
                torrent["torrent_uploaded_to_server"] = True # change to true if the file is already on the seedbox!

        os.chdir(current_path)


    ########################################################################
    if args.checkserver:
        print("Unfinished downloads in Seedbox:")
        for torrent in torrents:
            if not torrent["download_complete_on_server"]:
                torrent["download_complete_on_server"] = sftp.checkTorrentfileDownloadedRemote(torrent["torrentname"], SEEDBOX_DL_FOLDER)
                print(torrent["torrentname"])
            if torrent["download_complete_on_server"]:
                torrent["torrent_uploaded_to_server"] = True #  change to true  if the torrent is completed download!


    if args.checklocal:
        files = []              # I am sure there is a more elegant way of doing this.
        for location in FILE_DIRECTORIES:
            files = files + (os.listdir(location))

        count = 0
        for torrent in torrents:
            if not torrent["download_complete_on_local"]:
                torrent["download_complete_on_local"] = torrent["torrentname"] in files
                count += 1 # increment
        print(f"found {count} torrents in local directories.")


    ########################################################################
    if args.download:
        sftp.changeWorkingDirectory(SEEDBOX_DL_FOLDER)
        for torrent in torrents:
            if not torrent["download_complete_on_local"] and torrent["download_complete_on_server"]:
                dl_directory = torrent_management.localMediaFileCategorizer(torrent["mimetype"], DL_DIR)
                sftp.downloadRemoteDir(torrent["torrentname"], dl_directory)
                torrent["download_complete_on_local"] = True

    ########################################################################
    if not args.print:
        torrent_management.saveTorrentFilelist(torrents)

    # this checks if an ftp instance was created, and if it does exist, disconnects.
    try:
        sftp.disconnect()
    except NameError:
        pass
