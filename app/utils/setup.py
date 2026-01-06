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

    # =====================================================
    # 🎮 CASO 1: GAMES DE PC (ATALHO .LNK)
    # =====================================================
    if console_name == "Games":
        try:
            print("💻 Iniciando jogo de PC...")
            os.startfile(
                rom_path
            )  # Windows resolve tudo (exe, argumentos, working dir)
            print("✅ Jogo iniciado.")
        except Exception as e:
            print(f"❌ Erro ao iniciar jogo de PC: {e}")
        return

    # =====================================================
    # 🕹️ CASO 2: EMULADORES (RetroArch)
    # =====================================================
    if not os.path.exists(RETROARCH_EXE):
        print("❌ ERRO: retroarch.exe não encontrado!")
        return

    core_dll = CORES_MAP.get(console_name)
    if not core_dll:
        print(f"⚠️ AVISO: Core não mapeado para {console_name}")
        return

    full_core_path = os.path.join(CORES_DIR, core_dll)

    cmd = [
        RETROARCH_EXE,
        "-L",
        full_core_path,
        rom_path,
        "-f",
    ]

    print("🚀 Iniciando emulador...")

    try:
        creation_flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

        process = subprocess.Popen(
            cmd,
            cwd=get_system_root(),
            creationflags=creation_flags,
        )
        process.wait()

        print("✅ Emulador encerrado.")
    except Exception as e:
        print(f"❌ Falha no subprocesso: {e}")
