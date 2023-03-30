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
    speech_config.speech_synthesis_voice_name='de-CH-LeniNeural'

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
    openai.api_version = "2023-03-15-preview"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    print("Sending to OpenAI...")
    
    response = openai.ChatCompletion.create(
        deployment_id="gpt-35", 
        model="gpt-3.5-turbo", 
        messages=[
          {"role": "system", "content": "Du bist ein Experte für generative AI und nimmst an einer Podiumsdisskusion teil. Gib kurze Antworten."},
          {"role": "user", "content": text}
        ],
        max_tokens=120,)

    print("Response from OpenAI: " + response.choices[0].message.content)
    print()

    # if the response does not end with an ., ! or ?, remove everything after the last ., ! or ? and add a .
    if not response.choices[0].message.content.endswith("!") and not response.choices[0].message.content.endswith("?") and not response.choices[0].message.content.endswith("."):
        answer_split = response.choices[0].message.content.rsplit(".", 1)[0]

        answer = answer_split[0:len(answer_split)-2] + "."
    else:
        answer = response.choices[0].message.content
    return answer


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