import os
import customtkinter as ctk
from PIL import Image
from .components import KeypadButton

class AboutManager:
    # KONFIGURASI TAMPILAN 
    COLOR_BG = "#000000"
    COLOR_CARD = "#1a1a1a"
    LOGO_SIZE = (120, 120)

    def __init__(self, root, category_font, unit_font):
        self.root = root
        self.category_font = category_font
        self.unit_font = unit_font
        self.about_page = None
        
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.logo_path = os.path.join(base_path, "assets", "icons", "logo unesa.png")


    def show_about_page(self):
        self.about_page = ctk.CTkFrame(self.root, fg_color=self.COLOR_BG, corner_radius=0)
        self.about_page.place(x=0, y=0, relwidth=1, relheight=1)

        header = ctk.CTkFrame(self.about_page, fg_color=self.COLOR_BG, height=60)
        header.pack(fill="x", side="top", padx=10, pady=10)

        back_btn = KeypadButton(header, text="←", width=50, command=self.hide_about_page)
        back_btn.pack(side="left")

        ctk.CTkLabel(
            header, text="About", font=self.category_font, text_color="white"
        ).pack(side="left", padx=20)

        content_frame = ctk.CTkFrame(self.about_page, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=20)

        if os.path.exists(self.logo_path):
            try:
                pil_img = Image.open(self.logo_path)
                logo_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=self.LOGO_SIZE)
                ctk.CTkLabel(content_frame, image=logo_img, text="").pack(pady=(10, 10))
            except:
                pass

        card = ctk.CTkFrame(content_frame, fg_color=self.COLOR_CARD, corner_radius=15)
        card.pack(fill="both", expand=True, padx=10, pady=(10, 20))

        self._create_disclaimer_text(card)

        KeypadButton(
            card, text="Continue", command=self.hide_about_page, height=40
        ).pack(pady=(0, 20), padx=40, fill="x")

    def _create_disclaimer_text(self, parent):
        text_box = ctk.CTkTextbox(
            parent, font=("Inter", 12), text_color="white", 
            fg_color="transparent", wrap="word", activate_scrollbars=False
        )
        text_box.pack(expand=True, fill="both", padx=15, pady=15)

        disclaimer_text = (
            "Disclaimer:\n\n"
            "Konteks Proyek:\n"
            "Aplikasi Unit Converter ini dikembangkan dan disusun sebagai Proyek Akhir (Tugas Akhir) "
            "pada mata kuliah Pemrograman Dasar di Universitas Negeri Surabaya (UNESA). "
            "Proyek ini dibuat sebagai bagian dari pemenuhan persyaratan akademik pada Program Studi Data Science.\n\n"
            "Tujuan Pendidikan:\n"
            "Program ini dibuat semata-mata untuk keperluan akademik dan pembelajaran. "
            "Aplikasi ini dikembangkan untuk menunjukkan penerapan konsep dasar pemrograman, "
            "meliputi logika pemrograman, perancangan antarmuka pengguna, serta implementasi fungsi program "
            "sesuai dengan kurikulum perguruan tinggi. "
            "Aplikasi ini tidak ditujukan untuk penggunaan profesional, komersial, maupun penggunaan kritis lainnya.\n\n"
            "© 2025 | Farros RD"
        )
        
        text_box.insert("0.0", disclaimer_text)
        text_box.configure(state="disabled")

    def hide_about_page(self):
        if self.about_page:
            self.about_page.destroy()
            self.about_page = None