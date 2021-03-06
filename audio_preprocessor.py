import os
import numpy as np
import librosa
import librosa.display
import pandas as pd
import matplotlib.pyplot as plt
import shutil
import sys
import warnings

from tqdm import tqdm

class audio_preprocessor:
    ''' Process audio files and create Mel Spectrogram images '''

    def __init__(self):
        ''' Constructor for this class '''
        # Audio and Mel Spectorgram directories
        self.AUDIO_DATASET_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fma_small')
        self.MEL_SPECTROGRAM_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fma_spectrogram')
        self.MEL_SPECTROGRAM_CACHE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fma_spectrogram_cache')
        self.list_of_all_audio_files = []
        self.__find_audio_files()

    def __find_audio_files(self):
        ''' Find audio files '''

        if not os.path.exists(self.AUDIO_DATASET_DIR):
            print ("Failed to find audio files. Please download dataset")
            return

        for dirpath, subdirs, files in os.walk(self.AUDIO_DATASET_DIR):
            for file in files:
                if file.endswith('.mp3'):
                    self.list_of_all_audio_files.append(os.path.join(dirpath, file))

        print('Found ' + str(len(self.list_of_all_audio_files)) + ' songs')

    def audio_read(self, audio_filepath):
        ''' Read audio wav file and normalize to [-1, 1)  '''
        ''' input_path - input mp3 file '''
        y = None
        sr = None
        audio = None
        nbits = 32

        with warnings.catch_warnings():
            # Ignore warnings when reading audio file using Librosa
            warnings.simplefilter("ignore")
            y, samplerate = librosa.load(audio_filepath)

        if y.dtype == "float32":
            audio = y
        else:
            # change range to [-1,1)
            if y.dtype == "uint8":
                nbits = 8
            elif y.dtype == "int16":
                nbits = 16
            elif y.dtype == "int32":
                nbits = 32
            elif y.dtype == "float64":
                nbits = 64

            audio = y / float(2 ** (nbits - 1))

        # special case of unsigned format
        if y.dtype == "uint8":
            audio = audio - 1.0

        if audio.ndim > 1:
            audio = audio[:, 0]

        return audio, samplerate

    def block_audio(x, blockSize, hopSize, fs):
        """
        Generate blocks from a signal
        Parameters:
        x: Signal (likely, numpy array)
        blockSize: Integer
        hopSize: Integer
        fs: Integer
        returns:
        xb: [[ndarray], ...] of shape (numBlocks x blockSize)
        t: ndarray of shape (NumOfBlocks,)
        """

        # allocate memory
        numBlocks = math.ceil(x.size / hopSize)
        xb = np.zeros([numBlocks, blockSize])
        # compute time stamps
        t = (np.arange(0, numBlocks) * hopSize) / fs
        x = np.concatenate((x, np.zeros(blockSize)), axis=0)
        for n in range(0, numBlocks):
            i_start = n * hopSize
            i_stop = np.min([x.size - 1, i_start + blockSize - 1])
            xb[n][np.arange(0, blockSize)] = x[np.arange(i_start, i_stop + 1)]
        return xb, t

    def make_mel_spect_dir(self):
        ''' Make Mel Spectrogram directory '''
        if not os.path.exists(self.MEL_SPECTROGRAM_DIR):
            os.makedirs(self.MEL_SPECTROGRAM_DIR)
        return

    def del_mel_spect_dir(self):
        ''' Delete previous Mel Spectrogram directory '''
        if os.path.exists(self.MEL_SPECTROGRAM_DIR):
            shutil.rmtree(self.MEL_SPECTROGRAM_DIR)
        return

    def del_mel_spect_cache_dir(self):
        ''' Delete previous Mel Spectrogram directory '''
        if os.path.exists(self.MEL_SPECTROGRAM_CACHE_DIR):
            shutil.rmtree(self.MEL_SPECTROGRAM_CACHE_DIR)
        return

    def make_mel_spect_cache_dir(self):
        ''' Make Mel Spectrogram directory '''
        if not os.path.exists(self.MEL_SPECTROGRAM_CACHE_DIR):
            os.makedirs(self.MEL_SPECTROGRAM_CACHE_DIR)
        return

    def get_mel_spectrogram(self, audio_filepath):
        ''' Get Mel Spectrogram '''
        y, sr = self.audio_read(audio_filepath)
        spect = librosa.feature.melspectrogram(y=y, sr=sr,n_fft=2048, hop_length=512)
        spect = librosa.power_to_db(spect, ref=np.max)
        return spect

    def get_mel_spectrogram_with_cache(self, audio_filepath):
        ''' Load previously saved spectrogram if there is one, if not generate spectrogram and save it as a file reloadable '''
        self.make_mel_spect_cache_dir()
        output_file = os.path.join(self.MEL_SPECTROGRAM_CACHE_DIR, os.path.splitext(os.path.basename(audio_filepath))[0] + '.npy')
        if os.path.exists(output_file):
            return np.load(output_file)
        else:
            spectrogram = self.get_mel_spectrogram(audio_filepath)
            np.save(output_file, spectrogram)
            return spectrogram

    def prepare_mel_spectrogram_image(self, audio_filepath):
        WIDTH = 10
        HEIGHT = 4
        spect = self.get_mel_spectrogram(audio_filepath)
        plt.figure(figsize=(WIDTH, HEIGHT))
        plt.axis('off')
        librosa.display.specshow(spect, y_axis='mel', fmax=20000, x_axis='time')

    def save_mel_spectrogram(self, audio_filepath, output_filepath):
        ''' Save an spectrogram to a file '''
        print ('Saving Mel Spectrogram for ' + os.path.basename(audio_filepath))
        self.prepare_mel_spectrogram_image(audio_filepath)
        self.make_mel_spect_dir()
        plt.savefig(output_filepath)
        plt.close()
        return

    def plot_mel_spectrogram(self, audio_filepath):
        ''' Plot Mel Spectrogram '''
        print ('Showing Mel Spectrogram for ' + os.path.basename(audio_filepath))
        self.prepare_mel_spectrogram_image(audio_filepath)
        plt.show()
        plt.close()
        return

    def find_song_filepath(self, song_id):
        file_name = '{0:06}.mp3'.format(song_id)
        for root, dirs, files in os.walk(self.AUDIO_DATASET_DIR):
            if file_name in files:
                return os.path.join(root, file_name)

if __name__ == '__main__':
    processor = audio_preprocessor()
    for file in tqdm(processor.list_of_all_audio_files):
        output_file = os.path.join(processor.MEL_SPECTROGRAM_DIR, os.path.splitext(os.path.basename(file))[0] + '.png')
        if not os.path.exists(output_file):
            processor.save_mel_spectrogram(file, output_file)

