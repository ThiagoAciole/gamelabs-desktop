import os
import zipfile
import threading
import gdown
import customtkinter as ctk
from PIL import Image
from .paths import get_icon_path, get_system_root, get_games_root, DEFAULT_CONSOLES
from .theme import Colors, Fonts

class InitialSetup:
    def __init__(self, root_window):
        self.root = root_window
        self.system_root = get_system_root()
        self.games_root = get_games_root()
        self.google_drive_url = "https://drive.google.com/uc?id=1vEBWkDBKqc2Kbyn8d-F9JAPP-XYpkvRD"
        self.zip_path = os.path.join(self.system_root, "system_files.zip")
        
        self.loading_window = None
        self.progress_bar = None
        self.status_label = None

    def check_and_setup(self, on_complete_callback):
        """Verifica pastas e inicia o download se necessário."""
        # 1. Garante que as pastas básicas existam (isso já é feito pelo paths.py mas reforçamos)
        if not os.path.exists(self.system_root):
            os.makedirs(self.system_root, exist_ok=True)
            
        if not os.path.exists(self.games_root):
            os.makedirs(self.games_root, exist_ok=True)
            
        for console in DEFAULT_CONSOLES:
            console_path = os.path.join(self.games_root, console)
            os.makedirs(console_path, exist_ok=True)
            # Também cria pasta Covers por conveniência
            os.makedirs(os.path.join(console_path, "Covers"), exist_ok=True)

        # 2. Verifica se a pasta system está vazia
        # Ignoramos arquivos ocultos ou system_files.zip se ele já estiver lá
        system_files = [f for f in os.listdir(self.system_root) if f != "system_files.zip"]
        
        if not system_files:
            # Se estiver vazia, mostra loading e baixa
            self._show_loading()
            threading.Thread(target=self._download_and_extract, args=(on_complete_callback,), daemon=True).start()
        else:
            # Se não estiver vazia, segue normalmente
            on_complete_callback()

    def _show_loading(self):
        self.loading_window = ctk.CTkToplevel(self.root)
        self.loading_window.title("Configurando GameLabs")
        self.loading_window.attributes("-fullscreen", True)
        self.loading_window.configure(fg_color="black")
        self.loading_window.attributes("-topmost", True)
        self.loading_window.overrideredirect(True)

        # Logo
        logo_path = get_icon_path("logo.png")
        if os.path.exists(logo_path):
            try:
                pil_img = Image.open(logo_path)
                logo_size = (150, 150)
                big_logo = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=logo_size)
                ctk.CTkLabel(self.loading_window, text="", image=big_logo).place(relx=0.5, rely=0.4, anchor="center")
            except:
                pass

        # Texto de Status
        self.status_label = ctk.CTkLabel(
            self.loading_window,
            text="Configurando GameLabs...",
            text_color="white",
            font=Fonts.SUBTITLE
        )
        self.status_label.place(relx=0.5, rely=0.55, anchor="center")

        # Barra de Progresso
        self.progress_bar = ctk.CTkProgressBar(
            self.loading_window,
            width=400,
            height=6,
            mode="indeterminate",
            progress_color=Colors.ACCENT,
            fg_color=Colors.BORDER,
        )
        self.progress_bar.place(relx=0.5, rely=0.62, anchor="center")
        self.progress_bar.start()

        self.loading_window.update()

    def _download_and_extract(self, on_complete_callback):
        try:
            # Download
            self.root.after(0, lambda: self.status_label.configure(text="Baixando arquivos do sistema (pode demorar)..."))
            gdown.download(self.google_drive_url, self.zip_path, quiet=False)

            # Extração
            self.root.after(0, lambda: self.status_label.configure(text="Extraindo arquivos..."))
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.system_root)

            # Limpeza
            if os.path.exists(self.zip_path):
                os.remove(self.zip_path)

            self.root.after(0, lambda: self.status_label.configure(text="Concluído!"))
            
        except Exception as e:
            print(f"Erro no setup inicial: {e}")
            self.root.after(0, lambda: self.status_label.configure(text=f"Erro ao configurar: {e}"))
            # Espera um pouco para o usuário ver o erro antes de seguir (ou fechar)
            import time
            time.sleep(3)
        
        finally:
            self.root.after(0, self._finish_setup, on_complete_callback)

    def _finish_setup(self, on_complete_callback):
        if self.loading_window:
            self.loading_window.destroy()
        on_complete_callback()
