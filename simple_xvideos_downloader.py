#!/usr/bin/env python3

import argparse
import lxml.html
import math
import multiprocessing
import requests
import os
import sys
import urllib.parse
import uuid

def get_entries(list_file):
    """
    func: retrieve video links from a file
    """
    try:
        with open(list_file, 'r') as f:
            entries = f.read().splitlines()
    except:
        entries = []

    return entries

def get_video(video_link):
    """
    func: get video contents in bytes
    """
    video_content = None

    try:
        req = requests.session()
        s = req.get(video_link)
    except:
        msg = "WARNING: Failed to access the video link: %s." %(video_link)
        print(msg)
    else:
        if s.status_code == 200:
            video_html = lxml.html.fromstring(s.text)
            try:
                video_download_link = video_html.xpath('//div//*[@id="video-player-bg"]//a')[0].values()[0]
            except:
                video_content = None
                msg = "WARNING: Failed to implement XPath query on the video link: %s." %(video_link)
                print(msg)
            else:
                video = req.get(video_download_link, timeout=None)
                video_content = video.content
        else:
            msg = "WARNING: Video URL %s returns non-200 response code: %d." %(video_link, s.status_code)
            print(msg)
            video_content = None

    return video_content

def url_basename(video_link):
    """
    func: retrieve basename of a url
    """
    url_base = os.path.basename(urllib.parse.urlparse(video_link).path)
    return url_base

def write_video(video_filename, video_content):
    """
    func: write video content bytes to a file
    """
    try:
        with open(video_filename, 'wb') as f:
            f.write(video_content)
    except:
        msg = 'WARNING: Failed to write file: %s.' %(video_filename)
        print(msg)

def download(video_link):
    """
    func: download a video clip from a url
    """
    uuid_extension = str(uuid.uuid4())
    video_uri = url_basename(video_link)
    """
    it's possible the uri basenames are the same among
    different urls. filename should be unique in this case
    """
    filename = target_dir+"/"+video_uri+"."+uuid_extension

    print('>>> Downloading %s...' %(video_uri))
    video_content = get_video(video_link)
    if video_content != None:
        write_video(filename, video_content)
        print('>>> %s Downloaded => %s.' %(video_uri, filename))

if __name__ == '__main__':
    """
    initialize vars
    """
    i = 0
    video_list = []

    """
    set up args
    """
    parser = argparse.ArgumentParser(description="Simple XVideos Downloader")
    parser.add_argument("-d", "--targetdir", type=str, required=True, help="target save directory")
    parser.add_argument("-l", "--link", type=str, help="video URL")
    parser.add_argument("-f", "--file", type=str, help="video URL list file")
    parser.add_argument("-w", "--worker", type=int, help="number of download parallel workers (default: 5)")
    args = parser.parse_args()

    target_dir = args.targetdir

    if args.link:
        link = args.link
        video_list.append(link)

    if args.file:
        if os.access(args.file, os.R_OK) != True:
            msg = 'WARNING: %s is not readable.' %(args.file)
            print(msg)
        else:
            video_list.extend(get_entries(args.file))

    if not args.link and not args.file:
        print('error: at least one option -l/-f must be used.')
        sys.exit(2)

    if os.access(target_dir, os.W_OK) != True:
        msg = 'ERROR: %s is not writable.' %(target_dir)
        print(msg)
        sys.exit(2)

    if args.worker:
        workers = args.worker
    else:
        workers = 5

    """
    get all video links from -l/-f and dedup elements
    """
    video_list = list(set(video_list))
    print(video_list)
    msg = '%d video(s) will be downloaded.' %(len(video_list))
    print(msg)

    """
    download workers initialized
    """
    rounds = math.ceil(len(video_list) / workers)
    for n in range(rounds):
        run_list = video_list[i:i+workers]
        i += workers
        msg = '>>> Running Batch [%d]' %(n)
        print(msg)
        with multiprocessing.Pool(processes=workers) as pool:
            pool.map(download, run_list)
            pool.terminate()
            pool.join()
