import os
import shutil
import subprocess
import time
import tkinter.filedialog as filedialog
from tkinter import messagebox  # Necessário para confirmação de exclusão

import customtkinter as ctk
from PIL import Image, ImageDraw
from utils.audio import AudioManager
from utils.icons import add_legend, load_ui_assets
from utils.inputs import InputManager
from utils.paths import get_asset_path, get_games_root
from utils.setup import run_game

# Cores fixas
BACKGROUND = "#2b2b2b"
SURFACE_LIGHT = "#3a3a3a"


class GameList(ctk.CTkFrame):
    def __init__(self, parent, console_name, on_back):
        super().__init__(parent, fg_color="black")

        self.on_back = on_back
        self.console_name = console_name
        self.icons = load_ui_assets()
        self.root = self.winfo_toplevel()
        # Inicializa InputManager
        self.inputs = InputManager(self.winfo_toplevel())
        self.default_cover_path = get_asset_path("default.png")

        self.covers_path = os.path.join(get_games_root(), self.console_name, "Covers")
        if not os.path.exists(self.covers_path):
            os.makedirs(self.covers_path, exist_ok=True)

        self.games = []
        self.cover_size = (180, 240)

        self.load_games_from_folder()

        self.selected_index = 0
        self.visible_start = 0
        self.visible_count = 5
        self.card_width = 250
        self.card_height = 350

        # Layout Principal
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.create_header()

        self.lbl_selected_game = ctk.CTkLabel(
            self, text="", font=("Arial", 18, "bold"), text_color="#6200ea"
        )
        self.lbl_selected_game.grid(row=1, column=0, pady=10)

        self.create_carousel_area()
        self.create_footer()
        self.update_carousel()

        self.focus_set()
        self.setup_controls()

    def setup_controls(self):
        self.inputs.bind_screen_controls(
            on_left=self.move_left,
            on_right=self.move_right,
            on_confirm=self.launch_current_game,
            on_back=self.go_back,  # Aqui o InputManager vai ligar o ESC ao voltar
        )

    def round_corners(
        self,
        img: Image.Image,
        radius: int,
        border_width: int = 2,
        border_color=(51, 51, 51, 255),
    ):
        img = img.convert("RGBA")
        w, h = img.size

        # Máscara arredondada
        mask = Image.new("L", (w, h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle(
            [(0, 0), (w - 1, h - 1)],
            radius=radius,
            fill=255,
        )

        # Aplica transparência
        img.putalpha(mask)

        # Desenha SOMENTE a borda
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle(
            [
                (border_width // 2, border_width // 2),
                (w - border_width // 2 - 1, h - border_width // 2 - 1),
            ],
            radius=radius,
            outline=border_color,
            width=border_width,
        )

        return img

    def crop_image(self, pil_img, target_size):
        """Redimensiona mantendo proporção e corta o excesso (Center Crop)"""
        target_w, target_h = target_size
        img_w, img_h = pil_img.size

        scale = max(target_w / img_w, target_h / img_h)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)

        img_resized = pil_img.resize((new_w, new_h), Image.LANCZOS)

        left = (new_w - target_w) / 2
        top = (new_h - target_h) / 2
        right = (new_w + target_w) / 2
        bottom = (new_h + target_h) / 2

        return img_resized.crop((left, top, right, bottom))

    def load_games_from_folder(self):
        self.games = []
        folder_path = os.path.join(get_games_root(), self.console_name)

        valid_extensions = (
            ".iso",
            ".bin",
            ".cue",
            ".chd",
            ".cso",
            ".exe",
            ".pbp",
            ".zip",
            ".7z",
            ".bat",
            ".lnk",
            ".url",
        )
        img_extensions = (".jpg", ".png", ".jpeg")

        if os.path.exists(folder_path):
            files = os.listdir(folder_path)
            # Ordenar arquivos pode ajudar na consistência
            files.sort()
            for f in files:
                if f.lower().endswith(valid_extensions):
                    display_name = os.path.splitext(f)[0]

                    cover_img = None
                    possible_cover_path = None
                    found_cover = False

                    # 1️⃣ tenta achar capa real
                    for ext in img_extensions:
                        path = os.path.join(self.covers_path, display_name + ext)
                        if os.path.exists(path):
                            try:
                                pil_img = Image.open(path)
                                pil_cropped = self.crop_image(pil_img, self.cover_size)
                                pil_rounded = self.round_corners(
                                    pil_cropped, radius=10, border_width=1
                                )

                                cover_img = ctk.CTkImage(
                                    pil_rounded, size=self.cover_size
                                )
                                possible_cover_path = path
                                found_cover = True
                            except Exception:
                                pass
                            break

                    # 2️⃣ se NÃO achou capa → usa default.png
                    if not found_cover and os.path.exists(self.default_cover_path):
                        try:
                            pil_img = Image.open(self.default_cover_path)
                            pil_cropped = self.crop_image(pil_img, self.cover_size)
                            pil_rounded = self.round_corners(
                                pil_cropped, radius=10, border_width=1
                            )

                            cover_img = ctk.CTkImage(pil_rounded, size=self.cover_size)
                            possible_cover_path = None
                        except Exception:
                            cover_img = None

                    self.games.append(
                        {
                            "name": display_name,
                            "file": f,
                            "cover": cover_img,
                            "cover_path": possible_cover_path,
                        }
                    )

    def create_loading_screen(self):
        loading_window = ctk.CTkToplevel(self.root)
        loading_window.title("Loading")

        loading_window.attributes("-fullscreen", True)
        loading_window.configure(fg_color="black")
        loading_window.attributes("-topmost", True)
        loading_window.overrideredirect(True)

        progress_bar = ctk.CTkProgressBar(
            loading_window,
            width=300,
            height=4,
            mode="indeterminate",
            progress_color="#6200ea",
            fg_color="#333333",
        )
        # Tenta forçar um intervalo rápido de atualização (5ms)
        try:
            progress_bar.start(5)
        except:
            progress_bar.start()

        logo_path = get_asset_path("logo.png")
        logo_size = (100, 100)

        logo_loaded = False

        if os.path.exists(logo_path):
            try:
                pil_img = Image.open(logo_path)
                big_logo = ctk.CTkImage(
                    light_image=pil_img, dark_image=pil_img, size=logo_size
                )
                ctk.CTkLabel(loading_window, text="", image=big_logo).place(
                    relx=0.5, rely=0.45, anchor="center"
                )
                progress_bar.place(relx=0.5, rely=0.55, anchor="center")
                logo_loaded = True
            except:
                logo_loaded = False

        if not logo_loaded:
            progress_bar.place(relx=0.5, rely=0.5, anchor="center")
            ctk.CTkLabel(
                loading_window,
                text="Carregando...",
                text_color="gray",
                font=("Arial", 12),
            ).place(relx=0.5, rely=0.55, anchor="center")

        loading_window.update()
        loading_window.attributes("-topmost", False)
        return loading_window

    def create_windows_shortcut(self, target_path, shortcut_path):
        target_path = os.path.abspath(target_path)
        shortcut_path = os.path.abspath(shortcut_path)

        ps_script = f"""
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
    $Shortcut.TargetPath = '{target_path}'
    $Shortcut.WorkingDirectory = '{os.path.dirname(target_path)}'
    $Shortcut.IconLocation = '{target_path},0'
    $Shortcut.Save()
    """

        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                ps_script,
            ],
            check=True,
        )

        # 🔍 DEBUG CRÍTICO
        if not os.path.exists(shortcut_path):
            raise Exception("Falha ao criar atalho (.lnk)")

    def launch_current_game(self):
        if not self.games:
            return
        game_data = self.games[self.selected_index]
        AudioManager.play_sound("press.mp3")
        loading_screen = self.create_loading_screen()
        AudioManager.stop()

        start_time = time.time()
        while time.time() - start_time < 3.0:
            loading_screen.update()
            time.sleep(0.01)

        loading_screen.attributes("-topmost", False)

        try:
            run_game(self.console_name, game_data["file"])
        except Exception as e:
            print(f"Erro ao rodar jogo: {e}")

        loading_screen.destroy()
        self.focus_set()
        AudioManager.play_bgm("bgm.mp3", 0.6)

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent", height=60)
        header.grid(row=0, column=0, sticky="ew", padx=30, pady=20)
        ctk.CTkButton(
            header,
            text="",
            image=self.icons["return"],
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#222",
            command=self.go_back,
        ).pack(side="left")
        ctk.CTkLabel(
            header,
            text=self.console_name,
            font=("Arial", 28, "bold"),
            text_color="white",
        ).place(relx=0.5, rely=0.5, anchor="center")
        if self.console_name == "Games":
            icon_add = self.icons.get("add") or self.icons.get("placeholder")
            ctk.CTkButton(
                header,
                text="",
                image=icon_add,
                width=40,
                height=40,
                fg_color="transparent",
                hover_color="#222",
                command=self.add_pc_game_action,
            ).pack(side="right")

    def add_pc_game_action(self):
        AudioManager.play_sound("press.mp3")

        file_path = filedialog.askopenfilename(
            title="Selecione o executável do jogo",
            filetypes=[("Jogos de PC", "*.exe *.lnk")],
        )
        if not file_path:
            return

        dest_folder = os.path.join(get_games_root(), "Games")
        os.makedirs(dest_folder, exist_ok=True)

        filename = os.path.basename(file_path)
        name_only, ext = os.path.splitext(filename)

        try:
            if ext.lower() == ".lnk":
                dest_path = os.path.join(dest_folder, filename)
                shutil.copy(file_path, dest_path)
            else:
                dest_path = os.path.join(dest_folder, f"{name_only}.lnk")
                self.create_windows_shortcut(file_path, dest_path)

            print(f"✅ Jogo adicionado: {dest_path}")

            self.load_games_from_folder()

            self.selected_index = max(0, len(self.games) - 1)
            self.visible_start = max(0, len(self.games) - self.visible_count)

            self.update_carousel()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar jogo:\n{e}")

    def open_context_menu(self, event, game_index):
        root = self.winfo_toplevel()
        # Remove menus anteriores
        for w in root.winfo_children():
            if isinstance(w, ctk.CTkFrame) and getattr(w, "is_context_menu", False):
                w.destroy()

        menu = ctk.CTkFrame(
            root,
            fg_color=BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color="#111",
        )
        menu.is_context_menu = True

        icon_edit = self.icons.get("edit")
        icon_edit_image = self.icons.get("edit_image")
        icon_trash = self.icons.get("trash")
        # --- OPÇÃO 1: ALTERAR CAPA ---
        ctk.CTkButton(
            menu,
            image=icon_edit_image,
            text="Alterar Capa",
            compound="left",
            font=("Segoe UI", 13, "bold"),
            text_color="white",
            fg_color="transparent",
            hover_color=SURFACE_LIGHT,
            corner_radius=6,
            width=200,
            height=35,
            anchor="w",
            command=lambda: (menu.destroy(), self.change_cover_action(game_index)),
        ).pack(padx=5, pady=(5, 2))

        # --- OPÇÃO 2: RENOMEAR ---
        ctk.CTkButton(
            menu,
            image=icon_edit,
            text="Renomear Jogo",
            compound="left",
            font=("Segoe UI", 13, "bold"),
            text_color="white",
            fg_color="transparent",
            hover_color=SURFACE_LIGHT,
            corner_radius=6,
            width=200,
            height=35,
            anchor="w",
            command=lambda: (menu.destroy(), self.rename_game_action(game_index)),
        ).pack(padx=5, pady=2)

        # --- OPÇÃO 3: REMOVER ---
        ctk.CTkButton(
            menu,
            image=icon_trash,
            text="Remover Jogo",
            compound="left",
            font=("Segoe UI", 13, "bold"),
            text_color="#ff5555",
            fg_color="transparent",
            hover_color=SURFACE_LIGHT,
            corner_radius=6,
            width=200,
            height=35,
            anchor="w",
            command=lambda: (menu.destroy(), self.remove_game_action(game_index)),
        ).pack(padx=5, pady=(2, 5))

        # Posicionamento do Menu
        widget = event.widget
        widget_x = widget.winfo_rootx() - root.winfo_rootx()
        widget_y = widget.winfo_rooty() - root.winfo_rooty()
        widget_w = widget.winfo_width()
        menu_w = 210
        window_w = root.winfo_width()

        pos_x = (
            max(widget_x - menu_w - 10, 0)
            if widget_x + widget_w + menu_w + 20 > window_w
            else widget_x + widget_w + 10
        )
        menu.place(x=pos_x, y=widget_y)
        menu.lift()

        def close_menu(ev):
            try:
                if not (
                    menu.winfo_x()
                    <= ev.x_root - root.winfo_rootx()
                    <= menu.winfo_x() + menu.winfo_width()
                    and menu.winfo_y()
                    <= ev.y_root - root.winfo_rooty()
                    <= menu.winfo_y() + menu.winfo_height()
                ):
                    menu.destroy()
                    root.unbind("<Button-1>")
            except:
                pass

        root.bind("<Button-1>", close_menu)

    # --- AÇÃO: RENOMEAR JOGO ---
    def rename_game_action(self, game_index):
        game_data = self.games[game_index]
        current_name = game_data["name"]
        old_file_path = os.path.join(
            get_games_root(), self.console_name, game_data["file"]
        )

        # Caixa de diálogo para novo nome
        dialog = ctk.CTkInputDialog(
            text="Digite o novo nome do jogo:", title="Renomear Jogo"
        )
        new_name = dialog.get_input()

        if new_name and new_name != current_name:
            try:
                # 1. Renomear arquivo do jogo
                file_ext = os.path.splitext(game_data["file"])[1]
                new_filename = new_name + file_ext
                new_file_path = os.path.join(
                    get_games_root(), self.console_name, new_filename
                )

                os.rename(old_file_path, new_file_path)

                # 2. Renomear capa (se existir)
                if game_data["cover_path"] and os.path.exists(game_data["cover_path"]):
                    cover_ext = os.path.splitext(game_data["cover_path"])[1]
                    new_cover_path = os.path.join(
                        self.covers_path, new_name + cover_ext
                    )
                    os.rename(game_data["cover_path"], new_cover_path)

                AudioManager.play_sound("press.mp3")
                # Recarrega a lista para atualizar
                self.load_games_from_folder()
                self.update_carousel()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao renomear: {e}")

    # --- AÇÃO: REMOVER JOGO ---
    def remove_game_action(self, game_index):
        game_data = self.games[game_index]
        game_name = game_data["name"]

        confirm = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja apagar o jogo '{game_name}'?\nIsso excluirá o arquivo permanentemente.",
        )

        if confirm:
            try:
                # 1. Remover arquivo do jogo
                file_path = os.path.join(
                    get_games_root(), self.console_name, game_data["file"]
                )
                if os.path.exists(file_path):
                    os.remove(file_path)

                # 2. (Opcional) Remover capa
                # Se não quiser remover a capa automaticamente, comente este bloco
                if game_data["cover_path"] and os.path.exists(game_data["cover_path"]):
                    try:
                        os.remove(game_data["cover_path"])
                    except:
                        pass

                AudioManager.play_sound("press.mp3")

                # Ajusta índices
                del self.games[game_index]
                if self.selected_index >= len(self.games):
                    self.selected_index = max(0, len(self.games) - 1)

                # Ajusta visualização se a lista ficou menor que o count visível
                if (
                    self.visible_start > 0
                    and len(self.games) <= self.visible_start + self.visible_count
                ):
                    self.visible_start = max(0, self.visible_start - 1)

                self.update_carousel()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover arquivo: {e}")

    def change_cover_action(self, game_index):
        file_path = filedialog.askopenfilename(
            title="Selecione a nova capa", filetypes=[("Imagens", "*.jpg *.jpeg *.png")]
        )
        if not file_path:
            return
        game_data = self.games[game_index]
        game_name = game_data["name"]
        _, ext = os.path.splitext(file_path)
        new_dest_path = os.path.join(self.covers_path, game_name + ext)
        try:
            shutil.copy(file_path, new_dest_path)
            pil_img = Image.open(new_dest_path)

            pil_cropped = self.crop_image(pil_img, self.cover_size)
            new_ctk_img = ctk.CTkImage(pil_cropped, size=self.cover_size)

            self.games[game_index]["cover"] = new_ctk_img
            self.games[game_index]["cover_path"] = new_dest_path
            self.update_carousel()
        except Exception as e:
            print(f"Erro: {e}")

    def create_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent", height=50)
        footer.grid(row=3, column=0, pady=30)
        add_legend(footer, "Jogar", self.icons["btn_a"])
        add_legend(footer, "Voltar", self.icons["btn_b"])

    def create_carousel_area(self):
        carousel_frame = ctk.CTkFrame(self, fg_color="transparent")
        carousel_frame.grid(row=2, column=0, sticky="nsew")
        carousel_frame.grid_columnconfigure((0, 2), weight=1)
        carousel_frame.grid_columnconfigure(1, weight=10)
        carousel_frame.grid_rowconfigure(0, weight=1)

        self.btn_left = ctk.CTkButton(
            carousel_frame,
            text="",
            image=self.icons["arrow_left"],
            width=50,
            height=300,
            fg_color="transparent",
            hover_color="#111",
            command=self.move_left,
        )
        self.btn_left.grid(row=0, column=0)
        self.cards_container = ctk.CTkFrame(carousel_frame, fg_color="transparent")
        self.cards_container.grid(row=0, column=1, sticky="nsew")
        self.btn_right = ctk.CTkButton(
            carousel_frame,
            text="",
            image=self.icons["arrow_right"],
            width=50,
            height=300,
            fg_color="transparent",
            hover_color="#111",
            command=self.move_right,
        )
        self.btn_right.grid(row=0, column=2)

    def update_carousel(self):
        # Limpa os widgets anteriores
        for w in self.cards_container.winfo_children():
            w.destroy()

        # Verifica se tem jogos
        if not self.games:
            self.btn_left.grid_remove()
            self.btn_right.grid_remove()
            self.lbl_selected_game.grid_remove()
            icon = self.icons.get("not_found") or self.icons["placeholder"]
            empty_frame = ctk.CTkFrame(self.cards_container, fg_color="transparent")
            empty_frame.pack(expand=True)
            ctk.CTkLabel(empty_frame, text="", image=icon).pack()
            ctk.CTkLabel(
                empty_frame,
                text="Nenhum jogo encontrado.",
                text_color="gray",
                font=("Arial", 14),
            ).pack(pady=10)
            return

        # Mostra botões de navegação
        self.btn_left.grid()
        self.btn_right.grid()
        self.lbl_selected_game.grid()
        self.lbl_selected_game.configure(text=self.games[self.selected_index]["name"])

        # --- A MÁGICA ACONTECE AQUI ---
        # 1. Criamos um "Container Interno" transparente.
        #    O 'expand=True' faz esse container flutuar no CENTRO da tela.
        inner_container = ctk.CTkFrame(self.cards_container, fg_color="transparent")
        inner_container.pack(expand=True)

        end = min(self.visible_start + self.visible_count, len(self.games))
        for i, game in enumerate(self.games[self.visible_start : end]):
            real_index = self.visible_start + i
            is_sel = real_index == self.selected_index

            card = ctk.CTkFrame(
                inner_container,
                width=self.card_width,
                height=self.card_height,
                fg_color="#1a1a1a" if is_sel else "#0d0d0d",
                border_color="#6200ea" if is_sel else "#333",
                border_width=3 if is_sel else 2,
                corner_radius=15,
            )

            # 3. Usamos expand=False para que eles fiquem coladinhos (respeitando apenas o padx)
            card.pack(side="left", padx=15, expand=False)

            # Impede que o frame encolha para o tamanho do conteúdo (mantém tamanho fixo)
            card.pack_propagate(False)

            display_img = game["cover"] if game["cover"] else self.icons["placeholder"]

            img_lbl = ctk.CTkLabel(
                card, text="", image=display_img, fg_color="transparent"
            )
            img_lbl.place(relx=0.5, rely=0.45, anchor="center")

            lbl_name = ctk.CTkLabel(
                card,
                text=game["name"],
                text_color="white" if is_sel else "gray",
                font=("Arial", 14, "bold" if is_sel else "normal"),
                wraplength=self.card_width - 20,
            )
            lbl_name.place(relx=0.5, rely=0.9, anchor="center")

            if is_sel:
                for w in [card, img_lbl, lbl_name]:
                    w.bind("<Button-1>", lambda e: self.launch_current_game())
            for w in [card, img_lbl, lbl_name]:
                w.bind(
                    "<Button-3>",
                    lambda e, idx=real_index: self.open_context_menu(e, idx),
                )

    def move_right(self):
        if not self.games:
            return
        if self.selected_index < len(self.games) - 1:
            AudioManager.play_sound("navigate.mp3")
            self.selected_index += 1
            if self.selected_index >= self.visible_start + self.visible_count:
                self.visible_start += 1
            self.update_carousel()

    def move_left(self):
        if not self.games:
            return
        if self.selected_index > 0:
            AudioManager.play_sound("navigate.mp3")
            self.selected_index -= 1
            if self.selected_index < self.visible_start:
                self.visible_start -= 1
            self.update_carousel()

    def go_back(self):
        AudioManager.play_sound("press.mp3")
        self.on_back()
