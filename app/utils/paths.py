import os
import sys

# Verifica se está rodando como executável compilado (.exe) ou script Python normal
IS_FROZEN = getattr(sys, "frozen", False)


def get_project_root():
    """
    Retorna a raiz do projeto (GameLabs/).
    - Se for script: Sobe de 'app/utils' para 'GameLabs'.
    - Se for .exe: É a pasta onde o .exe está localizado.
    """
    if IS_FROZEN:
        return os.path.dirname(sys.executable)

    # Se for script: Estamos em app/utils/paths.py -> sobe 2 niveis para GameLabs/
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def get_internal_root():
    """
    Retorna a raiz interna dos arquivos da aplicação (app/).
    Importante para achar Assets quando compilado.
    """
    if IS_FROZEN:
        # Quando compilado, os arquivos internos ficam numa pasta temporária (_MEIPASS)
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        return os.path.join(base, "app")

    # Se for script: Estamos em app/utils/paths.py -> sobe 1 nivel para app/
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# --- CAMINHOS BASE ---


def get_assets_root():
    """Retorna o caminho da pasta assets."""
    return os.path.join(get_internal_root(), "assets")


def get_games_root():
    """Retorna o caminho da pasta games (externa)."""
    path = os.path.join(get_project_root(), "games")
    os.makedirs(path, exist_ok=True)  # Cria se não existir
    return path


def get_system_root():
    """Retorna o caminho da pasta system (externa)."""
    path = os.path.join(get_project_root(), "system")
    os.makedirs(path, exist_ok=True)  # Cria se não existir
    return path


# --- FUNÇÕES DE BUSCA DE ARQUIVOS ---


def get_asset_path(filename: str = "") -> str:
    """Busca arquivos dentro de app/assets/"""
    return os.path.join(get_assets_root(), filename)


def get_system_path(filename: str = "") -> str:
    """Busca arquivos dentro de system/"""
    return os.path.join(get_system_root(), filename)


def get_game_path(console_folder: str, rom_filename: str = "") -> str:
    """
    Busca arquivos dentro de games/CONSOLE/
    Ex: get_game_path('Playstation 2', 'jogo.iso')
    """
    # Garante que a pasta do console exista (ex: games/Playstation 2)
    console_path = os.path.join(get_games_root(), console_folder)
    os.makedirs(console_path, exist_ok=True)

    return os.path.join(console_path, rom_filename)


# --- ALIAS / ATALHOS (Para manter compatibilidade) ---


def get_icon_path(name: str):
    """Atalho para pegar ícones direto da raiz de assets ou subpasta"""
    # Se você tiver uma pasta 'icons' dentro de assets, mude para:
    # return get_asset_path(os.path.join("icons", name))
    return get_asset_path(name)


def get_button_path(name: str):
    return get_asset_path(name)


# --- DEBUG (Pode remover depois) ---
if __name__ == "__main__":
    print(f"Modo Congelado (EXE): {IS_FROZEN}")
    print(f"Raiz do Projeto: {get_project_root()}")
    print(f"Raiz Interna (App): {get_internal_root()}")
    print(f"Assets: {get_assets_root()}")
    print(f"Games: {get_games_root()}")
    print(f"System: {get_system_root()}")
