import kaa.metadata
import shutil
from os import listdir, mkdir

prefix = '/share/music/'


class MFile(object):

    def __init__(self, location):
        self.location = location
        self.suffix = location.split('.')[1]
        self.audiofile = kaa.metadata.parse(location)
        for key in ['title', 'artist', 'album']:
            value = getattr(self.audiofile, key)
            if value is None:
                value = ''
            for char in [':', '\\', '/', u'\xed', u'\xe9', '*', '?', u'\xf6', u'\xe1', u'\u2019']:
                value = value.replace(char, '')
            setattr(
                self,
                key,
                value,
            )
        self.rename()

    def rename(self):
        try:
            mkdir('{}{}'.format(prefix, self.artist))
        except OSError:
            pass
        if self.album:
            try:
                mkdir('{}{}/{}'.format(prefix, self.artist, self.album))
            except OSError:
                pass
        new_location = '{0}{1.artist}/{1.album}/{1.title}.{2}'.format(
            prefix,
            self,
            self.suffix,
        )
        print('{} -> {}'.format(self.location, new_location))
        shutil.move(
            self.location,
            new_location,
        )

def main():
    files = []
    folders = listdir(prefix + 'ipod/')
    for folder in folders:
        file_names = listdir(prefix + 'ipod/' + folder)
        for file_name in file_names:
            files.append(MFile('{}{}/{}/{}'.format(
                prefix,
                'ipod',
                folder,
                file_name,
            )))


if __name__ == '__main__':
    main()
