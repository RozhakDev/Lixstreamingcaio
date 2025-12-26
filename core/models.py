from dataclasses import dataclass

@dataclass
class VideoMetadata:
    """
    Menyimpan informasi identitas dasar dari sebuah video.

    Kelas ini digunakan untuk mengelola data teknis video seperti ID unik
    dan identitas file dalam sistem.

    Args:
        suid (str): Identitas unik sesi atau pengguna (Short Unique ID).
        file_id (str): Kode unik yang merujuk pada file video tertentu.
    """
    suid: str
    file_id: str

@dataclass
class DecryptedAsset:
    """
    Representasi data aset yang telah berhasil didekripsi.

    Menyediakan akses langsung ke URL konten yang siap untuk digunakan
    atau ditampilkan pada aplikasi.

    Args:
        embed_url (str): Alamat URL sematan untuk memutar atau mengakses aset.
    """
    embed_url: str