# ailia AI Voice Python API

!! CAUTION !!
“ailia” IS NOT OPEN SOURCE SOFTWARE (OSS).
As long as user complies with the conditions stated in [License Document](https://ailia.ai/license/), user may use the Software for free of charge, but the Software is basically paid software.

## About ailia AI Voice

ailia AI Voice is a library for speech synthesis using AI. It provides APIs for C# for Unity and for C for native applications. By using ailia AI Voice, it is possible to easily implement AI-based speech synthesis in applications.

ailia AI Voice can perform speech synthesis offline, only on edge devices, without the need for cloud connectivity. It also supports the latest GPT-SoVITS, enabling speech synthesis in any voice timbre.

## Install from pip

You can install the ailia AI Voice free evaluation package with the following command.

```
pip3 install ailia_voice
```

## Install from package

You can install the ailia AI Voice from Package with the following command.

```
python3 bootstrap.py
pip3 install ./
```

## Usage

```python
import ailia_voice

import librosa
import time
import soundfile

import os
import urllib.request

# Load reference audio
ref_text = "水をマレーシアから買わなくてはならない。"
ref_file_path = "reference_audio_girl.wav"
if not os.path.exists(ref_file_path):
	urllib.request.urlretrieve(
		"https://github.com/axinc-ai/ailia-models/raw/refs/heads/master/audio_processing/gpt-sovits/reference_audio_captured_by_ax.wav",
		"reference_audio_girl.wav"
	)
audio_waveform, sampling_rate = librosa.load(ref_file_path, mono=True)

# Infer
voice = ailia_voice.GPTSoVITS()
voice.initialize_model(model_path = "./models/")
voice.set_reference_audio(ref_text, ailia_voice.AILIA_VOICE_G2P_TYPE_GPT_SOVITS_JA, audio_waveform, sampling_rate)
buf, sampling_rate = voice.synthesize_voice("こんにちは。今日はいい天気ですね。", ailia_voice.AILIA_VOICE_G2P_TYPE_GPT_SOVITS_JA)
#buf, sampling_rate = voice.synthesize_voice("Hello world.", ailia_voice.AILIA_VOICE_G2P_TYPE_GPT_SOVITS_EN)

# Save result
soundfile.write("output.wav", buf, sampling_rate)
```

## User dictionary

To load a user dictionary created with pyopenjtalk, give the user_dict_path to initialize_model.

```
voice.initialize_model(model_path = "./models/", user_dict_path = "./userdic.dic")
```

## API specification

https://github.com/axinc-ai/ailia-sdk

