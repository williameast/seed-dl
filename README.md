- [What is seed-dl?](#orgaa536d2)
- [Assumptions](#org6f7749a)
- [Prerequisites](#org2697009)
- [Installation](#org2a63867)
- [Usage](#orgb7f4a5c)
  - [Default](#org0b486ba)
  - [Optional flags](#org85670fb)
- [If You Want to Help&#x2026;](#org419240d)
  - [Naming Conventions](#org3051a7d)
  - [Torrent Management](#org31da728)
  - [connecting to the seedbox](#org7479b93)
- [To-do list](#org22d6e26)
  - [torrent type identifier](#org752df36)
  - [initial scanner](#org3181782)
  - [improve the CLI interface](#org616d39a)
  - [Daemon/background process](#org7937e74)
  - [Check compatibility in WIN and OSX (only tested on Linux currently)](#orgcd5a34b)
  - [Testing Suite](#org906b85e)



<a id="orgaa536d2"></a>

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


<a id="org6f7749a"></a>

# Assumptions

-   your Seedbox supports FTP
-   your Seedbox can move finished torrents to a directory within itself
    automatically (like RuTorrent, used on seedbox.io)
-   you can run python scripts locally


<a id="org2697009"></a>

# Prerequisites

Seed-dl was developed using Python 3.10.

dependencies need to be installed manually (for now) or use a poetry shell

```toml
python = "^3.10"
pyyaml = "^6.0"
torrentool = "^1.1.1"
bencodepy = "^0.9.5"
```


<a id="org2a63867"></a>

# Installation

clone the repo, and adapt the `config_example.yaml` file.

then, inside the Seedbox, make sure to set the Path for where finished
downloads go (note your seedbox username will be differnt):

> Autotools &gt; Path to Finished Downloads: &ldquo;/home/files/seedboxusername/Completed
> Downloads&rdquo;

and

> Operation Type: Move

Now, when a torrent is complete, the data will be moved to the folder, and
seed-dl can detect it!

You can name the completed download folder whatever you want, it just needs to
match what is in the `config.yaml`.

optionally, if you want to scan directories to ensure you are not downloading duplicate
torrents, just set up those directory paths in the `config.yaml`.


<a id="orgb7f4a5c"></a>

# Usage


<a id="org0b486ba"></a>

## Default

assuming you have python installed, run, from within the cloned directory:

```sh
python main.py
```

this will

-   scan the download directory for new torrents
-   add them to torrents.json
-   load them to the seedbox
-   check which torrents have finished downloading
-   download them, placing them in a folder corresponding to their type.

each `.torrent` will be scanned for the largest file in it, that will then
determine where that file will be downloaded to in the `download_dir`.


<a id="org85670fb"></a>

## Optional flags

```nil
  -h, --help          show this help message and exit
  -u, --upload        upload files to seedbox.io using the credentials in the config
  -p, --print         print files in inbound torrent folder
  -m, --move          move files in inbound folder to outbound torrent folder
  -cs, --checkserver  Check if server has finished downloading
  -d, --download      Download torrents from seedbox.io to the specified folder.
  -l, --list          print torrents currently tracked in the .json.
  -cm, --checklocal   check if files exist locally
  -fl, --flushcache   DEBUG: delete the torrents.json file
```


<a id="org419240d"></a>

# If You Want to Help&#x2026;


<a id="org3051a7d"></a>

## Naming Conventions

torrents are distributed based on a `.torrent` file, which produces a torrent.
confusingly, the name of a torrent and the name of the `.torrent` file are mostly
not the same. `.torrent` files use bencode to store the information about the
torrent it creates. to keep that distinction clear, &ldquo;torrentfile&rdquo; refers to the
torrent files downloaded as a result of adding a `.torrent` file to a torrent client.


<a id="org31da728"></a>

## Torrent Management

locally, torrents are tracked via the `torrents.json` file. This is to create a
source of truth that can be checked against the seedbox. this will update and
change the status of torrents according to:

-   has the `.torrent` been uploaded to the seedbox?
-   has the torrentfile finished downloading on the server?
-   has the torrentfile finished downloading locally?


<a id="org7479b93"></a>

## connecting to the seedbox

at the moment, this is designed for the shared seedboxes at seedbox.io. these
only allow you to connect via FTP, there is no shell access and you cannot use
sftp, or rsync, as these would be much better suited to this type of file
transfer. Alas, we must make use of the antiquated FTP system.

the credentials stored in the config file. obviously keep those secrets safe.


<a id="org22d6e26"></a>

# To-do list


<a id="org752df36"></a>

## torrent type identifier

to predict what type of torrent is created, we use the mimetype (.mp3 or .mp4)
or whatever of the largest file in a torrent to predict the nature of the
torrent. this lets us move the finished download into a sensible folder for
later processing.


<a id="org3181782"></a>

## initial scanner

scan the seedbox for all torrents and local directories to produce a full
database.


<a id="org616d39a"></a>

## improve the CLI interface

different colours. integrate a Verbose mode
to reduce CLI clutter.


<a id="org7937e74"></a>

## Daemon/background process

One day it would be nice if the whole process was in the background. click and
download a torrent, wait, enjoy it&rsquo;s content!


<a id="orgcd5a34b"></a>

## Check compatibility in WIN and OSX (only tested on Linux currently)


<a id="org906b85e"></a>

## Testing Suite

currently no tests are performed. would be better to make sure we can handle
edge cases like non-standard characters etc.

