
# Table of Contents

1.  [What is seed-dl?](#orge4ec9b3)
2.  [Assumptions](#orge0c99ee)
3.  [Installation](#org754f83d)
4.  [Usage](#orgeb88f77)
5.  [Naming conventions](#orgd79d331)
6.  [Torrent management](#org5275634)
7.  [connecting to the seedbox](#org4d5597c)
    1.  [torrent type identifier](#orgb666146)
    2.  [initial scanner](#org3ee9d48)
    3.  [improve the CLI interface](#org158a73b)
    4.  [Daemon/background process](#org1eaa116)
    5.  [Check compatibility in WIN and OSX (only tested on Linux currently)](#orga6e409e)



<a id="orge4ec9b3"></a>

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


<a id="orge0c99ee"></a>

# Assumptions

-   your Seedbox supports FTP
-   your Seedbox can move finished torrents to a directory within itself
    automatically (like RuTorrent, used on seedbox.io)
-   you can run python scripts locally


<a id="org754f83d"></a>

# Installation

clone the repo, and adapt the `config\_example.yaml` file.

then, inside the Seedbox, make sure to set the Path for where finished
downloads go:

> Autotools > Path to Finished Downloads: &ldquo;/home/files/<seedboxusername>/Completed
> Downloads&rdquo;

and

> Operation Type: Move

Now, when a torrent is complete, the data will be moved to the folder, and
seed-dl can detect it!


<a id="orgeb88f77"></a>

# Usage

assuming you have python installed, run

    python main.py

each `.torrent` will be scanned for the largest file in it, that will then
determine where that file will be downloaded to in the `download_dir`. It will
create them as needed.


<a id="orgd79d331"></a>

# Naming conventions

torrents are distributed based on a `.torrent` file, which produces a torrent.
confusingly, the name of a torrent and the name of the `.torrent` file are mostly
not the same. `.torrent` files use bencode to store the information about the
torrent it creates. to keep that distinction clear, &ldquo;torrentfile&rdquo; refers to the
torrent files downloaded as a result of adding a `.torrent` file to a torrent client.


<a id="org5275634"></a>

# Torrent management

locally, torrents are tracked via the `torrents.json` file. This is to create a
source of truth that can be checked against the seedbox. this will update and
change the status of torrents according to:

-   has the `.torrent` been uploaded to the seedbox?
-   has the torrentfile finished downloading on the server?
-   has the torrentfile finished downloading locally?


<a id="org4d5597c"></a>

# connecting to the seedbox

at the moment, this is designed for the shared seedboxes at seedbox.io. these
only allow you to connect via FTP, there is no shell access and you cannot use
sftp, or rsync, as these would be much better suited to this type of file
transfer. Alas, we must make use of the antiquated FTP system.

the credentials stored in the config file. obviously keep those secrets safe.


<a id="orgb666146"></a>

## DONE torrent type identifier

to predict what type of torrent is created, we use the mimetype (.mp3 or .mp4)
or whatever of the largest file in a torrent to predict the nature of the
torrent. this lets us move the finished download into a sensible folder for
later processing.


<a id="org3ee9d48"></a>

## TODO initial scanner

scan the seedbox for all torrents and local directories to produce a full
database.


<a id="org158a73b"></a>

## TODO improve the CLI interface

different colours. integrate a Verbose mode
to reduce CLI clutter.


<a id="org1eaa116"></a>

## TODO Daemon/background process

One day it would be nice if the whole process was in the background. click and
download a torrent, wait, enjoy it&rsquo;s content!


<a id="orga6e409e"></a>

## TODO Check compatibility in WIN and OSX (only tested on Linux currently)

