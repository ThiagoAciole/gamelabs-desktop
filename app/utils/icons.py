import os
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image

from .paths import get_button_path, get_icon_path


def load_ctk_image(name: str, size=(30, 30)):
    try:
        path = get_icon_path(name)
        if not os.path.exists(path):
            print(f"⚠️ Imagem não encontrada: {path}")
            return None

        img = Image.open(path)
        return CTkImage(light_image=img, dark_image=img, size=size)
    except Exception as e:
        print(f"❌ Erro ao carregar {name}: {e}")
        return None


def load_button_image(name: str, size=(30, 30)):
    try:
        img = Image.open(get_button_path(name))
        return CTkImage(light_image=img, dark_image=img, size=size)
    except Exception:
        return None


def load_ui_assets():
    return {
        # Navegação
        "arrow_left": load_ctk_image("chevron-left.png", (30, 30)),
        "arrow_right": load_ctk_image("chevron-right.png", (30, 30)),
        "return": load_ctk_image("return.png", (30, 30)),
        "menu": load_ctk_image("menu.png", (30, 30)),
        "edit": load_ctk_image("edit.png", (30, 30)),
        "edit_image": load_ctk_image("edit-image.png", (30, 30)),
        "trash": load_ctk_image("trash.png", (30, 30)),
        # Identidade
        "logo": load_ctk_image("logo.png", (40, 40)),
        "placeholder": load_ctk_image("gamepad.png", (80, 80)),
        "not_found":   load_ctk_image("notfound.png", (200, 200)),
        "add": load_ctk_image("add.png", (30, 30)),
        # Botões (Controles)
        "btn_a": load_button_image("A.png"),
        "btn_b": load_button_image("B.png"),
        "btn_x": load_button_image("X.png"),
        
    }


def add_legend(screen, text, icon):
    f = ctk.CTkFrame(screen, fg_color="transparent")
    f.pack(side="left", padx=20)
    if icon:
        ctk.CTkLabel(f, text="", image=icon).pack(side="left", padx=5)
    ctk.CTkLabel(f, text=text, text_color="#ccc", font=("Kanit", 14)).pack(side="left")
