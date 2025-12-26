import flet as ft
from ui.app import main as app_main

def main():
    """
    Memulai jalannya aplikasi utama secara keseluruhan.

    Fungsi ini berfungsi sebagai pintu masuk (entry point) untuk menjalankan
    antarmuka pengguna menggunakan framework Flet.
    """
    ft.run(app_main)

if __name__ == "__main__":
    main()