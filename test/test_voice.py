from src.voice.language_manager import LanguageManager
from src.voice.voice_router import VoiceRouter



def test_language_detection():


    manager = LanguageManager()


    language = manager.detect_language(

        "Hello, I want to buy vegetables"

    )


    assert language == "en"



def test_voice_selection():


    router = VoiceRouter()


    voice = router.select_voice(
        "en"
    )


    assert voice is not None



def test_supported_voice():


    router = VoiceRouter()


    voice = router.select_voice(
        "ta"
    )


    assert (
        "tamil"
        in voice
        or
        voice is not None
    )