import os
import subprocess

from .paths import get_game_path, get_system_root

# --- CONFIGURAÇÃO DE CAMINHOS ---
RETROARCH_EXE = os.path.join(get_system_root(), "retroarch.exe")
CORES_DIR = os.path.join(get_system_root(), "cores")

CORES_MAP = {
    "Playstation": "swanstation_libretro.dll",
    "Playstation 2": "pcsx2_libretro.dll",
    "PSP": "ppsspp_libretro.dll",
}


def run_game(console_name, rom_filename):
    print("\n--- TENTANDO ABRIR JOGO ---")
    print(f"Console: {console_name}")

    rom_path = get_game_path(console_name, rom_filename)

    if not os.path.exists(rom_path):
        print(f"❌ ERRO: Arquivo não encontrado: {rom_path}")
        return

    # === CASO 1: PC GAMES ===
    if console_name == "Games":
        try:
            print("💻 Iniciando Games de PC...")
            work_dir = os.path.dirname(rom_path)

            if rom_path.lower().endswith(".lnk"):
                os.startfile(rom_path, cwd=work_dir)
            else:
                print(f"   Executando: {rom_path}")

                # Configura flag para não abrir janela extra se for .bat ou .cmd
                no_window_flag = 0
                if os.name == "nt":
                    no_window_flag = subprocess.CREATE_NO_WINDOW

                process = subprocess.Popen(
                    [rom_path],
                    cwd=work_dir,
                    creationflags=no_window_flag,  # Aplica aqui também por garantia
                )
                process.wait()

            print("✅ Jogo fechado.")
        except Exception as e:
            print(f"❌ Erro Games de PC: {e}")
        return

    # === CASO 2: EMULADORES (RetroArch) ===
    if not os.path.exists(RETROARCH_EXE):
        print("❌ ERRO: retroarch.exe não encontrado!")
        return

    core_dll = CORES_MAP.get(console_name)
    if not core_dll:
        print(f"⚠️ AVISO: Core não mapeado para {console_name}")
        return

    full_core_path = os.path.join(CORES_DIR, core_dll)

    # Nota: Removi o --verbose para limpar a saída, já que não veremos o terminal
    cmd = [RETROARCH_EXE, "-L", full_core_path, rom_path, "-f"]

    print("🚀 Iniciando emulador...")

    try:
        # Define a flag para ocultar a janela do console
        creation_flags = 0
        if os.name == "nt":  # Verifica se é Windows
            creation_flags = subprocess.CREATE_NO_WINDOW

        # Passamos creationflags aqui
        process = subprocess.Popen(
            cmd, cwd=get_system_root(), creationflags=creation_flags
        )

        process.wait()

        print("✅ Emulador encerrado.")
    except Exception as e:
        print(f"❌ Falha no subprocesso: {e}")
