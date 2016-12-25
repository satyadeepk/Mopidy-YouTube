from __future__ import unicode_literals
import os
import logging
import pykka
import youtube_dl

from mopidy import backend

from mopidy_youtube.library import YoutubeLibraryProvider

logger = logging.getLogger(__name__)


class YoutubeBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(YoutubeBackend, self).__init__()

        self.config = config
        
        self.library = YoutubeLibraryProvider(config, backend=self)
        # self.playback = backend.PlaybackProvider(audio=audio, backend=self)
        self.playback = YouTubePlaybackProvider(audio=audio, backend=self)

        self.uri_schemes = ['youtube']

class YouTubePlaybackProvider(backend.PlaybackProvider):
    def __init__(self, audio, backend):
    	super(YouTubePlaybackProvider, self).__init__(audio=audio, backend=backend)

        self.config = backend.config

    def translate_uri(self, uri):
        if uri.startswith('yt:'):
            uri = uri[len('yt:'):]
        elif uri.startswith('youtube:'):
            uri = uri[len('youtube:'):]

        download_dir = self.config['youtube']['download_dir']
        filepath = download_dir + uri + '.mp3'

        if not os.path.isfile(filepath):
	        command_tokens = [
	            'youtube-dl',
	            '--extract-audio',
	            '--audio-format mp3',
	            '--audio-quality 0',
	            '--output \'' +  download_dir + '%(id)s.%(ext)s\'',
	            # '--output \'~/Music/%(title)s.%(ext)s\'',
	            uri]
	        
	        command = ' '.join(command_tokens)
	        print('Downloading ' + uri)
	        os.system(command)

        fileurl = 'file://' + filepath
        print('Playback ' + fileurl)
        return fileurl
        # ytOpts = {
            
        # }
        # with youtube_dl.YoutubeDL(ytOpts) as ydl:
        #     ytInfo = ydl.extract_info(
        #         url=uri,
        #         download=False
        #     )
        #     print ("extract_info " + ytInfo['id'])
        #     if 'id' in ytInfo:
        #     	filename = 'file:///Users/satyadeep/Music/' + ytInfo['id'] + '.mp3'
        #         print("Youtube Playback: " +  filename)
        #         return filename
        #     else:
        #         return None
