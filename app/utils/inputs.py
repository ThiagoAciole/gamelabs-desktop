class InputManager:
    """
    Gerencia a ligação entre teclas físicas (e futuramente botões de joystick)
    e as funções do aplicativo.
    """

    def __init__(self, master_window):
        self.root = master_window

        # Mapeamento inicial de TECLADO
        # No futuro, você pode mapear botões do Joystick aqui
        self.key_map = {
            "LEFT": ["<Left>"],
            "RIGHT": ["<Right>"],
            "CONFIRM": ["<Return>", "<KP_Enter>", "<space>"],  # Enter ou Espaço
            "BACK": ["<Escape>", "<BackSpace>"],
        }

    def bind_screen_controls(
        self, on_left=None, on_right=None, on_confirm=None, on_back=None
    ):
        """
        Vincula as ações (Esquerda, Direita, etc) às funções da tela atual.
        Sempre que uma tela é carregada, ela deve chamar essa função.
        """

        # Função auxiliar para limpar binds antigos e setar novos
        def bind_action(action_name, callback):
            keys = self.key_map.get(action_name, [])
            for key in keys:
                # Primeiro removemos bind anterior para evitar conflito (opcional, mas seguro)
                self.root.unbind(key)
                if callback:
                    self.root.bind(key, lambda event: callback())

        # Aplica os bindings
        bind_action("LEFT", on_left)
        bind_action("RIGHT", on_right)
        bind_action("CONFIRM", on_confirm)
        bind_action("BACK", on_back)

    # --- ESPAÇO RESERVADO PARA JOYSTICK ---
    # No futuro, você criará um método "check_gamepad_loop" aqui
    # que roda num self.root.after(...) verificando inputs do PyGame
    # e chamando as funções on_left, on_right, etc.
