import flet as ft
from core.api import LixAPI
from core.decrypt import decrypt_url
from utils.validator import extract_video_id

def main(page: ft.Page):
    """
    Mengatur seluruh antarmuka dan interaksi pengguna aplikasi.

    Fungsi ini menyusun tata letak halaman, mendefinisikan elemen visual, 
    serta mengelola transisi data dari input hingga tampilan hasil konversi.

    Args:
        page (ft.Page): Objek halaman Flet yang menjadi kanvas utama aplikasi.
    """
    page.title = "Lixstream Converter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window_height = 700
    page.window_width = 800

    notification_text = ft.Text(visible=False)

    def show_notification(message, color):
        """
        Menampilkan pesan status singkat kepada pengguna.

        Digunakan untuk memberikan konfirmasi keberhasilan atau peringatan
        jika terjadi kendala selama proses berlangsung.

        Args:
            message (str): Pesan yang ingin disampaikan.
            color (str): Warna teks yang merepresentasikan jenis pesan.
        """
        notification_text.value = message
        notification_text.color = color
        notification_text.visible = True
        page.update()

    def convert_click(e):
        """
        Memproses permintaan konversi saat tombol ditekan.

        Melakukan validasi input, berkomunikasi dengan API untuk mengambil
        metadata, dan menampilkan hasil dekripsi beserta informasi video.
        """
        notification_text.visible = False
        result_container.visible = False

        video_id = extract_video_id(video_id_input.value)
        if not video_id:
            show_notification("Input tidak valid. Silakan masukkan ID atau URL yang benar.", ft.Colors.RED_400)
            return
        
        progress_ring.visible = True
        convert_button.disabled = True
        page.update()

        try:
            api = LixAPI()
            metadata = api.get_video_metadata(video_id)

            if not metadata or not metadata.files:
                show_notification("Metadata tidak ditemukan. Periksa kembali ID video.", ft.Colors.ORANGE_400)
                return

            video_info = metadata.files[0]
            encrypted_url = api.get_asset_url(metadata)

            if not encrypted_url:
                show_notification("Gagal mendapatkan alamat URL aset.", ft.Colors.ORANGE_400)
                return
            
            decrypted_url_str = decrypt_url(encrypted_url)

            thumbnail_image.src = video_info.thumbnail
            video_title.value = video_info.display_name
            duration_seconds = video_info.duration
            minutes = duration_seconds // 60
            seconds = duration_seconds % 60
            video_duration.value = f"Durasi: {minutes:02d}:{seconds:02d}"
            result_textfield.value = decrypted_url_str
            
            result_container.visible = True
            show_notification("Konversi berhasil dilakukan!", ft.Colors.GREEN_400)
        except Exception as ex:
            show_notification(f"Terjadi kendala teknis: {ex}", ft.Colors.RED_400)
        finally:
            progress_ring.visible = False
            convert_button.disabled = False
            page.update()

    async def copy_to_clipboard(e):
        """
        Menyimpan hasil URL yang didekripsi ke dalam sistem clipboard.
        """
        await page.clipboard.set(result_textfield.value)
        show_notification("URL berhasil disalin ke papan klip!", ft.Colors.BLUE_400)

    video_id_input = ft.TextField(
        hint_text="Masukkan ID Video atau URL",
        width=450,
        border_radius=ft.border_radius.all(10),
    )

    convert_button = ft.ElevatedButton(
        on_click=convert_click,
        content=ft.Row(
            [
                ft.Icon(ft.Icons.AUTORENEW),
                ft.Text("Konversi"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
    )

    progress_ring = ft.ProgressRing(visible=False)

    thumbnail_image = ft.Image(
        height=180,
        width=320,
        src="",
        fit="cover",
        border_radius=ft.border_radius.all(10),
    )

    video_title = ft.Text(size=16, weight=ft.FontWeight.BOLD)
    video_duration = ft.Text()
    
    result_textfield = ft.TextField(
        read_only=True,
        expand=True,
        border_radius=ft.border_radius.all(10),
        label="Embed URL",
    )

    copy_button = ft.IconButton(
        icon=ft.Icons.COPY,
        on_click=copy_to_clipboard,
    )

    result_container = ft.Row(
        [
            thumbnail_image,
            ft.Column(
                [
                    video_title,
                    video_duration,
                    ft.Row(
                        [result_textfield, copy_button],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=10,
                width=400,
                alignment=ft.MainAxisAlignment.START,
            ),
        ],
        visible=False,
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.START,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    main_content = ft.Column(
        [
            ft.Text("Lixstream URL Converter", size=30),
            ft.Text("Penyimpanan Video Awan yang Aman dan Andal", size=16, color=ft.Colors.GREY_500),
            ft.Container(height=10),
            video_id_input,
            ft.Row(
                [convert_button, progress_ring],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            notification_text,
            result_container,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    footer = ft.Row(
        [ft.Text("Copyright © 2025 Lixbox All Rights Reserved", color=ft.Colors.GREY_600, size=12)],
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(
        ft.Column(
            [
                main_content,
                footer,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)