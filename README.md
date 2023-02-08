
# Table of Contents

1.  [What is seed-dl?](#orgb5d2b3c)
2.  [Installation](#orgdb86d72)
3.  [Usage](#org9e40ba5)
4.  [Naming conventions](#orgc0f52af)
5.  [Torrent management](#org0f3681d)
6.  [connecting to the seedbox](#org383d9b2)
    1.  [torrent type identifier](#org508799e)
    2.  [initial scanner](#org2d62c73)
    3.  [improve the CLI interface](#org54b7a6a)
    4.  [Daemon/background process](#org9bf4146)
    5.  [Check compatibility in WIN and OSX (only tested on Linux currently)](#orgfbf3f42)



<a id="orgb5d2b3c"></a>

# What is seed-dl?

Seed-dl tries real hard to make using a seedbox convenient. when browsing
torrent sites, I want to choose my .torrent files, run a single command and have
the completed .torrent files on my computer - I don&rsquo;t want to drag and drop into
a seedbox, use some FTP client and remember my login deets. With each run, Seed-dl scans a directory
(default is your download directory), creates a database of the torrents it
finds, and then uploads them to your seedbox. this triggers the download of your
torrents. Seed-dl checks for completed downloads on each run. (**note**, this
requires configuring the seedbox to move torrents to a folder once completed)

after configuring config.yaml, with one run of the command, it can

-   put your .torrent files into your seedbox
-   check if the .torrent files have finished downloading
-   download the resulting files for you, throwing them into a directory by type
    (audio, video, application)

Optionally, seed-dl can

-   scan a directory to work out which torrents exist locally and which ones remotely
    to update the database (add the directories to scan against in the
    config.yaml)


<a id="orgdb86d72"></a>

# Installation

clone the repo, and adapt the `config\_example.yaml` file.


<a id="org9e40ba5"></a>

# Usage

assuming you have python installed, run

    python main.py


<a id="orgc0f52af"></a>

# Naming conventions

torrents are distributed based on a `.torrent` file, which produces a torrent.
confusingly, the name of a torrent and the name of the `.torrent` file are mostly
not the same. `.torrent` files use bencode to store the information about the
torrent it creates. to keep that distinction clear, &ldquo;torrentfile&rdquo; refers to the
torrent files downloaded as a result of adding a `.torrent` file to a torrent client.


<a id="org0f3681d"></a>

# Torrent management

locally, torrents are tracked via the `torrents.json` file. This is to create a
source of truth that can be checked against the seedbox. this will update and
change the status of torrents according to:

-   has the `.torrent` been uploaded to the seedbox?
-   has the torrentfile finished downloading on the server?
-   has the torrentfile finished downloading locally?


<a id="org383d9b2"></a>

# connecting to the seedbox

at the moment, this is designed for the shared seedboxes at seedbox.io. these
only allow you to connect via FTP, there is no shell access and you cannot use
sftp, or rsync, as these would be much better suited to this type of file
transfer. Alas, we must make use of the antiquated FTP system.

the credentials stored in the config file. obviously keep those secrets safe.


<a id="org508799e"></a>

## DONE torrent type identifier

to predict what type of torrent is created, we use the mimetype (.mp3 or .mp4)
or whatever of the largest file in a torrent to predict the nature of the
torrent. this lets us move the finished download into a sensible folder for
later processing.


<a id="org2d62c73"></a>

## TODO initial scanner

scan the seedbox for all torrents and local directories to produce a full
database.


<a id="org54b7a6a"></a>

## TODO improve the CLI interface

different colours. integrate a Verbose mode
to reduce CLI clutter.


<a id="org9bf4146"></a>

## TODO Daemon/background process

One day it would be nice if the whole process was in the background. click and
download a torrent, wait, enjoy it&rsquo;s content!


<a id="orgfbf3f42"></a>

## TODO Check compatibility in WIN and OSX (only tested on Linux currently)

