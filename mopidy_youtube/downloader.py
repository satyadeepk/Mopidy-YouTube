import os
import logging
import youtube_dl

def download_if_not_exists(download_dir, youtubeId):
    filepath = download_dir + 'yt_' + youtubeId + '.mp3'
    if not os.path.isfile(filepath):
        command_tokens = [
            'youtube-dl',
            '--extract-audio',
            '--audio-format mp3',
            '--audio-quality 5',
            '--output \'' +  download_dir + 'yt_%(id)s.%(ext)s\'',
            # '--output \'~/Music/%(title)s.%(ext)s\'',
            youtubeId]
        
        command = ' '.join(command_tokens)
        print('Downloading ' + youtubeId)
        print('' + command)
        os.system(command)
        print('Download ' + youtubeId + ' complete.')
    return filepath

def download_uris(download_dir, trackuris):
    for uri in trackuris:
        if uri.startswith('youtube:'):
            youtubeId = uri[len('youtube:'):]
            download_if_not_exists(download_dir, youtubeId)
