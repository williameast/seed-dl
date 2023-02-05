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
    TORRENTFILE_DIR = config["torrentfile_dir"] # location where torrentfiles are put, to check against
    SEEDBOX_ADDR = config["seedbox_addr"]
    SEEDBOX_LOGIN = config["seedbox_login"]
    SEEDBOX_PW = config["seedbox_pw"]
    SEEDBOX_DL_FOLDER = config["ftp_remote_directory_for_completed_downloads"]


    ########################################################################

    # if (args.upload or args.move or args.checkserver or args.list or args.print):
    torrents = torrent_management.listTorrents(directory=TARGET_DIR)

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
        for torrent in torrents:
            print(torrent["name"])

    ########################################################################
    if args.upload:
        # set CWD to Watch folder
        sftp.changeWorkingDirectory(remotePath="watch")

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
                #
        os.chdir(current_path)


    ########################################################################
    if args.checkserver:
        print("Completed Downloads in Seedbox:")
        for torrent in torrents:
            if not torrent["download_complete_on_server"]:
                torrent["download_complete_on_server"] = sftp.checkTorrentfileDownloadedRemote(torrent["torrentname"], SEEDBOX_DL_FOLDER)
                print(torrent["torrentname"])
            if torrent["download_complete_on_server"]:
                torrent["torrent_uploaded_to_server"] = True #  change to true  if the torrent is completed download!

    if args.checklocal:
        local_torrentfiles = os.listdir(TORRENTFILE_DIR)

        for torrent in torrents:
            if not torrent["download_complete_on_local"]:
                # check to see if the file is inside the destination directory already. prevents having to redownload.
                # TODO would be nice if it diffs the file to ensure that a broken transfer file is detected (i.e. smaller filesize on destination)
                 torrent["download_complete_on_local"] = torrent["torrentname"] in local_torrentfiles


    ########################################################################
    if args.download:
        sftp.changeWorkingDirectory(SEEDBOX_DL_FOLDER)
        for torrent in torrents:
            if not torrent["download_complete_on_local"] and torrent["download_complete_on_server"]:
                sftp.downloadRemoteDir(torrent["torrentname"], TARGET_DIR)
                torrent["download_complete_on_local"] = True

    ########################################################################
    if not args.print:
        torrent_management.saveTorrentFilelist(torrents)

    # this checks if an ftp instance was created, and if it does exist, disconnects.
    try:
        sftp.disconnect()
        print("disconnected successfully.")
    except NameError:
        pass
