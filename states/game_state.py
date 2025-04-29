from abc import ABC, abstractmethod
import pygame as pg

class State(ABC):
    def __init__(self, game):
        self.game = game  # Ссылка на класс Game для доступа к окну и переключению состояний

    @abstractmethod
    def handle_events(self, events):
        """Обрабатывает события (нажатия клавиш, клики мыши)."""
        pass

    @abstractmethod
    def update(self):
        """Обновляет логику состояния."""
        pass

    @abstractmethod
    def render(self, window):
        """Отрисовывает элементы состояния."""
        pass

