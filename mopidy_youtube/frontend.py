from __future__ import unicode_literals
import os
import logging
import pykka
import youtube_dl

from mopidy import backend
from mopidy.core import CoreListener


from mopidy_youtube.library import YoutubeLibraryProvider

logger = logging.getLogger(__name__)


class YoutubeFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super(YoutubeFrontend, self).__init__()
        self.config = config
        self.core = core      
    
    def tracklist_changed(self):
        logger.info('Frontend: Tracklist changed')
        tracks = self.core.tracklist.get_tracks().get()
        for track in tracks:
        	logger.info("track " + track.uri)
