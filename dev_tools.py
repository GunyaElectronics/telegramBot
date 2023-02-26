import moviepy.editor as mp


class MyAudioExtractor:
    def __init__(self, file_in, file_result=None):
        self.file_in = file_in
        if file_result is None:
            self.file_result = file_in.replace('.mp4', '.mp3')

    def convert_to_mp3(self):
        try:
            video = mp.VideoFileClip(self.file)
            print(f'The input file is {self.file}. Try convert to the {self.file_result}')
            video.audio.write_audiofile(self.file_result)
        except FileExistsError:
            print('File already exist')
