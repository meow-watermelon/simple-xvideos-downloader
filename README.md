# simple-xvideos-downloader

**Intro**

simple-xvideos-downloader is a small tool to download video clips from XVideos.

**Usage**

```
usage: simple_xvideos_downloader.py [-h] -d TARGETDIR -l LINK [-f FILE]
                                    [-w WORKER]

Simple XVideos Downloader

optional arguments:
  -h, --help            show this help message and exit
  -d TARGETDIR, --targetdir TARGETDIR
                        target save directory
  -l LINK, --link LINK  video URL
  -f FILE, --file FILE  video URL list file
  -w WORKER, --worker WORKER
                        number of download parallel workers (default: 5)

```

*-d*: target directory to save downloaded video clips.

*-l*: full url link of a video url.

*-f*: filename which contains video urls. separated by newline.

*-w*: number of download workers. the default number is 5.

**Notes**
* This tool is parsing the video URL to retrieve the content access URL then download the video clip. In this case, XVideos would restrict the download speed which is **slower** than logged-in user download from the *Download* function.

**Change Log**

**20190126**: initial commit

**20190126**: typo fix
