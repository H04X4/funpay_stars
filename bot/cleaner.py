import re
import base64

def clean_and_decode(encoded_string):
    cleaned_string = re.sub(r'[^A-Za-z0-9+/=]', '', encoded_string)

    missing_padding = len(cleaned_string) % 4
    if missing_padding:
        cleaned_string += '=' * (4 - missing_padding)

    decoded_bytes = base64.b64decode(cleaned_string)
    removed_headers = decoded_bytes.split(b'\x00\x00\x00\x00')[1]
    if b'\x01' in removed_headers:
        removed_headers = removed_headers.split(b'\x01')[0]
    return removed_headers.decode('utf-8', errors='ignore')