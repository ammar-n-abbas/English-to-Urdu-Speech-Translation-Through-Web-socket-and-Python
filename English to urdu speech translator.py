import pyaudio
import wave
import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud import LanguageTranslatorV2
from watson_developer_cloud import TextToSpeechV1
from mtranslate import translate
from gtts import gTTS

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "En-Ur(En).wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print ("recording...")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print ("finished recording")

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

speech_to_text = SpeechToTextV1(
    username= "2b4386e1-0f5a-4cdf-8339-84b0f9f604af",
    password= "gqShfpkXp3QE",
    x_watson_learning_opt_out=False
)

with open(join(dirname(__file__), "D:\RCAI\watson\examples\En-Ur(En).wav"),
          'rb') as audio_file:
    English_speech_to_text=speech_to_text.recognize(
        audio_file, content_type='audio/wav', timestamps=True,
        word_confidence=True)
    English_Speech=English_speech_to_text["results"][0]["alternatives"][0]["transcript"]
    print(English_Speech)

def main():

    print(translate(English_Speech, 'ur'))

    tts_1 = translate(English_Speech, 'hi')
    tts = gTTS(tts_1.encode('utf-8', 'ignore'), lang='hi', slow=False)
    tts.save("En-Ur(Ur).mp3")

if __name__ == '__main__':
    main()

import mp3play,time

clip = mp3play.load(r'D:\RCAI\watson\examples\En-Ur(Ur).mp3')
clip.play()
time.sleep(5)
clip.stop()