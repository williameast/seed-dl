#!/usr/bin/env python3

from dataclasses import dataclass
import os
import json
import bencodepy
from datetime import datetime


# TODO DEFINITIONS ONLY FOR TESTING PLEASE DELETE

DIRECTORY = '/home/weast/org/projects/Dev/Python/seed_dl_2/seed_dl/seed_dl'
TESTTORRENT =  "/home/weast/org/projects/Dev/Python/seed_dl_2/seed_dl/seed_dl/Omni Trio - The Haunted Science - 1996 (CD - MP3 - 320)-1046102.torrent"
###################################################################
###################################################################



@dataclass
class Torrent:
    # name of the .torrent file.
    name: str  # the name of the .torrent file
    torrentname: str  # decode the bencode to get the name as the torrent file would be called as it downloads
    download_complete_on_server: bool  # on initiation this is False. when the server is queries on the status, it is updated
    download_complete_on_local: bool  # if this is true, then it means that the file is completely finished, i.e. downloaded on server, FTPed into the local dir, no further actions to be done.
    path: str  # this is the composite filepath to the location of the torrent.
    timestamp: datetime


def checkMimes(file, allowed_extensions):
    """Check if the file is in the correct extensions list, if not, return False"""
    if os.path.splitext(file)[1] in allowed_extensions:
        file_valid = True
    else:
        file_valid = False
    return file_valid


def getTorrentName(filename):
    '''
    Get the name of a torrent from the corresponding .torrent file.
    The dependency of bencode has produced some complications. currently the drop in
    bencodepy replacement reads the dict as bytes. that is why the conversion happens.
    '''
    with open(filename, "rb") as f:
        torrent = bencodepy.decode(f.read())[b"info"][b"name"]
        return torrent.decode("utf8")


def saveTorrentFilelist(torrents, filename):
    '''
    Save torrent file at location with filename.
    '''
    with open(filename, 'w', encoding = "utf8") as f:
        json.dump(torrents, f, indent=4)


def loadTorrentFilelist(filename):
    '''
    Load torrent file at location filename.
    '''
    with open(filename, 'r', encoding = "utf8") as f:
        out = json.load(f)
    return out


def ListTorrents(directory, torrentfilelist="torrents.json", appendExisting=True):
    """
    generates a list of torrents - if torrent is file and ends in .torrent,
    add it to list, and uses torrent data form.
    """

    count = 0  # counts how many torrent files we find
    torrentnames = []
    torrents = []

    if appendExisting:
        try:
            torrents = loadTorrentFilelist(torrentfilelist)
            print("loaded in existing torrent file list.")
            for torrent in torrents: # hacky way to prevent duplicate .torrentfiles being uploaded. FIXME
                torrentnames.append(torrent["name"])
        except IOError:
            print(f"No torrent cache list found at {torrentfilelist}, creating a new one.")


    with os.scandir(directory) as localdir:
        for entry in localdir:
            # check if file is correct type
            if entry.is_file() and checkMimes(entry, ".torrent") and entry.name not in torrentnames:
                entry = Torrent(
                    name=entry.name,
                    torrentname=getTorrentName(entry),
                    download_complete_on_local=False,
                    download_complete_on_server=False,
                    path=entry.path,
                    timestamp=datetime.now().isoformat())
                # the use of __dict__ solves my JSON not subscriptable problem but seems
                # like it makes the assignment of the datalcass redundant
                torrents.append(entry.__dict__)
                count += 1


    if len(torrents) == 0:
        print(f"No torrents found in {directory}, aborting.")
        return

    if count == 0:
        print("No new torrents found!")
    else:
        print(f"Added {count} torrentfiles in {directory} to the torrent list.")

    saveTorrentFilelist(torrents, torrentfilelist)

    return torrents
