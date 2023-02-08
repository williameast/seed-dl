#!/usr/bin/env python3
import yaml
import argparse


def parseArgs():
    parser = argparse.ArgumentParser(
        description="This tool finds .torrent files in your download folder\
        and gives the option to move them directly into a shared seedbox via\
        FTP. it also allows for download of that file, as well as moving the\
        .torrent files somewhere convenient after processing."
    )
    # only upload files to seedbox.io,
    parser.add_argument(
        "-u",
        "--upload",
        action="store_true",
        help="upload files to seedbox.io using the\
        credentials in the config",
    )
    parser.add_argument(
        "-p",
        "--print",
        action="store_true",
        help="print files in inbound torrent folder",
    )
    parser.add_argument(
        "-m",
        "--move",
        action="store_true",
        help="move files in inbound folder to outbound torrent folder",
    )  # move torrent files locally
    parser.add_argument(
        "-cs",
        "--checkserver",
        action="store_true",
        help="Check if server has finished downloading",
    )
    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download torrents from seedbox.io to the specified folder.",
    )  # download torrents
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="print torrents currently tracked in the .json.",
    )
    parser.add_argument(
        "-cm",
        "--checklocal",
        action="store_true",
        help="check if files exist locally",
    )  # move torrent files locally
    parser.add_argument(
        "-fl",
        "--flushcache",
        action="store_true",
        help="DEBUG: delete the torrents.json file"
    )
    return parser.parse_args()


def getConfigData(config_file="config.yaml"):
    """Handle the yaml data, load it into the space safely."""
    with open("config.yaml", "r") as config:
        try:
            data = yaml.safe_load(config)
            return data
        except yaml.YAMLError as exc:
            print(exc)
