from requests.auth import HTTPDigestAuth
from playsound import playsound
import requests

## -- Your settings here --
TEXT = 'Hey, man, how are you?'
#VOICE = 'Ilona30'      # cs
#VOICE = 'Oldrich30'    # cs
VOICE = 'Tim30'         # en
#VOICE = 'Emma30'       # en
# --

response = requests.get(
    'https://ryzen2.megaword.cz:9998/tts-AZUPP/v4/synth', 
    params={
        'text': TEXT,
        'engine': VOICE,
        'format': 'wav'
    },
    auth=HTTPDigestAuth('reichm','AZUPP-TTSserver')
)

## -- Save the .wav file
if response.status_code == 200:
    with open('test.wav', 'wb') as f:
        f.write(response.content)
        print('Wav file saved.')
else:
    print("Failed to save file. Status code:", response.status_code)

playsound('test.wav')
