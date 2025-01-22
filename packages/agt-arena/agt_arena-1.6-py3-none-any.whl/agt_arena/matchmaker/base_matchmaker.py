from abc import ABC, abstractmethod

class BaseMatchmaker(ABC):
    """
    Abstract base class for all matchmakers.
    """
    
    def __init__(self):
        self.bot_data = {}

    def update_bot_data(self, bot, data):
        """Update data for a bot (e.g., ELO)"""
        if bot not in self.bot_data:
            raise ValueError(f"Bot {bot} is not registered.")
        self.bot_data[bot].update(data)

    @abstractmethod
    def generate_matches(self, players):
        """
        Generate a list of matches from the given players.
        Args:
            players: List of players (e.g., ["Player 1", "Player 2", ...]).
        Returns:
            List of matches, where each match is a tuple of players.
        """
        pass