import requests
from .models import VideoMetadata

class LixAPI:
    """
    Penghubung utama untuk berinteraksi dengan layanan LixStreaming.

    Kelas ini mengelola sesi koneksi dan menyediakan metode terstruktur 
    untuk mengambil data video dari server API.
    """
    BASE_URL = "https://api.lixstreamingcaio.com/v2/s"

    def __init__(self):
        """
        Menyiapkan sesi komunikasi dengan konfigurasi header yang sesuai.
        """
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        })

    def get_video_metadata(self, video_id: str) -> VideoMetadata | None:
        """
        Mengambil informasi dasar video dari server berdasarkan ID.

        Proses ini mengumpulkan data teknis yang diperlukan seperti SUID 
        dan ID file untuk kebutuhan pemrosesan selanjutnya.

        Args:
            video_id (str): Identitas unik video yang ingin dicari.

        Returns:
            VideoMetadata | None: Objek metadata video atau None jika tidak ditemukan.
        """
        try:
            response = self.session.post(f"{self.BASE_URL}/home/resources/{video_id}")
            response.raise_for_status()
            data = response.json()

            if "suid" in data and "files" in data and data["files"]:
                return VideoMetadata(suid=data["suid"], file_id=data["files"][0]["id"])
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error getting video metadata: {e}")
            return None
        
    def get_asset_url(self, metadata: VideoMetadata) -> str | None:
        """
        Mendapatkan alamat URL aset yang masih terproteksi.

        Fungsi ini meminta URL enkripsi dari server menggunakan metadata 
        yang telah dikumpulkan sebelumnya.

        Args:
            metadata (VideoMetadata): Objek metadata yang berisi informasi sesi dan file.

        Returns:
            str | None: String URL terenkripsi atau None jika terjadi kendala.
        """
        try:
            response = self.session.get(f"{self.BASE_URL}/assets/f?id={metadata.file_id}&uid={metadata.suid}")
            response.raise_for_status()
            data = response.json()

            if "url" in data:
                return data["url"]
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error getting asset URL: {e}")
            return None