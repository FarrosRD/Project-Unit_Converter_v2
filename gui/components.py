import customtkinter as ctk

class KeypadButton(ctk.CTkButton):
    def __init__(self, master, text, command, height=50, corner_radius=10, **kwargs):
        button_font = kwargs.pop("font", ("Inter", 18))
        button_fg = kwargs.pop("fg_color", "#1a1a1a")
        button_hover = kwargs.pop("hover_color", "#333333")
        button_text_color = kwargs.pop("text_color", "white")

        super().__init__(
            master, 
            text=text, 
            command=command, 
            height=height, 
            corner_radius=corner_radius,
            font=button_font,
            fg_color=button_fg,
            hover_color=button_hover,
            text_color=button_text_color,
            **kwargs
        )