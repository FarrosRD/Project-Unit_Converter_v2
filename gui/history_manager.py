import os
import json
import customtkinter as ctk
from .components import KeypadButton

class HistoryManager:
    # KONFIGURASI WARNA 
    COLOR_BG = "#000000"
    COLOR_CARD = "#1a1a1a"
    COLOR_ACCENT = "#b14400"
    COLOR_ACCENT_HOVER = "#8a3500"
    COLOR_DELETE = "#ff5555"

    def __init__(self, root, category_font, unit_font):
        self.root = root
        self.category_font = category_font
        self.unit_font = unit_font
        
        self.history_file = "history.json"
        self.history_data = self.load_history()
        self.history_page = None 


    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history_to_file(self):
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.history_data, f, indent=4)
        except Exception as e:
            print(f"Error saving history: {e}")

    def add_to_history(self, input_val, from_u, result_text, to_u, category):
        if input_val == "0": return
        
        entry = {
            "input": input_val,
            "from_unit": from_u,
            "result": result_text,
            "to_unit": to_u,
            "category": category
        }
        self.history_data.insert(0, entry)
        
        if len(self.history_data) > 50:
            self.history_data.pop()
            
        self.save_history_to_file()


    def show_history_page(self):
        self.history_page = ctk.CTkFrame(self.root, fg_color=self.COLOR_BG, corner_radius=0)
        self.history_page.place(x=0, y=0, relwidth=1, relheight=1)

        header = ctk.CTkFrame(self.history_page, fg_color=self.COLOR_BG, height=60)
        header.pack(fill="x", side="top", padx=10, pady=10)

        back_btn = KeypadButton(header, text="←", width=50, command=self.hide_history_page)
        back_btn.pack(side="left")

        ctk.CTkLabel(
            header, text="History", font=self.category_font, text_color="white"
        ).pack(side="left", padx=20)

        self.scroll_frame = ctk.CTkScrollableFrame(self.history_page, fg_color="transparent")
        self.scroll_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.populate_history_list()

        clear_btn = KeypadButton(
            self.history_page, text="Clear All History", height=45, 
            fg_color=self.COLOR_ACCENT, hover_color=self.COLOR_ACCENT_HOVER,
            command=self.clear_all_history
        )
        clear_btn.pack(pady=20, padx=20, fill="x")

    def populate_history_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not self.history_data:
            ctk.CTkLabel(
                self.scroll_frame, text="Your history is empty.", 
                text_color="gray", font=self.unit_font
            ).pack(pady=40)
            return

        for i, item in enumerate(self.history_data):
            card = ctk.CTkFrame(self.scroll_frame, fg_color=self.COLOR_CARD, corner_radius=10)
            card.pack(fill="x", pady=5, padx=5)

            del_btn = ctk.CTkButton(
                card, text="✕", width=30, height=30, 
                fg_color="transparent", text_color=self.COLOR_DELETE, 
                hover_color="#330000", font=("Arial", 12, "bold"),
                command=lambda idx=i: self.delete_single_item(idx)
            )
            del_btn.pack(side="right", padx=10)

            text_frame = ctk.CTkFrame(card, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            ctk.CTkLabel(
                text_frame, text=item.get('category', 'Unknown'), 
                font=("Inter", 11), text_color="gray"
            ).pack(anchor="w")
            
            conv_text = f"{item['input']} {item['from_unit']} =\n{item['result']} {item['to_unit']}"
            ctk.CTkLabel(
                text_frame, text=conv_text, font=("Inter", 15), 
                anchor="w", justify="left"
            ).pack(anchor="w")

    def hide_history_page(self):
        if self.history_page:
            self.history_page.destroy()
            self.history_page = None

    def delete_single_item(self, index):
        if 0 <= index < len(self.history_data):
            del self.history_data[index]
            self.save_history_to_file()
            self.populate_history_list()

    def clear_all_history(self):
        self.history_data = []
        self.save_history_to_file()
        self.populate_history_list()