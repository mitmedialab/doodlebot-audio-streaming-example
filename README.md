# Setup & Execution

The `main.py` script includes an example of making a request to the azure speech service to generate audio data. 

Instead of storing the bytes in a wav file, they could instead be streamed to the doodlebot (~line 78). 

First, download the `.env` file a developer should have given you to be located at the root of this repository. 

Then, execute the following:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

This will create an output.wav file containg the generated audio bytes stored in a `.wav`. 