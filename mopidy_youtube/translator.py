from __future__ import unicode_literals

import subprocess
import sys
import re
import logging
import calendar

import iso8601
import isodate
import dateutil.parser

from mopidy import models

logger = logging.getLogger(__name__)

def to_mopidy_track(youtube_track, addUrl, url=None):
    if youtube_track is None:
        logger.info("No Track Returned")
        return
        
    uri = idToUri(youtube_track['id'])
        
    date = youtube_track['snippet']['publishedAt']
    artist = to_mopidy_artist(youtube_track['snippet']['channelId'], youtube_track['snippet']['channelTitle'])
    
    if addUrl:
        trackUri = url
    else:
        trackUri = uri
    
    return models.Track(
        uri=trackUri,
        name=youtube_track['snippet']['title'],
        artists=[artist],
        album=dummy_mopidy_album(artist, date),
        track_no=0,
        date=isoToUnix(date),
        length=isoToDuration(youtube_track['contentDetails']['duration']),
        bitrate=320)

def to_mopidy_artist(channelId, channelTitle):
    uri = "youtube:channel:%s" % channelId
    
    return models.Artist(uri=uri, name=channelTitle)

def dummy_mopidy_album(artist, date):
    return models.Album(
        uri='',
        name='n/a',
        artists=[artist],
        date=date)

def urlToId(url):
    # http://gdata.youtube.com/feeds/api/videos/Nh2xYpwe4ws
    idgroup = re.search("videos\/(.+)", url)
    if idgroup is None:
        print "Couldn't match URL Regex:%s " % url
        return ""
    return idgroup.group(1)
    
def uriToId(uri):
    uriParts = uri.split(":")
    return uriParts[-1]
    
def urlToUri(url):
    return idToUri(urlToId(url))
    
def idToUri(id):
    return 'youtube:%s' % id
    
def isoToUnix(iso):
    return iso8601.parse_date(iso).strftime("%s")
    
def isoToDuration(iso):
    return int(isodate.parse_duration(iso).total_seconds()) * 1000

def uriToVideo(uri):
    
    id = uriToId(uri);
    
    if not id:
        return [];
    
    url = subprocess.Popen(["youtube-dl", "-g", 'http://www.youtube.com/watch?v=' + id], stdout=subprocess.PIPE)
    flvlocation = url.communicate()[0].strip()

    logger.info('Youtube-dl returned location of VideoID: %s' % id)
    #logger.debug('Youtube-dl returned location of VideoID: ' + id + " URL: " + flvlocation)

    return flvlocation
