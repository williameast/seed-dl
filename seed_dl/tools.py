#!/usr/bin/env python3


def showAllFiles(torrents):
    for torrent in torrents:
        print(torrent["torrentname"])


def showIncompleteFiles(torrents):
    print("Not uploaded to Seedbox:")
    for torrent in torrents:
        if not torrent["torrent_uploaded_to_server"]:
            print("-->",torrent["torrentname"])
    print("---------------------------------------------------------------------")
    print("Not Completed Downloading on Seedbox:")
    for torrent in torrents:
        if not torrent["download_complete_on_server"]:
            print("-->",torrent["torrentname"])
    print("---------------------------------------------------------------------")
    print("Not downloaded from Seedbox:")
    for torrent in torrents:
        if not torrent["download_complete_on_local"]:
            print("-->",torrent["torrentname"])
    print("---------------------------------------------------------------------")
