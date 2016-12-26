import os
import logging
import youtube_dl

def download_if_not_exists(download_dir, youtubeId):
    filepath = download_dir + youtubeId + '.mp3'
    if not os.path.isfile(filepath):
        command_tokens = [
            'youtube-dl',
            '--extract-audio',
            '--audio-format mp3',
            '--audio-quality 5',
            '--output \'' +  download_dir + '%(id)s.%(ext)s\'',
            # '--output \'~/Music/%(title)s.%(ext)s\'',
            youtubeId]
        
        command = ' '.join(command_tokens)
        print('Downloading ' + youtubeId)
        os.system(command)
    return filepath

def download_uris(download_dir, trackuris):
    for uri in trackuris:
        if uri.startswith('youtube:'):
            youtubeId = uri[len('youtube:'):]
            download_if_not_exists(download_dir, youtubeId)