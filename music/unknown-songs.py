import os
import re
import shutil
from itertools import count


unknown_no = count(0)
def unknown(path, name):
    new = '{}/unknown_{}{}'.format(path, unknown_no.next(), name)
    shutil.move(
        '{}/{}'.format(path, name),
        new,
    )
    print('changed {} to {}'.format(name, new))
    
for artist in os.listdir('/share/music/'):
    no_space = re.sub(' +', '-', artist)
    if no_space != artist:
        shutil.move(
            '/share/music/{}'.format(artist),
            '/share/music/{}'.format(no_space)
        )
        artist= no_space
    path = '/share/music/{}'.format(artist)
    for songOrAlbum in os.listdir(path):
        no_space = re.sub(' +', '-', songOrAlbum)
        if no_space != songOrAlbum:
            shutil.move(
                '{}/{}'.format(path, songOrAlbum),
                '{}/{}'.format(path, no_space)
            )
            print('{} changed {} to {}'.format(path, songOrAlbum, no_space))
            songOrAlbum = no_space
        if songOrAlbum[0] == '.':
            unknown(path, songOrAlbum)

        path_1 = '{}/{}'.format(path, songOrAlbum)
        if os.path.isdir(path_1):
            for song in os.listdir(path_1):
                no_space = re.sub(' +', '-', song)
                if no_space != song:
                    shutil.move(
                        '{}/{}'.format(path_1, song),
                        '{}/{}'.format(path_1, no_space)
                    )
                    song= no_space
                if song[0] == '.':
                    unknown(path_1, song)
            


