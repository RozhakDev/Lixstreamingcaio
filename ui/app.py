import flet as ft
from core.api import LixAPI
from core.decrypt import decrypt_url
from utils.validator import extract_video_id

def main(page: ft.Page):
    """
    Mengatur tampilan dan logika utama antarmuka pengguna.

    Fungsi ini membangun struktur visual aplikasi, menangani input pengguna, 
    dan menghubungkan elemen UI dengan logika dekripsi video.

    Args:
        page (ft.Page): Objek halaman Flet yang menjadi wadah utama aplikasi.
    """
    page.title = "Lixstream Converter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    notification_text = ft.Text(visible=False)

    def show_notification(message, color):
        """
        Menampilkan pesan pemberitahuan kepada pengguna.

        Digunakan untuk memberikan umpan balik visual terkait status proses
        atau pesan kesalahan yang terjadi.

        Args:
            message (str): Teks pesan yang ingin disampaikan.
            color (str): Warna teks untuk menunjukkan kategori pesan.
        """
        notification_text.value = message
        notification_text.color = color
        notification_text.visible = True
        page.update()

    def convert_click(e):
        """
        Menangani peristiwa klik pada tombol konversi.

        Fungsi ini menjalankan seluruh alur kerja aplikasi, mulai dari validasi 
        input, pengambilan metadata, hingga proses dekripsi URL.
        """
        notification_text.visible = False

        video_id = extract_video_id(video_id_input.value)
        if not video_id:
            show_notification("Invalid input. Please enter a valid video ID or URL.", ft.Colors.RED_400)
            return
        
        progress_ring.visible = True
        convert_button.disabled = True
        page.update()

        try:
            api = LixAPI()
            metadata = api.get_video_metadata(video_id)

            if not metadata:
                show_notification("Failed to get video metadata. Please check the ID.", ft.Colors.ORANGE_400)
                return
            
            encrypted_url = api.get_asset_url(metadata)

            if not encrypted_url:
                show_notification("Failed to get asset URL.", ft.Colors.ORANGE_400)
                return
            
            decrypted_url_str = decrypt_url(encrypted_url)
            result_textfield.value = decrypted_url_str
            result_textfield.visible = True
            copy_button.visible = True

            show_notification("Successfully converted!", ft.Colors.GREEN_400)
        except Exception as ex:
            show_notification(f"An error occurred: {ex}", ft.Colors.RED_400)
        finally:
            progress_ring.visible = False
            convert_button.disabled = False
            page.update()

    async def copy_to_clipboard(e):
        """
        Menyalin hasil dekripsi URL ke papan klip perangkat.
        """
        await page.clipboard.set(result_textfield.value)
        show_notification("Copied to clipboard!", ft.Colors.BLUE_400)

    video_id_input = ft.TextField(
        hint_text="Enter Video ID or URL",
        width=400,
        border_radius=ft.border_radius.all(10),
    )

    convert_button = ft.ElevatedButton(
        on_click=convert_click,
        content=ft.Row(
            [
                ft.Icon(ft.Icons.AUTORENEW),
                ft.Text("Convert"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
    )

    progress_ring = ft.ProgressRing(visible=False)

    result_textfield = ft.TextField(
        read_only=True,
        visible=False,
        width=400,
        border_radius=ft.border_radius.all(10),
    )

    copy_button = ft.IconButton(
        icon=ft.Icons.COPY,
        on_click=copy_to_clipboard,
        visible=False,
    )

    page.add(
        ft.Column(
            [
                ft.Text("Lixstream URL Converter", size=30),
                video_id_input,
                ft.Row(
                    [
                        convert_button,
                        progress_ring,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                notification_text,
                ft.Row(
                    [
                        result_textfield,
                        copy_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)