from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    def __init__(self, params):
        self.params = params

    @abstractmethod
    def generate_signal(self, df: pd.DataFrame):
        """
        Receives data, returns a signal.
        Returns: None, 'BUY', or 'SELL'
        """
        pass