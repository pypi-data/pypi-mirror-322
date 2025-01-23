from deep_translator import GoogleTranslator
import random

def translate(times, original):
    languages = list(GoogleTranslator().get_supported_languages(as_dict=True).values())
    translated = original
    for i in range(times):
        random.shuffle(languages)  # Shuffle the list of supported languages
        translator = GoogleTranslator(source='en', target=languages[0])  # Random target language
        translated = translator.translate(translated)
        if i == times - 1:
            translator = GoogleTranslator(source='auto', target='en')  # Final translation to English
            translated = translator.translate(translated)
    
    return translated  # Return the final result outside of the loop
