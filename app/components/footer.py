import customtkinter as ctk
from utils.theme import Colors, Fonts, Dimensions

class Footer(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", height=Dimensions.FOOTER_HEIGHT, **kwargs)
        # self.pack_propagate(False) # Removido para permitir que a largura se ajuste ao conteúdo
        
    def add_legend(self, text, icon):
        """Adiciona um item de legenda ao rodapé."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(side="left", padx=20)
        
        if icon:
            ctk.CTkLabel(container, text="", image=icon).pack(side="left", padx=5)
            
        ctk.CTkLabel(
            container, 
            text=text, 
            text_color=Colors.TEXT_SECONDARY, 
            font=Fonts.LEGEND,
            width=Dimensions.FOOTER_LEGEND_WIDTH,
            anchor="w"
            
        ).pack(side="left")
