#!/usr/bin/env python3

from dataclasses import dataclass
import os
import json
import bencodepy
from datetime import datetime
import mimetypes
from pathlib import Path

@dataclass
class Torrent:
    # name of the .torrent file.
    name: str  # the name of the .torrent file
    torrentname: str  # decode the bencode to get the name as the torrent file would be called as it downloads
    download_complete_on_server: bool  # on initiation this is False. when the server is queries on the status, it is updated
    download_complete_on_local: bool  # if this is true, then it means that the file is completely finished, i.e. downloaded on server, FTPed into the local dir, no further actions to be done.
    torrent_uploaded_to_server: bool # if this is true, then .torrent file is in watch folder.
    path: str  # this is the composite filepath to the location of the torrent.
    mimetype: str
    timestamp: datetime


def checktorrentfileDownloadedLocally(torrentfile, location):
    '''
    Check to see if a given torrent has already been added to a given location.
    '''
    return torrentfile in os.listdir(location)

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


def saveTorrentFilelist(torrents, filename="torrents.json"):
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


def localMediaFileCategorizer(category, directory):
    # checks directory if category exists. if not, creates it.
    # TODO needs to handle error if a file is called category but is not a folder.
    filepath = os.path.join(directory, category)
    if not os.path.exists(filepath):
        Path(filepath).mkdir()
        print(f"creating a new category: {category} in {directory}")
    return filepath


    with open(filename, 'rb') as f:
        info = bencodepy.decode(f.read())[b"info"]
        if [b"files"] in info:
            files = info[b"files"]
            for file in files:
                # concatenates the contents of the path list. this gives us the mimetypes independently of
                # how nested the directories is.
                path = file[b"path"]
                name = ""
                for item in path:
                    item = item.decode("utf8")
                    name += item
                size = int(file[b"length"])
                mimetype = mimetypes.guess_type(name)[0]
                filelist.append({"name": name, "size": size, "mimetype": mimetype})
            # take the largest file, split the string to get just the filetype from the mimetype.
            # out = sorted(filelist, key=lambda d: d["size"], reverse=True)[0]["mimetype"].split("/")[0]
            out = sorted(filelist, key=lambda d: d["size"], reverse=True)[0]["mimetype"]
        else:
            out = mimetype.guess_type(info[b"name"]).split("/")[0]




def detectMediaType(filename):
    '''
    Detects the largest files in a torrent just using the .torrent file. this is then used to predict the media type
    of a torrent so that we can shunt it to the correct place in the computer. it can handle nested torrent structures. '''
    filelist = []
    with open(filename, 'rb') as f:
        info = bencodepy.decode(f.read())[b"info"]
        try:
            name = ""
            torrentname = info[b"name"]
            torrentname = torrentname.decode("utf8")
            name += torrentname
            out = mimetypes.guess_type(name)[0]
        except KeyError:
            files = info[b"files"]
            for file in files:
                # concatenates the contents of the path list. this gives us the mimetypes independently of
                # how nested the directories is.
                path = file[b"path"]
                name = ""
                for item in path:
                    item = item.decode("utf8")
                    name += item
                size = int(file[b"length"])
                mimetype = mimetypes.guess_type(name)[0]
                filelist.append({"name": name, "size": size, "mimetype": mimetype})
            # take the largest file, split the string to get just the filetype from the mimetype.
            # out = sorted(filelist, key=lambda d: d["size"], reverse=True)[0]["mimetype"].split("/")[0]
            out = sorted(filelist, key=lambda d: d["size"], reverse=True)[0]["mimetype"]
    if out is None:
        out = "uncategorized"
    else:
        out = out.split("/")[0]
    return out  # returns the mimetype of the largest file in the torrent.

def detect_media_type(file_path):
    """
    Detect the media type of a file based on its file extension.

    Args:
        file_path (str): The path to the file to detect the media type of.

    Returns:
        str: The media type of the file.
    """
    media_types = {
        'audio': ['mp3', 'wav', 'ogg', 'flac'],
        'video': ['mp4', 'mkv', 'avi', 'wmv'],
        'image': ['jpg', 'jpeg', 'png', 'gif'],
        'application': ['exe', 'msi', 'dmg', 'pkg', 'torrent']
    }

    file_ext = file_path.split('.')[-1].lower()
    for media_type, extensions in media_types.items():
        if file_ext in extensions:
            return media_type

    return 'unknown'



def listTorrents(directory,
                 torrentfilelist="torrents.json",
                 appendExisting=True,
                 readOnly=False,
                 printNewTorrents=False):
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
            # print("loaded in existing torrent file list.")
            print("Loaded in existing torrent file list")
            for torrent in torrents:  # prevent duplicate .torrentfiles being uploaded.
                torrentnames.append(torrent["name"])
        except IOError:
            print(f"No torrent list found at {torrentfilelist}, creating a new one.")

    with os.scandir(directory) as localdir:
        for entry in localdir:
            # check if file is correct type
            if entry.is_file() and checkMimes(entry, ".torrent") and entry.name not in torrentnames:
                entry = Torrent(
                    name=entry.name,
                    torrentname=getTorrentName(entry),
                    download_complete_on_local=False,
                    download_complete_on_server=False,
                    torrent_uploaded_to_server=False,
                    path=entry.path,
                    mimetype=detectMediaType(entry),
                    timestamp=datetime.now().isoformat())
                # the use of __dict__ solves my JSON not subscriptable problem but seems
                # like it makes the assignment of the datalcass redundant
                torrents.append(entry.__dict__)
                count += 1
                # torrent_json = vars(entry)

    if count == 0:
        print(f"No new torrents found in {directory}")

    if count > 0:
        if printNewTorrents or readOnly:
            for torrent in torrents:
                print(torrent["name"])
        else:
            print(f"Added {count} torrentfiles in {directory} to the torrent list.")

    return torrents

