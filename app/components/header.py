import customtkinter as ctk
from utils.theme import Colors, Fonts, Dimensions

class Header(ctk.CTkFrame):
    def __init__(self, parent, title="", icon_back=None, on_back=None, action_icon=None, on_action=None, **kwargs):
        super().__init__(parent, fg_color="transparent", height=Dimensions.HEADER_HEIGHT, **kwargs)
        
        self.grid_propagate(False) # Mantém altura fixa
        
        # Botão Voltar (Esquerda)
        if icon_back and on_back:
            self.btn_back = ctk.CTkButton(
                self,
                text="",
                image=icon_back,
                width=40,
                height=40,
                fg_color="transparent",
                hover_color=Colors.SURFACE_HOVER,
                command=on_back,
            )
            self.btn_back.pack(side="left")
            
        # Título (Centro - usando place para garantir centralização absoluta)
        if title:
            self.lbl_title = ctk.CTkLabel(
                self,
                text=title,
                font=Fonts.TITLE,
                text_color=Colors.TEXT_PRIMARY,
            )
            self.lbl_title.place(relx=0.5, rely=0.5, anchor="center")
            
        # Botão de Ação (Direita)
        if action_icon and on_action:
            self.btn_action = ctk.CTkButton(
                self,
                text="",
                image=action_icon,
                width=40,
                height=40,
                fg_color="transparent",
                hover_color=Colors.SURFACE_HOVER,
                command=on_action,
            )
            self.btn_action.pack(side="right")

    def set_title(self, title):
        if hasattr(self, 'lbl_title'):
            self.lbl_title.configure(text=title)
