#!/usr/bin/env python3

import parsed_args
import torrent_management
import ftp_management
import os

if __name__ == "__main__":
    # handle the arguments passed in the command line.
    args = parsed_args.parseArgs()

    # load in the config data
    config = parsed_args.getConfigData()

    TORRENT_DIR = config["torrent_dir"]
    TARGET_DIR = config["target_dir"]
    SEEDBOX_ADDR = config["seedbox_addr"]
    SEEDBOX_LOGIN = config["seedbox_login"]
    SEEDBOX_PW = config["seedbox_pw"]
    SEEDBOX_DL_FOLDER = config["ftp_remote_directory_for_completed_downloads"]
    ########################################################################
    ########################################################################
    ########################################################################

    # if (args.upload or args.move or args.checkserver or args.list or args.print):
    torrents = torrent_management.listTorrents(directory=TARGET_DIR)

    if (args.upload or args.download or args.checkserver):
        # This establishes the connection to the seedbox.
        sftp = ftp_management.SeedboxFTP(SEEDBOX_ADDR, SEEDBOX_LOGIN, SEEDBOX_PW)
        print(f"Attempting to connect to {SEEDBOX_ADDR}")
        sftp.connect()
        print("Connection established.")

    if args.list:
        for torrent in torrents:
            print(torrent["name"])

    if args.upload:
        # set CWD to Watch folder
        sftp.changeWorkingDirectory(remotePath="watch")

        # change local path to torrent dir, saving the old one.

        # TODO currently a hack to avoid the Permission Denied errors associated with the upload of the
        # .torrent file. in the future, I want to just use the torrent.path to upload the file.

        current_path = os.getcwd()
        os.chdir(TARGET_DIR)

        # loop through torrent list, and send them to the seedbox
        for torrent in torrents:
            if not (torrent["torrent_uploaded_to_server"] or torrent["download_complete_on_server"]):
                sftp.Upload(torrent["name"])
                torrent["torrent_uploaded_to_server"] = True

    if args.checkserver:
        for torrent in torrents:
            if not torrent["download_complete_on_server"]:
                torrent["download_complete_on_server"] = sftp.checkTorrentfileDownloaded(torrent["torrentname"], SEEDBOX_DL_FOLDER)
                print(torrent["torrentname"])

    if args.download:
        sftp.changeWorkingDirectory(SEEDBOX_DL_FOLDER)
        for torrent in torrents:
            if not torrent["download_complete_on_local"] and torrent["download_complete_on_server"]:
                sftp.downloadRemoteDir(torrent["torrentname"], TARGET_DIR)

    if not args.print:
        torrent_management.saveTorrentFilelist(torrents)


    # this checks if an ftp instance was created, and if it does exist, disconnects.
    try:
        sftp.disconnect()
        print("disconnected successfully.")
    except NameError:
        pass
