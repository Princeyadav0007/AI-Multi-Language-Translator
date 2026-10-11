"""
Module 4: Voice Translation — Speech-to-Text.
Uses SpeechRecognition with Google's free Web Speech API.
Works with either a live microphone (local machine) or an uploaded
audio file (safer for demos / deployed servers without a mic).
"""
import speech_recognition as sr


def recognize_from_microphone(language="en-US", timeout=5, phrase_time_limit=15):
    """Record from the default microphone and return recognized text."""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # noise handling
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    except (OSError, AttributeError):
        raise RuntimeError(
            "Microphone is not available in this environment. "
            "Live recording only works when the app is run on your own computer "
            "(not on a hosted/cloud server). Please use the 'Upload Audio File' option instead."
        )
    return _recognize(recognizer, audio, language)


def recognize_from_file(file_path, language="en-US"):
    """Recognize speech from an uploaded audio file (wav/aiff/flac)."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.record(source)
    return _recognize(recognizer, audio, language)


def _recognize(recognizer, audio, language):
    try:
        text = recognizer.recognize_google(audio, language=language)
        return text
    except sr.UnknownValueError:
        raise ValueError("Could not understand the audio. Please speak clearly and try again.")
    except sr.RequestError as e:
        raise RuntimeError(f"Speech recognition service error: {e}")
