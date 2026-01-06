import os

import pygame

from .paths import get_asset_path


class AudioManager:
    _initialized = False
    _sounds = {}  # Cache para carregar sons curtos

    @classmethod
    def init_mixer(cls):
        """Inicia o mixer do pygame se ainda não foi iniciado"""
        if not cls._initialized:
            try:
                # frequency=44100, size=-16, channels=2, buffer=512
                # Buffer baixo ajuda na resposta rápida dos cliques
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                cls._initialized = True
            except Exception as e:
                print(f"Erro ao iniciar sistema de áudio: {e}")

    @classmethod
    def play_bgm(cls, filename="bgm.mp3", volume=0.5):
        """Toca a música de fundo em loop"""
        cls.init_mixer()
        music_path = get_asset_path(filename)

        if not os.path.exists(music_path):
            print(f"⚠️ Música não encontrada: {music_path}")
            return

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops=-1, fade_ms=2000)
        except Exception as e:
            print(f"Erro ao tocar música: {e}")

    @classmethod
    def play_sound(cls, filename):
        """Toca um efeito sonoro curto (SFX)"""
        cls.init_mixer()

        # Carrega no cache se não estiver lá
        if filename not in cls._sounds:
            path = get_asset_path(filename)
            if os.path.exists(path):
                try:
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(0.5)
                    cls._sounds[filename] = sound
                except:
                    cls._sounds[filename] = None
            else:
                return

        # Toca o som
        sound_obj = cls._sounds.get(filename)
        if sound_obj:
            sound_obj.play()

    @classmethod
    def stop(cls):
        """Para a música de fundo"""
        if cls._initialized:
            try:
                pygame.mixer.music.stop()
            except Exception as e:
                print(f"Erro ao parar música: {e}")

    @classmethod
    def set_volume(cls, volume):
        """Ajusta o volume da música em tempo real"""
        if cls._initialized:
            try:
                pygame.mixer.music.set_volume(volume)
            except:
                pass
