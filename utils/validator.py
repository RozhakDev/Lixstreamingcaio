import re

def extract_video_id(input_str: str) -> str | None:
    """
    Mengambil identitas unik video dari teks atau tautan yang diberikan.

    Fungsi ini secara cerdas memisahkan kode ID dari format URL atau 
    memvalidasi jika input yang dimasukkan sudah berupa kode ID murni.

    Args:
        input_str (str): Teks berupa URL video atau kode ID langsung.

    Returns:
        str | None: String kode ID video jika ditemukan, atau None jika format tidak sesuai.
    """
    match = re.search(r'(?:/v/|/)([a-zA-Z0-9]+)$', input_str)
    if match:
        return match.group(1)
    
    if re.match(r'^[a-zA-Z0-9]+$', input_str):
        return input_str
    
    return None