#!/usr/bin/env python3

import parsed_args
import torrent_management
import ftp_management

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

    if (args.upload or args.move or args.list or args.print):
        torrents = torrent_management.listTorrents(directory=TARGET_DIR)

    if (args.upload or args.download or args.checkserver):
        # This establishes the connection to the seedbox.
        sftp = ftp_management.SeedboxFTP(SEEDBOX_ADDR, SEEDBOX_LOGIN, SEEDBOX_PW)
        print(f"Attempting to connect to {SEEDBOX_ADDR}")
        sftp.connect()
        print("Connection established.")

    if args.upload:
        # set CWD to Watch folder
        sftp.changeWorkingDirectory(remotePath="watch")

        # loop through torrent list, and send them to the seedbox
        for torrent in torrents:
            if not torrent["torrent_uploaded_to_server"]:
                sftp.Upload(torrent["path"])
                torrent["torrent_uploaded_to_server"] = True

    if args.checkserver:
        for torrent in torrents:
            if torrent["download_complete_on_server"]:
                ftp_management.checkTorrentFileDownloaded()
