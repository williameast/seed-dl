import parsed_args
import torrent_management

#!/usr/bin/env python3
if __name__ == "__main__":
    # handle the arguments passed in the command line.
    args = parsed_args.parseArgs()

    # load in the config data
    config = parsed_args.getConfigData()

    # TORRENT_DIR = config["torrent_dir"]
    # TARGET_DIR = config["target_dir"]
    # SEEDBOX_ADDR = config["seedbox_addr"]
    # SEEDBOX_LOGIN = config["seedbox_login"]
    # SEEDBOX_PW = config["seedbox_pw"]
    # SEEDBOX_DL_FOLDER = config["ftp_remote_directory_for_completed_downloads"]

    torrent_management.saveTorrentFilelist()
