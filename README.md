<p align="center">
<img width="620" height="100" alt="gamelabs-logo-dark" src="https://github.com/user-attachments/assets/4346f635-73d2-4bda-ba65-99a2b865b5fe#gh-light-mode-only" />
<img width="620" height="100" alt="gamelabs-logo-light" src="https://github.com/user-attachments/assets/f5d43f3e-6c21-46f2-9596-78f96692a44d#gh-dark-mode-only" />
</p>

**Gamelabs Desktop** é um launcher e front-end para **Windows** desenvolvido em Python, projetado para transformar seu PC ou Notebook em uma estação de emulação dedicada. Com uma interface **"Dashboard" imersiva**, ele organiza seus emuladores e jogos de PC em uma experiência fluida, controlável via teclado ou gamepad.

### 🚀 Preview
<p align="center">
  <img src="https://github.com/user-attachments/assets/f0a1f9c9-3ef9-44f8-bc08-f243edd1f97d" width="700" />
</p>

## ✨ Funcionalidades

### 🎮 Interface Imersiva (TV/Handheld Friendly)
- Design minimalista em tela cheia (Fullscreen).
- **Background Dinâmico**: O plano de fundo muda suavemente conforme o console selecionado.
- Navegação por carrossel de cartões com **efeito de bordas arredondadas**.
- Feedback sonoro (BGM e SFX) para navegação e seleção.

### 🕹️ Suporte a Sistemas

O Gamelabs atua como um front-end para o **RetroArch**, gerenciando o lançamento de jogos de forma transparente para o usuário (backend invisível).

#### Consoles Suportados (Via RetroArch Cores):
- **Playstation 1** (SwanStation)
- **Playstation 2** (PCSX2 / LRPS2)
- **PSP** (PPSSPP)

#### 💻 PC Games (Nativo)
- Lançador para jogos de Windows.
- Suporte a executáveis (`.exe`), atalhos (`.lnk`) e scripts (`.bat`).
- Criação automática de scripts de lançamento para garantir compatibilidade.

### 🎨 Customização
- Suporte a **Capas Personalizadas** (`.jpg`, `.png`) com recorte e arredondamento automático.
- Menu de contexto (Botão Direito) para alteração rápida de capas dentro do próprio app.

## 📂 Estrutura de Arquivos

Para que o Gamelabs funcione, a estrutura de pastas ao lado do executável (`GameLabs.exe` ou `main.py`) deve ser a seguinte:

```plaintext
/GameLabs/
├── app/                  # Código Fonte (se rodando via Python)
│   └── assets/           # Ícones, Logos e Sons
├── games/                # Onde você coloca seus jogos
│   ├── PC Games/
│   ├── Playstation/
│   ├── Playstation 2/
│   ├── PSP/
│       ├── ROMs/         # Arquivos de jogo (.iso, .bin, .exe, etc)
│       └── Covers/       # Capas dos jogos
└── system/               # Backend de Emulação
    ├── retroarch.exe     # Executável do RetroArch
    └── cores/            # Núcleos Libretro (.dll)
        ├── swanstation_libretro.dll
        ├── pcsx2_libretro.dll
        ├── ppsspp_libretro.dll
        └── ...
```
## ⚖️ Licença e Créditos
Este projeto foi desenvolvido por Thiago Aciole. Feito com ❤️ usando CustomTkinter e Python.
