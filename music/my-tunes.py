from bottle import Bottle, run, template
import os

app = Bottle()  

class Song(object):

    def __init__(self, path, artist, album, song):
        self.path = path
        self.artist = artist
        self.album = album
        self.song = song

class MPlayer(object):

    file_root = '/share/music/'
    songs = []

    def __init__(self):
        self.get_songs(self.file_root)
    
    def get_songs(self, root_dir):
        artists = os.listdir(root_dir)
        
        for artist in artists:
            print(artist)
            everything = os.listdir(root_dir + artist)
            song_names = album_names = []
            for title in everything:
                if os.path.isfile(title):
                    extention = title.split('.')[-1]
                    if extention in ['.mp3', '.m4a']:
                        song_names.append(title)
                    else:
                        print('Unrecognised extention "{}"'.format(extension))
                elif os.path.isdir(title):
                    album_names.append(title)
                else:
                    print('{} not a file or folder apparently.'.format(title))
            self.add_songs(song_names, artist)
            for album in album_names:
                song_names = [
                    title for title in os.listdir('{}{}/{}/'.format(root_dir, artist, album))
                    if os.path.isfile(title)
                ]
                self.add_songs(songs, artist, album)

    def add_songs(self, songs, artist, album='Unknown'):
        file_path = '{}{}/{}{{}}'.format(
            self.file_root,
            artist,
            album + '/' if album != 'Unknown' else '',
        )
        self.songs += [
            Song(file_path.format(title), artist, album, title)
            for title in songs
        ]
                

@app.route('/display/<category>')
def display(category):
    return page_maker('<a href="../display/{0}a">{0}</a>'.format(category))


def page_maker(content):
    page = '''
        <!DOCTYPE html>
        <hmtl>
        <head>
        <title>Music for Speaker</title>
        </head>
        <body>
        {}
        </body>
        </hmtl>
    '''

    return page.format(content) 

@app.route('/')
def greet(name='Stranger'):
    result = ''

    result += ('''
        <h1>This is a Heading</h1>
        <p>This is a paragraph.</p>
    ''')

    return page_maker(result)

film_playing = None

@app.get('/cmds/<key>')
def film_cmd(key):
    global film_playing
    try:
        film_playing[1].stdin.flush()
        film_playing[1].stdin.write(key)
    except Exception as e:
        print 'Failed to send commands to {}. Saw {}'.format(film_playing[0], e)
    if key == 'q':
        print 'Stopped {}'.format(film_playing[0])
        film_playing = None

@app.route('/playing/<film_name>')
def play(film_name):
    global film_playing
    if film_playing is None:
        film_playing = (film_name, subprocess.Popen(
            ['omxplayer', '-o', 'hdmi', '-r', '/share/VIDEO/film/' + film_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True
        ))
        print 'playing {}'.format(film_name)
    page = []
    head = []
    head.append('''
        <title>Now Playing</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js">
        </script>
        <script>
        function send_cmd(key){
            $.get("/cmds/" + key);
        }
        </script>
    ''')
    #Position
    page.append('<p>')
    for key, label in [('i', '|<<'),
                       ('\x1b[B', '<<'),
                       ('\x1b[D', '<'),
                       ('p', 'Play/Pause'), 
                       ('\x1b[C', '>'),
                       ('\xb1[A', '>>'),
                       ('o', '>>|'),]:
        page.append('<button onclick="send_cmd(\'{}\');">{}</button> '.format(key, label))
    page.append('</p><p>')

    #Volume
    for key, label in [('-', 'quieter'),
                       ('+', 'louder'),]:
        page.append('<button onclick="send_cmd(\'{}\');">{}</button> '.format(key, label))
    page.append('</p><p>')

    #Quit
    page.append('<a href="../library"><button type="button" onclick="send_cmd(\'q\');">Quit</button></a></p>')
    
    return page_maker(head, page)



if __name__ == '__main__':

    player = MPlayer()

    run(app, host='0.0.0.0', port=8082)
    
