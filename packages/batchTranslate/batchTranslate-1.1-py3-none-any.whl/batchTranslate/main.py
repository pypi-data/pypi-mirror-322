from deep_translator import GoogleTranslator
import random

def translate(times,original):
    languages =list(GoogleTranslator().get_supported_languages(as_dict=True).values())
    lines=original.split('\n')
    translated_lines=[]
    for i in range(times):
        translated_lines=[]
        random.shuffle(languages)
        for line in lines:
            translator=GoogleTranslator(source='auto', target=languages[0])
            translated_line=translator.translate(line)
            translated_lines.append(translated_line)
        if i==times-1:
            translated_lines=[]
            for line in lines:
                translator=GoogleTranslator(source='auto', target="en")
                translated_line=translator.translate(line)
                translated_lines.append(translated_line)
            translated_text = '\n'.join(translated_lines)
            return translated_text