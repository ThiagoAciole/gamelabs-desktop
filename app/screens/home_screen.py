import customtkinter as ctk

# Importamos o carregador do dicionário e a função para imagens dinâmicas (consoles)
from utils.audio import AudioManager
from utils.icons import  load_image_from_path, load_ui_assets
from utils.inputs import InputManager
from utils.paths import get_console_path
from utils.theme import Colors, Dimensions

# Componentes
from components.header import Header
from components.footer import Footer

class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent, on_console_select):
        super().__init__(parent, fg_color=Colors.BACKGROUND)
        self.on_console_select = on_console_select
        # Inicializa o InputManager pegando a janela raiz
        self.inputs = InputManager(self.winfo_toplevel())

        # 1. Carrega os ícones fixos da UI
        self.icons = load_ui_assets()

        # 2. Dados dos Consoles
        self.consoles = [
            {"name": "Playstation", "img": "ps1.png"},
            {"name": "Playstation 2", "img": "ps2.png"},
            {"name": "PSP", "img": "psp.png"},
            {"name": "Games", "img": "pc.png"},
        ]
        self.current_index = 0

        # 3. Carrega imagens dinâmicas dos consoles
        self.console_images = {}
        for c in self.consoles:
            # Usamos a função importada para carregar itens que não estão no dict fixo
            self.console_images[c["name"]] = load_image_from_path(get_console_path(c["img"]), (400, 400))

        # --- Layout ---
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=1) # Carousel
        self.grid_rowconfigure(2, weight=0) # Footer
        self.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.create_carousel()
        self.create_footer()
        self.update_display()
        # --- APLICA OS CONTROLES ---
        # Aqui conectamos o teclado às funções da Home
        self.setup_controls()

    def setup_controls(self):
        self.inputs.bind_screen_controls(
            on_left=self.prev_console,
            on_right=self.next_console,
            on_confirm=self.confirm_selection,
            on_back=lambda: self.winfo_toplevel().destroy()
        )

    def create_header(self):
        # Usamos o componente Header desacoplado
        # Na home, temos Logo a esquerda e Menu a direita (Action)
        # Como o Header padrão espera titulo no meio e back na esquerda, podemos adaptar ou instanciar elementos manuais se fugir muito do padrão.
        # O Header component atual suporta: title, icon_back, action_icon.
        # Home header é um pouco diferente (Logo a esquerda). 
        # Vamos manter customizado aqui ou melhorar o componente Header? 
        # Vamos usar um frame simples aqui pois o Header component foi feito pensado em "Tela com Titulo".
        
        # Mas para "Code Clean", vamos fazer um header container
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=Dimensions.HEADER_HEIGHT)
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=20)
        
        ctk.CTkLabel(header_frame, text="", image=self.icons["logo"]).pack(side="left")

        ctk.CTkButton(
            header_frame,
            text="",
            image=self.icons["menu"],
            width=40,
            fg_color="transparent",
            hover=False,
        ).pack(side="right")

    def create_carousel(self):
        carousel_frame = ctk.CTkFrame(self, fg_color="transparent")
        carousel_frame.grid(row=1, column=0, sticky="ew")

        carousel_frame.grid_columnconfigure(0, weight=1)
        carousel_frame.grid_columnconfigure(1, weight=0)
        carousel_frame.grid_columnconfigure(2, weight=1)

        # Botão Esquerda
        self.btn_prev = ctk.CTkButton(
            carousel_frame,
            text="",
            image=self.icons["arrow_left"],
            width=60,
            height=60,
            fg_color="transparent",
            hover_color=Colors.SURFACE_HOVER,
            command=self.prev_console,
        )
        self.btn_prev.grid(row=0, column=0, sticky="w", padx=30)

        # Centro (Imagem/Botão)
        content_box = ctk.CTkFrame(carousel_frame, fg_color="transparent")
        content_box.grid(row=0, column=1)

        self.btn_console_img = ctk.CTkButton(
            content_box,
            text="",
            fg_color="transparent",
            hover=False,
            command=self.confirm_selection,
        )
        self.btn_console_img.pack()

        # Botão Direita
        self.btn_next = ctk.CTkButton(
            carousel_frame,
            text="",
            image=self.icons["arrow_right"],
            width=60,
            height=60,
            fg_color="transparent",
            hover_color=Colors.SURFACE_HOVER,
            command=self.next_console,
        )
        self.btn_next.grid(row=0, column=2, sticky="e", padx=30)

    def create_footer(self):
        footer = Footer(self)
        footer.grid(row=2, column=0, pady=30)
        
        # Centralizar o footer se quiser? O grid acima já centraliza o frame na coluna 0.
        # Mas os itens dentro do footer são pack left.
        # Vamos usar um frame wrapper ou deixar assim.
        
        footer.add_legend("Confirmar", self.icons["btn_a"])

    def update_display(self):
        data = self.consoles[self.current_index]
        img = self.console_images.get(data["name"])

        if img:
            self.btn_console_img.configure(image=img, state="normal")
        else:
            self.btn_console_img.configure(image=None, text="[Sem Imagem]")

    def next_console(self):
        AudioManager.play_sound("navigate.mp3")
        self.current_index = (self.current_index + 1) % len(self.consoles)
        self.update_display()

    def prev_console(self):
        AudioManager.play_sound("navigate.mp3")
        self.current_index = (self.current_index - 1) % len(self.consoles)
        self.update_display()

    def confirm_selection(self):
        AudioManager.play_sound("press.mp3")
        self.on_console_select(self.consoles[self.current_index]["name"])
