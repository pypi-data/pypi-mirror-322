import requests
from django.conf import settings
import polib
import os
from django.core.management import call_command

def simple_hash_text(text: str) -> str:
    hash1 = 0
    hash2 = 0

    for char in text:
        # get char code
        char_code = ord(char)
        
        # calculate hash1
        hash1 = (hash1 << 5) - hash1 + char_code
        hash1 &= 0xFFFFFFFF  
        
        # calculate hash2
        hash2 = (hash2 << 7) - hash2 + char_code
        hash2 &= 0xFFFFFFFF  # limit to 32 bits

    combined_hash = abs(hash1 + hash2)
    
    return base36_encode(combined_hash)


def base36_encode(number: int) -> str:
    """Convierte un número entero a una cadena en base 36."""
    if number == 0:
        return "0"
    
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = ""
    
    while number > 0:
        number, remainder = divmod(number, 36)
        result = chars[remainder] + result
    
    return result


def get_translations_from_api(data,source_lang, target_lang, route_file):
    url_api = f'http://127.0.0.1:8000/api/general_translations/?source_lang={source_lang}&target_lang={target_lang}'
    
    if route_file:
        url_api += f"&route_file={route_file}"
    
    url_api += '&type_project=django'

    token = settings.TRANSLATEFILES_API_TOKEN

    if token:
        token = f"Token {token}"

    response = requests.post(
        url_api,
        json=data,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': token,
        }
    )
    if response.status_code != 200:
        raise Exception(f"Error al actualizar los datos de traducción: {response.status_code}")
    
    return response.json()

def generate_new_file_po(language,recreate_json,locale_dir):
    new_po = polib.POFile()

    new_po.metadata = {
        'Project-Id-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
        'Language': language,
    }

    for msgid, msgstr in recreate_json.items():
        entry = polib.POEntry(
            msgid=msgid,       # original text
            msgstr=msgstr,     # translation
        )
        new_po.append(entry)

    new_po_file_path = os.path.join(locale_dir, language, 'LC_MESSAGES', 'django.po')
    new_po.save(new_po_file_path)


def make_recreate_json(original_translations,data_result_translations):
    recreate_json = {}
    for key, value in original_translations.items():
        simple_hash = simple_hash_text(key)
        
        if simple_hash in data_result_translations.keys():
            recreate_json[key] = data_result_translations[simple_hash]
            continue
    return recreate_json


def generate_translations(self, target_lang, locale_dir):
    default_language = settings.LANGUAGE_CODE

    # Start
    self.stdout.write(self.style.SUCCESS(f"\n🚀 Starting translation generation for language: {target_lang}"))

    # Paso 1: Generate files .po
    self.stdout.write(self.style.WARNING(f"  Step 1: Generating .po file for '{target_lang}'..."))
    call_command('makemessages', locale=[target_lang], verbosity=0)
    self.stdout.write(self.style.SUCCESS(f"    ✔ .po file generated for '{target_lang}'"))

    # Paso 2: Read File .po
    po_file_path = os.path.join(locale_dir, default_language, 'LC_MESSAGES', 'django.po')
    
    po = polib.pofile(po_file_path)
    self.stdout.write(self.style.SUCCESS(f"    ✔ .po file read successfully (entries: {len(po)}))"))

    translations = {
        simple_hash_text(entry.msgid): entry.msgid
        for entry in po
    }

    original_translations = {entry.msgid: entry.msgstr for entry in po}

    self.stdout.write(self.style.SUCCESS(f"    ✔ Hashed translations generated (total: {len(translations)}))"))

    # Step 2: Get translations from API
    self.stdout.write(self.style.WARNING(f"  Step 2: get translations for '{target_lang}'..."))
    data_result_translations = get_translations_from_api(translations, default_language, target_lang, f"{default_language}-django.po")
    self.stdout.write(self.style.SUCCESS(f"    ✔ Translations get (received: {len(data_result_translations)}))"))

    # Step 5: Recreate translations
    recreate_json = make_recreate_json(original_translations, data_result_translations)

    # Paso 3: Generate new translations file
    self.stdout.write(self.style.WARNING(f"  Step 3: Generating new translations file for '{target_lang}'..."))
    generate_new_file_po(target_lang, recreate_json, locale_dir)
    self.stdout.write(self.style.SUCCESS(f"    ✔ New .po file generated for '{target_lang}'"))

    # Finish
    self.stdout.write(self.style.SUCCESS(f"\n🎉 Successfully completed translation generation for '{target_lang}' ✅\n"))