import os
import sys
import numpy as np
from datetime import datetime
from agt_server.agents.base_agents.rps_agent import RPSAgent


class RPSBot(RPSAgent):
    def _redirect_logs(self):
        """Redirect logs to a timestamped file for easier debugging."""
        log_dir = os.path.join("logs", self.name)
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = open(os.path.join(log_dir, f"{timestamp}.log"), "a")
        sys.stdout = log_file
        sys.stderr = log_file
        print(f"Logging started for bot: {self.name}")

    def on_start(self, player_data):
        """Called at the start of each match"""
        self.match_data = {}
        self._redirect_logs()
        self.match_data['player'] = player_data['player']
        self.setup()
    
    def __str__(self): 
        return self.name 
    
    def __repr__(self):
        return str(self)
    
    