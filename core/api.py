import requests
import json
from typing import Optional
from .models import VideoMetadata

class LixAPI:
    """
    Manajer komunikasi untuk mengakses layanan API Lixstreaming.

    Kelas ini menangani permintaan jaringan secara terstruktur untuk mengambil
    informasi video dan alamat aset dari server.
    """

    BASE_URL = "https://api.lixstreamingcaio.com"

    def __init__(self):
        """
        Inisialisasi sesi dengan konfigurasi peramban standar.
        """
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        })

    def get_video_metadata(self, video_id: str) -> Optional[VideoMetadata]:
        """
        Mengambil informasi lengkap video berdasarkan kode identitas.

        Proses ini mengirimkan permintaan ke server untuk mendapatkan data
        metadata yang nantinya akan dikonversi menjadi objek VideoMetadata.

        Args:
            video_id (str): Kode unik video yang akan dicari.

        Returns:
            Optional[VideoMetadata]: Objek data video atau None jika gagal.
        """
        try:
            response = self.session.post(f"{self.BASE_URL}/v2/s/home/resources/{video_id}")
            response.raise_for_status()
            data = response.json()
            if not data.get('files'):
                return None
            return VideoMetadata.from_dict(data)
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Error getting video metadata: {e}")
            return None

    def get_asset_url(self, metadata: VideoMetadata) -> Optional[str]:
        """
        Mendapatkan alamat URL aset terenkripsi dari server.

        Menggunakan informasi dari metadata untuk meminta tautan file yang 
        siap didekripsi untuk kebutuhan pemutaran video.

        Args:
            metadata (VideoMetadata): Objek berisi informasi SUID dan file ID.

        Returns:
            Optional[str]: String URL terenkripsi atau None jika terjadi kendala.
        """
        if not metadata or not metadata.suid or not metadata.files:
            return None
        
        file_id = metadata.files[0].id
        uid = metadata.suid
        
        try:
            response = self.session.get(f'{self.BASE_URL}/v2/s/assets/f?id={file_id}&uid={uid}')
            response.raise_for_status()
            data = response.json()
            return data.get('url')
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Error getting asset URL: {e}")
            return None