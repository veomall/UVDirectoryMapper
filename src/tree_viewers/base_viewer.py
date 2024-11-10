from abc import ABC, abstractmethod


class BaseViewer(ABC):
    @abstractmethod
    def view(self, path):
        pass
