
# Table of Contents

1.  [What is seed-dl?](#orgbba17b4)
2.  [Assumptions](#org3c5d5d4)
3.  [Prerequisites](#orgbfa2ea1)
4.  [Installation](#org7d92c3d)
5.  [Usage](#orgc13f9a9)
    1.  [Default](#orgf95f4a3)
    2.  [Optional flags](#org03d8bc0)
6.  [If You Want to Help&#x2026;](#orgc2f547f)
    1.  [Naming Conventions](#org6ba472c)
    2.  [Torrent Management](#org35281eb)
    3.  [connecting to the seedbox](#orgac4a828)
7.  [To-do list](#org30c4af6)
    1.  [torrent type identifier](#org267c054)
    2.  [initial scanner](#org8797a15)
    3.  [improve the CLI interface](#orgb6d236e)
    4.  [Daemon/background process](#orgadad0b9)
    5.  [Check compatibility in WIN and OSX (only tested on Linux currently)](#org6a8a598)
    6.  [Testing Suite](#org832ecd1)

n


<a id="orgbba17b4"></a>

# What is seed-dl?

Seed-dl tries real hard to make using a seedbox convenient. when browsing
torrent sites, I want to choose my .torrent files, run a single command and have
the completed .torrent files on my computer - I don&rsquo;t want to drag and drop into
a seedbox, use some FTP client and remember my login deets. With each run, seed-dl scans a directory
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


<a id="org3c5d5d4"></a>

# Assumptions

-   your Seedbox supports FTP
-   your Seedbox can move finished torrents to a directory within itself
    automatically (like RuTorrent, used on seedbox.io)
-   you can run python scripts locally


<a id="orgbfa2ea1"></a>

# Prerequisites

Seed-dl was developed using Python 3.10.

dependencies need to be installed manually (for now) or use a poetry shell

    python = "^3.10"
    pyyaml = "^6.0"
    torrentool = "^1.1.1"
    bencodepy = "^0.9.5"


<a id="org7d92c3d"></a>

# Installation

clone the repo, and adapt the `config_example.yaml` file.

then, inside the Seedbox, make sure to set the Path for where finished
downloads go (note your seedbox username will be differnt):

> Autotools > Path to Finished Downloads: &ldquo;/home/files/seedboxusername/Completed
> Downloads&rdquo;

and

> Operation Type: Move

Now, when a torrent is complete, the data will be moved to the folder, and
seed-dl can detect it!

You can name the completed download folder whatever you want, it just needs to
match what is in the `config.yaml`.

optionally, if you want to scan directories to ensure you are not downloading duplicate
torrents, just set up those directory paths in the `config.yaml`.


<a id="orgc13f9a9"></a>

# Usage


<a id="orgf95f4a3"></a>

## Default

assuming you have python installed, run, from within the cloned directory:

    python main.py

this will

-   scan the download directory for new torrents
-   add them to torrents.json
-   load them to the seedbox
-   check which torrents have finished downloading
-   download them, placing them in a folder corresponding to their type.

each `.torrent` will be scanned for the largest file in it, that will then
determine where that file will be downloaded to in the `download_dir`. Note that
this currently does not work for zipped or files in an archive format (because
it&rsquo;s literally just looking at the filename ending, no fancy file header
analysis, as that would require the files themselves and not the `.torrent` file)


<a id="org03d8bc0"></a>

## Optional flags

    -h, --help          show this help message and exit
    -u, --upload        upload files to seedbox.io using the credentials in the config
    -p, --print         print files in inbound torrent folder
    -m, --move          move files in inbound folder to outbound torrent folder
    -cs, --checkserver  Check if server has finished downloading
    -d, --download      Download torrents from seedbox.io to the specified folder.
    -l, --list          print torrents currently tracked in the .json that are not completed.
    -cm, --checklocal   check if files exist locally
    -fl, --flushcache   DEBUG: delete the torrents.json file


<a id="orgc2f547f"></a>

# If You Want to Help&#x2026;


<a id="org6ba472c"></a>

## Naming Conventions

torrents are distributed based on a `.torrent` file, which produces a torrent.
confusingly, the name of a torrent and the name of the `.torrent` file are mostly
not the same. `.torrent` files use bencode to store the information about the
torrent it creates. to keep that distinction clear, &ldquo;torrentfile&rdquo; refers to the
torrent files downloaded as a result of adding a `.torrent` file to a torrent client.


<a id="org35281eb"></a>

## Torrent Management

locally, torrents are tracked via the `torrents.json` file. This is to create a
source of truth that can be checked against the seedbox. this will update and
change the status of torrents according to:

-   has the `.torrent` been uploaded to the seedbox?
-   has the torrentfile finished downloading on the server?
-   has the torrentfile finished downloading locally?


<a id="orgac4a828"></a>

## connecting to the seedbox

at the moment, this is designed for the shared seedboxes at seedbox.io. these
only allow you to connect via FTP, there is no shell access and you cannot use
sftp, or rsync, as these would be much better suited to this type of file
transfer. Alas, we must make use of the antiquated FTP system.

the credentials stored in the config file. obviously keep those secrets safe.


<a id="org30c4af6"></a>

# To-do list


<a id="org267c054"></a>

## torrent type identifier

improve it to cope with archived files (.R#, .tar.gz, .zip)


<a id="org8797a15"></a>

## initial scanner

scan the seedbox for all torrents and local directories to produce a full
database.


<a id="orgb6d236e"></a>

## improve the CLI interface

different colours. integrate a Verbose mode
to reduce CLI clutter.


<a id="orgadad0b9"></a>

## Daemon/background process

One day it would be nice if the whole process was in the background. click and
download a torrent, wait, enjoy it&rsquo;s content!


<a id="org6a8a598"></a>

## Check compatibility in WIN and OSX (only tested on Linux currently)


<a id="org832ecd1"></a>

## Testing Suite

currently no tests are performed. would be better to make sure we can handle
edge cases like non-standard characters etc.

