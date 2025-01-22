import itertools
from agt_arena.matchmaker.base_matchmaker import BaseMatchmaker
import os 
import json


class EloMatchmaker(BaseMatchmaker):
    def __init__(self, n_closest=3, k_factor=32, order_matters=False, meta_file="meta/results.json"):
        super().__init__()
        self.n_closest = n_closest
        self.k_factor = k_factor
        self.order_matters = order_matters
        self.meta_file = meta_file
        
        self.load_meta_file()
        
    def load_meta_file(self):
        """Load ELO data from the meta file if it exists."""
        if os.path.exists(self.meta_file):
            try:
                with open(self.meta_file, "r") as file:
                    data = json.load(file)
                for bot, results in data.items():
                    elo = results['elo']
                    self.bot_data[bot] = {"elo": elo}
            except Exception as e:
                print(f"Error reading meta file {self.meta_file}: {e}")

    def update_elo(self, winner, loser):
        """Update ELO scores based on match results"""
        winner_elo = self.bot_data[winner]["elo"]
        loser_elo = self.bot_data[loser]["elo"]

        # Expected scores
        winner_expected = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
        loser_expected = 1 - winner_expected

        self.bot_data[winner]["elo"] += self.k_factor * (1 - winner_expected)
        self.bot_data[loser]["elo"] += self.k_factor * (0 - loser_expected)
        
    
    def get_elo(self, player): 
        return self.bot_data[player]["elo"]

    def add_new_bots(self, players):
        """Add bots to the matchmaker with default ELO if they don't already exist"""
        os.makedirs(os.path.dirname(self.meta_file), exist_ok=True)
        
        for bot in players:
            if bot not in self.bot_data:
                self.bot_data[bot] = {"elo": 1500}

    def generate_matches(self, players):
        """Generate matches for the closest n bots based on ELO (Generator)"""
        for bot in players:
            sorted_bots = sorted(
                [p for p in players if p != bot],
                key=lambda other: abs(self.bot_data[bot]["elo"] - self.bot_data[other]["elo"])
            )

            for opponent in sorted_bots[:self.n_closest]:
                yield (bot, opponent)
                if self.order_matters:
                    yield (opponent, bot)
