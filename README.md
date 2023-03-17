# Talk to GPT 3.5 using your voice

The python files in this repository allow to have a conversation with GPT 3.5. 

You can formulate a question using the default microphone of the device you're using. Your question is automatically converted to text using the Azure Speech service and then sent to the OpenAI-Service on Azure. The response from GPT 3.5 is then converted to spoken text also using the Azure Speech service. 

You need to have the following environment variables available:
```
# Azure Speech Service Variables
export SPEECH_KEY=
export SPEECH_REGION=

# Azure OpenAI Variables
export OPENAI_API_KEY=
export OPENAI_ENDPOINT=
```

You could add them to your .bashrc-file for example

## Usage
To start the conversation, enter following command in the root directory of this repo:
```
python conversation.py
````

Then a dialogue is shown, which you can follow:

```
Enter 'start' to start the next question / answer pair or 'exit' to exit the application
start
Starting conversation...

You may now speak into the microphone...
Recognized: So wie geht es dir?

Sending to OpenAI...
Response from OpenAI: 
Ich bin ein Computerprogramm und habe keine Emotionen, aber ich bin bereit, jede Frage oder Diskussion zum Thema generative Künstliche Intelligenz zu führen. Wie kann ich Ihnen helfen?

Now speaking response...
Speech synthesized for text [
Ich bin ein Computerprogramm und habe keine Emotionen, aber ich bin bereit, jede Frage oder Diskussion zum Thema generative Künstliche Intelligenz zu führen. Wie kann ich Ihnen helfen?]
```

## Configuration of GPT 3.5
The GPT 3.5 model is configured to act as an expert on generative AI. You could change this if needed.
