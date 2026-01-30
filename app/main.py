import customtkinter as ctk
from screens.game_list import GameList
from screens.home_screen import HomeScreen
from utils.audio import AudioManager
from utils.theme import Colors
from utils.paths import get_asset_path, get_icon_path, initialize_folders
from utils.setup_manager import InitialSetup


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Inicializa as pastas do sistema básicas
        initialize_folders()

        self.title("GameLabs")
        self.attributes("-fullscreen", True)
        self.configure(fg_color=Colors.BACKGROUND)

        # Tenta carregar o ícone da janela
        try:
            self.iconbitmap(get_icon_path("icon.ico"))
        except Exception as e:
            print(f"Aviso: Ícone não encontrado ou formato inválido. {e}")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Inicia a música de fundo
        try:
            AudioManager.play_bgm("bgm.mp3", volume=0.6)
        except Exception as e:
            print(f"Erro ao iniciar música: {e}")

        # --- SETUP INICIAL (Pastas e Download) ---
        self.setup_manager = InitialSetup(self)
        self.setup_manager.check_and_setup(on_complete_callback=self.show_home)

    def show_home(self):
        # Garante que a chamada venha para a main thread se necessário
        # Remove a tela anterior se existir
        if hasattr(self, "current_screen") and self.current_screen:
            self.current_screen.destroy()

        # Cria a tela inicial
        # Nota: A HomeScreen deve configurar o InputManager para fechar o app no 'BACK'
        self.current_screen = HomeScreen(self, on_console_select=self.show_game_list)
        self.current_screen.grid(row=0, column=0, sticky="nsew")

    def show_game_list(self, console_name):
        # Remove a tela anterior se existir
        if hasattr(self, "current_screen") and self.current_screen:
            self.current_screen.destroy()

        # Cria a lista de jogos
        # Passamos self.show_home como callback para quando o usuário voltar
        self.current_screen = GameList(self, console_name, on_back=self.show_home)
        self.current_screen.grid(row=0, column=0, sticky="nsew")

    def destroy(self):
        """Sobrescreve o fechar para garantir que o áudio pare."""
        try:
            AudioManager.stop()
        except:
            pass
        super().destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
