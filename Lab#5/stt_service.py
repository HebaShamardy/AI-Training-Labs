import os
import yaml
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from google.cloud import speech_v1p1beta1 as speech



class SpeechToTextService:
    @classmethod
    def connect_stt(cls):
        authenticator = IAMAuthenticator(os.getenv("WATSON_STT_API_KEY"))
        cls.speech_to_text = SpeechToTextV1(
            authenticator=authenticator
        )

        cls.speech_to_text.set_service_url(os.getenv("WATSON_STT_URL"))


    def transcribe_audio(self, language: str, audio_data: bytes, config: object):
        provider = config.get("stt", {}).get(language, {}).get("provider")
        print("provider ", provider)
        if provider == 'watson':
            result = SpeechToTextService.speech_to_text.recognize(audio=audio_data, content_type='audio/wav', model="en-US").get_result()
            print("STT result ", result)
            return result['results'][0]['alternatives'][0]['transcript']

        elif provider == 'google':
            client = speech.SpeechClient()
            audio = speech.RecognitionAudio(content=audio_data)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                language_code="ar-SA"
            )
            response = client.recognize(config=config, audio=audio)
            return response.results[0].alternatives[0].transcript

