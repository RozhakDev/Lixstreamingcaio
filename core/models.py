from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class VideoFile:
    """
    Representasi data teknis dari sebuah berkas video.

    Memuat rincian spesifik seperti nama tampilan, ukuran, durasi, dan 
    tautan pratinjau (thumbnail) untuk kebutuhan antarmuka.

    Args:
        display_name (str): Nama judul video yang akan ditampilkan.
        size (int): Ukuran berkas video dalam satuan bita.
        duration (int): Durasi total video dalam satuan detik.
        id (str): Identitas unik berkas di dalam sistem.
        thumbnail (str): Tautan URL menuju gambar pratinjau video.
    """
    display_name: str
    size: int
    duration: int
    id: str
    thumbnail: str
    type: Optional[str] = None
    update_time: Optional[int] = None
    collage_screenshots: Optional[List[str]] = field(default_factory=list)

@dataclass
class VideoMetadata:
    """
    Struktur data lengkap untuk metadata konten video.

    Mengelompokkan identitas sesi (suid) beserta daftar berkas video 
    terkait dan informasi tambahan dari sisi server.

    Args:
        suid (str): Identitas unik sesi atau pengguna.
        files (List[VideoFile]): Daftar objek VideoFile yang tersedia.
    """
    suid: str
    files: List[VideoFile]
    ip_country: Optional[str] = None
    player_theme: Optional[str] = None
    slink: Optional[str] = None
    sid: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'VideoMetadata':
        """
        Mengonversi data kamus (dictionary) menjadi objek VideoMetadata.

        Fungsi ini memudahkan pemrosesan data mentah hasil respons API 
        menjadi struktur objek yang rapi dan terukur.

        Args:
            data (dict): Data mentah dalam format dictionary dari API.

        Returns:
            VideoMetadata: Objek yang telah terisi data secara otomatis.
        """
        files_data = data.get('files', [])
        video_files = [VideoFile(**file_data) for file_data in files_data]
        return cls(
            suid=data.get('suid'),
            files=video_files,
            ip_country=data.get('ip_country'),
            player_theme=data.get('player_theme'),
            slink=data.get('slink'),
            sid=data.get('sid')
        )