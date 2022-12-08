#!/usr/bin/env python3

from dataclasses import dataclass
import os
import json
import bencode

# TODO DEFINITIONS ONLY FOR TESTING PLEASE DELETE

DIRECTORY = '/home/weast/org/projects/Dev/Python/seed_dl_2/seed_dl/seed_dl'
TESTTORRENT =  "/home/weast/org/projects/Dev/Python/seed_dl_2/seed_dl/seed_dl/Omni Trio - The Haunted Science - 1996 (CD - MP3 - 320)-1046102.torrent"
###################################################################
###################################################################
@dataclass
class Torrent:
    # name of the .torrent file.
    filename: str  # the name of the .torrent file
    torrentname: str  # on initiation this is None. later we will create a method to extract the name of the file that the .torrent file generates.
    download_complete_on_server: bool  # on initiation this is False. when the server is queries on the status, it is updated
    download_complete_on_local: bool  # if this is true, then it means that the file is completely finished, i.e. downloaded on server, FTPed into the local dir, no further actions to be done.
    path: str  # this is the composite filepath to the location of the torrent.
    torrentfile: str


def checkMimes(file, allowed_extensions):
    """Check if the file is in the correct extensions list, if not, return False"""
    if os.path.splitext(file)[1] in allowed_extensions:
        file_valid = True
    else:
        file_valid = False
    return file_valid


def printTorrentFileList():
    with open("torrents.json", "r") as f:

        print(json.dumps(f))


def loadTorrentList(torrentlist="torrents.json"):
    try:
        with open(torrentlist, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"ERROR: Could not find file {torrentlist} at location.")


def getTorrentName(filename):
    '''Get the name of a torrent from the corresponding .torrent file.'''
    with open(filename, "rb") as fin:
        torrent = bencode.bdecode(fin.read())
        return torrent["info"]["name"]


def ListTorrents(directory):
    """
    generates a list of torrents - if torrent is file and ends in .torrent,
    add it to list, and uses torrent data form.
    """
    # torrents = loadTorrentList()
    # # not sure if this is enough error handling. I just assume that if loadTorrentList finds nothing then there are not torrents.
    # if torrents is None:
    #     print("found no torrent list. creating a new list.")
    #     torrents = []

    torrents = []

    with os.scandir(directory) as localdir:
        for entry in localdir:
            # check if file is correct type
            if entry.is_file() and checkMimes(entry, ".torrent") and entry not in torrents:
                entry = Torrent(
                    filename=entry.name,
                    torrentname=getTorrentName(entry),
                    download_complete_on_local=False,
                    download_complete_on_server=False,
                    path=entry.path,
                    # torrentfile=entry,
                    torrentfile=None
                )
                torrents.append(entry)

    if len(torrents) == 0:
        print(f"No torrents found in {directory}, aborting.")
        return

    return torrents


def saveTorrentFilelist(torrents, target_dir):
    with open("torrents.json", "w") as f:
        json.dump(torrents, f)
