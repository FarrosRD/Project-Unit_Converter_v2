import os
import customtkinter as ctk
from PIL import Image

from .components import KeypadButton
from .history_manager import HistoryManager
from .about_manager import AboutManager

from logic.area_logic import convert_area
from logic.data_logic import convert_data
from logic.length_logic import convert_length
from logic.mass_logic import convert_mass
from logic.speed_logic import convert_speed
from logic.temperature_logic import convert_temperature
from logic.currency_logic import convert_currency
from logic.currency_data import CURRENCY_INFO

class UnitConverterApp:
    # KONFIGURASI TAMPILAN 
    COLOR_BG = "#000000"
    COLOR_BTN_HOVER = "#1a1a1a"
    COLOR_DROPDOWN_FG = "#1a1a1a"
    COLOR_DROPDOWN_HOVER = "#333333"
    COLOR_TEXT_WHITE = "white"
    COLOR_TEXT_GRAY = "gray"
    COLOR_ACCENT_ORANGE = "#b14400"
    
    WINDOW_SIZE = "400x600"
    ICON_SIZE = (24, 24)

    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        self.display_value = "0"
        self.sidebar_visible = False
        self.active_input = "main"
        self.current_category = "Length"
        self.currency_info = CURRENCY_INFO
        
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.icon_path = os.path.join(base_dir, "assets", "icons")
        
        self.init_fonts()
        self.init_managers()
        
        self.create_header()
        self.create_display()
        self.create_keypad()
        self.create_sidebar()
        
        self.select_category("Length")

    def setup_window(self):
        self.root.title("Converter")
        self.root.geometry(self.WINDOW_SIZE)
        self.root.resizable(False, False)
        self.root.configure(fg_color=self.COLOR_BG)

    def init_fonts(self):
        """Mencoba load font Inter, fallback ke Segoe UI jika gagal."""
        families = ["Inter", "Segoe UI"]
        for family in families:
            try:
                self.fonts = {
                    "display_bold": (family, 48, "bold"),
                    "display_normal": (family, 48),
                    "unit": (family, 16),
                    "category": (family, 20, "bold"),
                    "button": (family, 18),
                    "button_bold": (family, 18, "bold"),
                    "small": (family, 13)
                }
                break
            except:
                continue

    def init_managers(self):
        self.history_mgr = HistoryManager(self.root, self.fonts["category"], self.fonts["unit"])
        self.about_mgr = AboutManager(self.root, self.fonts["category"], self.fonts["unit"])

    
    # UI 

    def create_header(self):
        self.header_frame = ctk.CTkFrame(self.root, height=60, corner_radius=0, fg_color=self.COLOR_BG)
        self.header_frame.pack(fill="x", side="top")

        # Tombol Menu 
        self.menu_button = KeypadButton(self.header_frame, text="☰", command=self.toggle_sidebar, width=50)
        self.menu_button.pack(side="left", padx=(10, 5), pady=10)

        # Label Kategori 
        self.category_display_label = ctk.CTkLabel(
            self.header_frame, text="Length", font=self.fonts["category"], text_color=self.COLOR_TEXT_WHITE
        )
        self.category_display_label.pack(side="left", padx=10)

        # Tombol History 
        self.history_button = KeypadButton(self.header_frame, text="🕒", command=self.history_mgr.show_history_page, width=50)
        self.history_button.pack(side="right", padx=10, pady=10)

    def create_display(self):
        self.display_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.display_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Input Atas 
        self.number_label = ctk.CTkLabel(
            self.display_frame, text=self.display_value, font=self.fonts["display_bold"], anchor="e"
        )
        self.number_label.pack(fill="x", padx=20, pady=(10, 0))
        self.number_label.bind("<Button-1>", lambda e: self.switch_active_input("main"))

        self.unit_dropdown = self._create_dropdown(self.display_frame)
        
        # Input Bawah 
        self.result_label = ctk.CTkLabel(
            self.display_frame, text="0", font=self.fonts["display_normal"], anchor="e"
        )
        self.result_label.pack(fill="x", padx=20, pady=(10, 0))
        self.result_label.bind("<Button-1>", lambda e: self.switch_active_input("result"))

        self.result_unit_dropdown = self._create_dropdown(self.display_frame)

    def _create_dropdown(self, parent):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=20)
        
        dropdown = ctk.CTkOptionMenu(
            container, values=[" "], font=self.fonts["unit"],
            fg_color=self.COLOR_BG, button_color=self.COLOR_BG, 
            button_hover_color=self.COLOR_BTN_HOVER,
            text_color=self.COLOR_TEXT_GRAY, dropdown_text_color=self.COLOR_TEXT_WHITE,
            dropdown_fg_color=self.COLOR_DROPDOWN_FG, dropdown_hover_color=self.COLOR_DROPDOWN_HOVER,
            anchor="e", dynamic_resizing=True,
            command=self.on_unit_change, width=300
        )
        dropdown.pack(side="right")
        return dropdown

    def create_keypad(self):
        self.keypad_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.COLOR_BG)
        self.keypad_frame.pack(fill="x", side="bottom")
        
        for c in range(4):
            self.keypad_frame.grid_columnconfigure(c, weight=1, uniform="col")
        
        self.update_keypad_layout()

    def update_keypad_layout(self):
        for widget in self.keypad_frame.winfo_children():
            widget.destroy()

        pad = 6
        # Tombol Angka
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('0', 3, 0), (',', 3, 1)
        ]

        for text, r, c in buttons:
            KeypadButton(
                self.keypad_frame, text=text, 
                command=lambda t=text: self.append_to_display(t)
            ).grid(row=r, column=c, padx=pad, pady=pad, sticky="nsew")

        # Tombol (+/-)
        if self.current_category == "Temperature":
            KeypadButton(
                self.keypad_frame, text="+/-", command=self.toggle_sign
            ).grid(row=3, column=2, padx=pad, pady=pad, sticky="nsew")

        # Tombol Aksi 
        KeypadButton(
            self.keypad_frame, text="AC", command=self.clear_display, 
            font=self.fonts["button_bold"], text_color=self.COLOR_ACCENT_ORANGE
        ).grid(row=0, column=3, rowspan=2, padx=pad, pady=pad, sticky="nsew")

        KeypadButton(
            self.keypad_frame, text="⌫", command=self.backspace
        ).grid(row=2, column=3, rowspan=2, padx=pad, pady=pad, sticky="nsew")

        # Tombol Save
        KeypadButton(
            self.keypad_frame, text="Save", command=self.on_enter_pressed, 
            font=self.fonts["button_bold"]
        ).grid(row=4, column=0, columnspan=4, padx=pad, pady=(10, 20), sticky="nsew")

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self.root, width=280, height=600, corner_radius=0)
        self.sidebar_frame.place(x=-280, y=60)
        
        categories = ["Currency", "Length", "Mass", "Speed", "Temperature", "Area", "Data"]
        
        for cat in categories:
            KeypadButton(
                self.sidebar_frame, text=f"  {cat}", width=260,
                command=lambda c=cat: self.select_category(c),
                image=self.load_icon(cat), compound="left", anchor="w"
            ).pack(pady=5, padx=10)
        
        # About 
        about_icon = self.load_icon("info")
        KeypadButton(
            self.sidebar_frame, text="  About", width=260, height=35,
            font=self.fonts["small"], command=self.about_mgr.show_about_page,
            image=about_icon, compound="left", fg_color="transparent", anchor="w"
        ).pack(side="bottom", pady=20, padx=10)

    
    # LOGIC 

    def calculate_conversion(self):
        try:
            val = float(self.display_value)
            
            if self.active_input == "main":
                from_u, to_u = self.unit_dropdown.get(), self.result_unit_dropdown.get()
            else:
                from_u, to_u = self.result_unit_dropdown.get(), self.unit_dropdown.get()

            converters = {
                "Area": convert_area, "Data": convert_data, "Length": convert_length,
                "Mass": convert_mass, "Speed": convert_speed, "Temperature": convert_temperature,
                "Currency": convert_currency
            }
            
            func = converters.get(self.current_category)
            res = func(val, from_u, to_u) if func else 0.0

            formatted_res = str(int(res)) if res == int(res) else f"{res:.4f}".rstrip('0').rstrip('.')
            
            prefix = ""
            if self.current_category == "Currency":
                target_str = self.result_unit_dropdown.get() if self.active_input == "main" else self.unit_dropdown.get()
                code = target_str.split(" - ")[0]
                prefix = self.currency_info.get(code, {}).get("symbol", "") + " "
            
            final_text = f"{prefix}{formatted_res.replace('.', ',')}"

            if self.active_input == "main":
                self.result_label.configure(text=final_text)
            else:
                self.number_label.configure(text=final_text)

        except:
            if self.active_input == "main":
                self.result_label.configure(text="0")
            else:
                self.number_label.configure(text="0")

    def append_to_display(self, value):
        if value == ",":
            if "." in self.display_value: return
            self.display_value += "."
        else:
            if self.display_value == "0":
                self.display_value = value
            else:
                self.display_value += value
        
        self.update_display()

    def select_category(self, category):
        self.current_category = category
        self.category_display_label.configure(text=category)
        
        unit_map = {
            "Currency": sorted([f"{k} - {v['label']}" for k, v in self.currency_info.items()]),
            "Area": ["Square Meter", "Square Kilometer", "Square Centimeter", "Hectare", "Acre", "Square Mile"],
            "Data": ["Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte"],
            "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Foot", "Inch"],
            "Mass": ["Gram", "Kilogram", "Milligram", "Metric Ton", "Pound", "Ounce"],
            "Speed": ["Meters per second", "Kilometers per hour", "Miles per hour", "Knot"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"]
        }
        
        units = unit_map.get(category, ["Unit A", "Unit B"])
        
        self.unit_dropdown.configure(values=units)
        self.unit_dropdown.set(units[0])
        self.result_unit_dropdown.configure(values=units)
        self.result_unit_dropdown.set(units[1] if len(units) > 1 else units[0])
        
        self.update_keypad_layout()
        self.clear_display()
        if self.sidebar_visible: self.toggle_sidebar()

    def update_display(self):
        display_text = self.display_value.replace(".", ",")
        prefix = ""
        
        if self.current_category == "Currency":
            curr_code = self.unit_dropdown.get().split(" - ")[0] if self.active_input == "main" else self.result_unit_dropdown.get().split(" - ")[0]
            prefix = self.currency_info.get(curr_code, {}).get("symbol", "") + " "
            
        if self.active_input == "main":
            self.number_label.configure(text=f"{prefix}{display_text}")
        else:
            self.result_label.configure(text=f"{prefix}{display_text}")
            
        self.calculate_conversion()

    def toggle_sidebar(self):
        new_x = 0 if not self.sidebar_visible else -280
        self.sidebar_frame.place(x=new_x, y=60)
        if not self.sidebar_visible: self.sidebar_frame.lift()
        self.sidebar_visible = not self.sidebar_visible

    def switch_active_input(self, target):
        self.active_input = target
        self.display_value = "0"
        
        is_main = (target == "main")
        self.number_label.configure(font=self.fonts["display_bold"] if is_main else self.fonts["display_normal"])
        self.result_label.configure(font=self.fonts["display_bold"] if not is_main else self.fonts["display_normal"])

    def load_icon(self, name):
        try:
            filename = "info.png" if name == "info" else f"{name.lower()}.png"
            p = os.path.join(self.icon_path, filename)
            img = Image.open(p)
            return ctk.CTkImage(light_image=img, dark_image=img, size=self.ICON_SIZE)
        except:
            return None


    def clear_display(self):
        self.display_value = "0"
        self.update_display()

    def backspace(self):
        self.display_value = self.display_value[:-1] if len(self.display_value) > 1 else "0"
        if self.display_value == "-": self.display_value = "0"
        self.update_display()

    def toggle_sign(self):
        if self.display_value != "0":
            self.display_value = self.display_value[1:] if self.display_value.startswith("-") else "-" + self.display_value
            self.update_display()

    def on_unit_change(self, _):
        self.calculate_conversion()

    def on_enter_pressed(self):
        self.calculate_conversion()
        self.history_mgr.add_to_history(
            self.display_value, self.unit_dropdown.get(),
            self.result_label.cget("text"), self.result_unit_dropdown.get(),
            self.current_category
        )