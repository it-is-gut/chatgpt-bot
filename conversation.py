import os
import azure.cognitiveservices.speech as speechsdk
import openai

# function to generate text from speech
def speech_to_text():
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language="de-CH"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("You may now speak into the microphone...")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        print()
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    

# function to generate speech from text
def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='de-CH-JanNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Get the text from openAI and synthesize it
    print("Now speaking response...")
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

# function to send generated text to openAI
def send_to_openAI(text):
    openai.api_type = "azure"
    openai.api_base = os.getenv("OPENAI_ENDPOINT") 
    openai.api_version = "2022-12-01"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    print("Sending to OpenAI...")

    response = openai.Completion.create(
    engine="gpt-35",
    prompt="<|im_start|>system\nThe system participates in a open discussion round regarding generative AI.\n<|im_end|>\n<|im_start|>user\n" + text + "\n<|im_end|>\n<|im_start|>assistant",
    temperature=1,
    max_tokens=50,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["<|im_end|>"])

    print("Response from OpenAI: " + response.choices[0].text)
    print()

    # if the response does not end with an ., ! or ?, remove everything after the last ., ! or ? and add a .
    if not response.choices[0].text.endswith("!") and not response.choices[0].text.endswith("?") and not response.choices[0].text.endswith("."):
        response.choices[0].text = response.choices[0].text.rsplit(".", 1)[0] + "."

    return response.choices[0].text


# main function
def main():
    while True:
        print()
        print("Enter 'start' to start the next question / answer pair or 'exit' to exit the application")
        start = input()

        if start == "start":
            print("Starting conversation...")
            print()
            
            # get text from speech
            text = speech_to_text()
            # send text to openAI
            response = send_to_openAI(text)
    
            # generate speech from response
            text_to_speech(response)
        elif start == "exit":
            print("Exiting application...")
            break

# entry point for the application
if __name__=="__main__":
    main()