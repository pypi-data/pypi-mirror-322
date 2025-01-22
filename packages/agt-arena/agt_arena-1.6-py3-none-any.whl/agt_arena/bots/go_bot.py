from abc import ABC, abstractmethod
import pyspiel
import os
from datetime import datetime
import sys

class GoBot(ABC):
    def _redirect_logs(self):
        """
        Redirects stdout and stderr to a log file named `{name}_bot_{timestamp}.log`.
        Writes logs to the `/logs` directory.
        """
        os.makedirs("/logs", exist_ok=True)
        os.makedirs(f"/logs/{self.name}", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"/logs/{self.name}/{timestamp}.log"
        log_file = open(log_filename, "a")

        sys.stdout = log_file
        sys.stderr = log_file

        print(f"Logging started for bot: {self.name}")
    
    def on_start(self, player_data):
        """Called at the start of each match"""
        self.match_data = {}
        self._redirect_logs()
        self.match_data['player'] = player_data['player']
        self.setup()

    def on_update(self, game_state: pyspiel.State):
        """Called after each move is made"""
        self.update(game_state)

    def get_action(self, game_state: pyspiel.State) -> int:
        """Main method to get the bot's next move"""
        return self.get_move(game_state)

    def setup(self):
        """Override to add custom match start logic"""
        pass

    def update(self, game_state: pyspiel.State, last_move: int):
        """Override to add custom move tracking logic"""
        pass

    @abstractmethod
    def get_move(self, game_state: pyspiel.State, time_remaining: int) -> int:
        """Select a move given the current game state"""
        pass
    
    def __repr__(self):
        return str(self)