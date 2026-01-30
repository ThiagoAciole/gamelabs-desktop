import os
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image

from .paths import get_button_path, get_icon_path, get_ui_path, get_asset_path


def load_image_from_path(path: str, size=(30, 30)):
    """Carrega uma CTkImage de um caminho absoluto/completo"""
    try:
        if not os.path.exists(path):
            print(f"⚠️ Imagem não encontrada: {path}")
            return None

        img = Image.open(path)
        return CTkImage(light_image=img, dark_image=img, size=size)
    except Exception as e:
        print(f"❌ Erro ao carregar imagem de {path}: {e}")
        return None


def load_ui_assets():
    """Carrega todos os assets de UI usando os caminhos organizados"""
    return {
        # Navegação
        "arrow_left": load_image_from_path(get_ui_path("chevron-left.png")),
        "arrow_right": load_image_from_path(get_ui_path("chevron-right.png")),
        "return": load_image_from_path(get_ui_path("return.png")),
        "menu": load_image_from_path(get_ui_path("menu.png")),
        "edit": load_image_from_path(get_ui_path("edit.png")),
        "edit_image": load_image_from_path(get_ui_path("edit-image.png")),
        "trash": load_image_from_path(get_ui_path("trash.png")),
        
        # Identidade
        "logo": load_image_from_path(get_icon_path("logo.png"), (40, 40)),
        "placeholder": load_image_from_path(get_button_path("gamepad.png"), (80, 80)),
        "not_found":   load_image_from_path(get_ui_path("notfound.png"), (200, 200)),
        "add": load_image_from_path(get_ui_path("add.png")),
        
        # Botões (Controles)
        "btn_a": load_image_from_path(get_button_path("A.png")),
        "btn_b": load_image_from_path(get_button_path("B.png")),
        "btn_x": load_image_from_path(get_button_path("X.png")),
    }
