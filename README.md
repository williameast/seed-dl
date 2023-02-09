---
author: William East
title: Seed DL workflow
---

# What is seed-dl?

Seed-dl tries real hard to make using a seedbox convenient. when
browsing torrent sites, I want to choose my .torrent files, run a single
command and have the completed .torrent files on my computer - I don\'t
want to drag and drop into a seedbox, use some FTP client and remember
my login deets. With each run, Seed-dl scans a directory (default is
your download directory), creates a database of the torrents it finds,
and then uploads them to your seedbox. this triggers the download of
your torrents. Seed-dl checks for completed downloads on each run.
(**note**, this requires configuring the seedbox to move torrents to a
folder once completed)

after configuring config.yaml, with one run of the command, it can

-   put your .torrent files into your seedbox
-   check if the .torrent files have finished downloading
-   download the resulting files for you, throwing them into a directory
    by type (audio, video, application)

Optionally, seed-dl can

-   scan a directory to work out which torrents exist locally and which
    ones remotely to update the database (add the directories to scan
    against in the config.yaml)

# Assumptions

-   your Seedbox supports FTP
-   your Seedbox can move finished torrents to a directory within itself
    automatically (like RuTorrent, used on seedbox.io)
-   you can run python scripts locally

# Prerequisites

Seed-dl was developed using Python 3.10.

dependencies need to be installed manually (for now) or use a poetry
shell

``` toml
python = "^3.10"
pyyaml = "^6.0"
torrentool = "^1.1.1"
bencodepy = "^0.9.5"
```

# Installation

clone the repo, and adapt the `config_example.yaml` file.

then, inside the Seedbox, make sure to set the Path for where finished
downloads go (note your seedbox username will be differnt):

> Autotools \> Path to Finished Downloads:
> \"/home/files/seedboxusername/Completed Downloads\"

and

> Operation Type: Move

Now, when a torrent is complete, the data will be moved to the folder,
and seed-dl can detect it!

You can name the completed download folder whatever you want, it just
needs to match what is in the `config.yaml`.

optionally, if you want to scan directories to ensure you are not
downloading duplicate torrents, just set up those directory paths in the
`config.yaml`.

# Usage

## Default

assuming you have python installed, run, from within the cloned
directory:

``` {.bash org-language="sh"}
python main.py
```

this will

-   scan the download directory for new torrents
-   add them to torrents.json
-   load them to the seedbox
-   check which torrents have finished downloading
-   download them, placing them in a folder corresponding to their type.

each `.torrent` will be scanned for the largest file in it, that will
then determine where that file will be downloaded to in the
`download_dir`.

## Optional flags

    -h, --help          show this help message and exit
    -u, --upload        upload files to seedbox.io using the credentials in the config
    -p, --print         print files in inbound torrent folder
    -m, --move          move files in inbound folder to outbound torrent folder
    -cs, --checkserver  Check if server has finished downloading
    -d, --download      Download torrents from seedbox.io to the specified folder.
    -l, --list          print torrents currently tracked in the .json.
    -cm, --checklocal   check if files exist locally
    -fl, --flushcache   DEBUG: delete the torrents.json file

# If You Want to Help...

## Naming Conventions

torrents are distributed based on a `.torrent` file, which produces a
torrent. confusingly, the name of a torrent and the name of the
`.torrent` file are mostly not the same. `.torrent` files use bencode to
store the information about the torrent it creates. to keep that
distinction clear, \"torrentfile\" refers to the torrent files
downloaded as a result of adding a `.torrent` file to a torrent client.

## Torrent Management

locally, torrents are tracked via the `torrents.json` file. This is to
create a source of truth that can be checked against the seedbox. this
will update and change the status of torrents according to:

-   has the `.torrent` been uploaded to the seedbox?
-   has the torrentfile finished downloading on the server?
-   has the torrentfile finished downloading locally?

## connecting to the seedbox

at the moment, this is designed for the shared seedboxes at seedbox.io.
these only allow you to connect via FTP, there is no shell access and
you cannot use sftp, or rsync, as these would be much better suited to
this type of file transfer. Alas, we must make use of the antiquated FTP
system.

the credentials stored in the config file. obviously keep those secrets
safe.

# To-do list

## [DONE]{.done .DONE} torrent type identifier {#torrent-type-identifier}

to predict what type of torrent is created, we use the mimetype (.mp3 or
.mp4) or whatever of the largest file in a torrent to predict the nature
of the torrent. this lets us move the finished download into a sensible
folder for later processing.

## [TODO]{.todo .TODO} initial scanner {#initial-scanner}

scan the seedbox for all torrents and local directories to produce a
full database.

## STRT improve the CLI interface

different colours. integrate a Verbose mode to reduce CLI clutter.

## [TODO]{.todo .TODO} Daemon/background process {#daemonbackground-process}

One day it would be nice if the whole process was in the background.
click and download a torrent, wait, enjoy it\'s content!

## [TODO]{.todo .TODO} Check compatibility in WIN and OSX (only tested on Linux currently) {#check-compatibility-in-win-and-osx-only-tested-on-linux-currently}

## [TODO]{.todo .TODO} Testing Suite {#testing-suite}

currently no tests are performed. would be better to make sure we can
handle edge cases like non-standard characters etc.
