from __future__ import unicode_literals
import os
import logging
import pykka
import youtube_dl

from mopidy import backend
from mopidy.core import CoreListener

from mopidy_youtube.library import YoutubeLibraryProvider
import downloader

logger = logging.getLogger(__name__)


class YoutubeFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super(YoutubeFrontend, self).__init__()
        self.config = config
        self.core = core      
    
    def tracklist_changed(self):
        download_dir = self.config['youtube']['download_dir']
        logger.info('Frontend: Tracklist changed')
        tracks = self.core.tracklist.get_tracks().get()
        trackuris = []
        # Get unique track uris from the tracklist
        for track in tracks:
            if track.uri not in trackuris:
                trackuris.append(track.uri)

        downloader.download_uris(download_dir, trackuris)

