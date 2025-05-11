from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from google.cloud import texttospeech
import os


class TextToSpeechService:
    @classmethod
    def connect_tts(cls):
        authenticator = IAMAuthenticator(os.getenv("WATSON_TTS_API_KEY"))
        cls.text_to_speech = TextToSpeechV1(
            authenticator=authenticator
        )

        cls.text_to_speech.set_service_url(os.getenv("WATSON_TTS_URL"))

    # def synthesize_text(self, text: str, language: str):
    #     voice = "en-US_AllisonV3Voice" if language == "english" else "ar-AR_OmarVoice"
    #     response = TextToSpeechService.text_to_speech.synthesize(
    #         text, voice=voice, accept='audio/mp3'
    #     ).get_result()
    #     return response.content

    def synthesize_text(self, text: str, language: str):
        if language == "english":
            voice = "en-US_AllisonV3Voice"
            response = TextToSpeechService.text_to_speech.synthesize(
                text, voice=voice, accept='audio/mp3'
            ).get_result()
            return response.content

        elif language == "arabic":
            # Google Text-to-Speech
            client = texttospeech.TextToSpeechClient()
            input_text = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="ar-XA",
                ssml_gender=texttospeech.SsmlVoiceGender.MALE
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            response = client.synthesize_speech(
                input=input_text,
                voice=voice,
                audio_config=audio_config
            )
            return response.audio_content

        else:
            raise ValueError(f"Unsupported language: {language}")
