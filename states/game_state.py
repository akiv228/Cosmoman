from abc import ABC, abstractmethod

class State(ABC):
    def __init__(self, game):
        self.game = game

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

    @abstractmethod
    def enter(self):
        pass
