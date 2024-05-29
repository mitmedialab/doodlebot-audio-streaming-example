import azure.cognitiveservices.speech as speechsdk
import dotenv
import os
import pyaudio
import wave

dotenv.load_dotenv()

# Set up the subscription info for the Speech Service:
subscription_key = os.environ.get("AZURE_SUBSCRIPTION_KEY")
region = "eastus"

# Set up the Speech Config
speech_config = speechsdk.SpeechConfig(
    subscription=subscription_key, region=region, )

speech_config.speech_synthesis_voice_name = "en-US-AnaNeural"

# Set up the audio output config to stream the audio:
audio_output_stream = speechsdk.audio.PullAudioOutputStream()
audio_output_config = speechsdk.audio.AudioOutputConfig(
    stream=audio_output_stream)

# Create a synthesizer with the given configs


config = {
    "rate": 16000,
    "format": pyaudio.paInt16,
    "channels": 1
}


def synthesize_to_stream(text):
    # Similiar to this example: https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/python/console/speech_synthesis_sample.py#L210

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_output_config)

    # Define a callback function to handle the audio output

    def audio_output_handler(evt: speechsdk.SpeechSynthesisEventArgs):
        print(evt.result.reason)
        if evt.result.audio_data:
            # Attempted to use this callback to continually write to a file,
            # but that results in constant, regular clicking in output file.
            # TODO: Investigate why this is happening
            pass

    # Connect the event handler
    synthesizer.synthesizing.connect(audio_output_handler)

    # Start synthesizing the text, and wait for the result (so this blocks)
    result = synthesizer.speak_text_async(text).get()

    # Check the result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Synthesis completed.")
        del result  # Delete result so we can later delete synthesizer
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
        return

    del synthesizer  # deleting synthesizer closes the stream

    with wave.open("output_audio.wav", "wb") as wf:
        wf.setnchannels(config["channels"])
        wf.setsampwidth(2)  # 2 bytes per sample for 16-bit audio
        wf.setframerate(config["rate"])

        # Pull audio data from the stream and write to file
        buffer = bytes(4096)
        while True:
            size = audio_output_stream.read(buffer)
            if size == 0:
                break
            # send bytes to doodlebot here!
            wf.writeframes(buffer[:size])


synthesize_to_stream("Hello, this is a streamed text-to-speech example.")
