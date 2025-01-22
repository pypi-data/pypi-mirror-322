import os
import json
import docker
import requests
import logging
from datetime import datetime
from itertools import combinations
import numpy as np
import pandas as pd
from tqdm import tqdm
from agt_server.local_games.base import LocalArena

class RPSDockerArena(LocalArena):
    def __init__(self, num_rounds=10, submission_ids=[], timeout=5, handin=False, logging_path=None, save_path=None):
        super().__init__(num_rounds, [], timeout, handin, logging_path, save_path)
        self.game_name = "Rock, Paper, Scissors"
        self.valid_actions = [0, 1, 2]
        self.utils = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
        self.invalid_move_penalty = -1
        self.submission_ids = submission_ids

        self.client = docker.from_env()
        self.players = self.setup_players()

    def setup_players(self):
        players = []
        for bot_id in tqdm(self.submission_ids, desc="Setting up players"):
            container, url = self.build_and_run_container(bot_id, 5000 + bot_id)
            if container:
                players.append({"id": bot_id, "url": url, "container": container})
            else:
                logging.warning(f"Failed to initialize bot {bot_id}")
        return players

    def build_and_run_container(self, bot_id, port):
        image_name = f"rps_bot_{bot_id}"
        container_name = f"rps_container_{bot_id}"

        # Build the container
        try:
            self.client.images.build(
                path=f"./submissions/rps/{bot_id}/",
                dockerfile="Dockerfile",
                tag=image_name
            )
            print(f"Built image for bot {bot_id}")
        except docker.errors.BuildError as e:
            logging.error(f"Error building container {bot_id}: {e}")
            return None, None

        # Run the container
        try:
            container = self.client.containers.run(
                image_name,
                name=container_name,
                detach=True,
                ports={'5000/tcp': port},
                environment={"BOT_PORT": port},
                network="rps_tournament_network"
            )
            return container, f"http://localhost:{port}"
        except docker.errors.APIError as e:
            logging.error(f"Error running container {bot_id}: {e}")
            return None, None

    def cleanup_players(self):
        for player in self.players:
            try:
                player["container"].stop()
                player["container"].remove()
            except Exception as e:
                logging.warning(f"Failed to remove {player['id']}: {e}")

    def run_game(self, p1, p2):
        p1_url, p2_url = p1["url"], p2["url"]
        p1_total_util, p2_total_util = 0, 0

        for _ in range(self.num_rounds):
            p1_action = self.get_bot_action(p1_url)
            p2_action = self.get_bot_action(p2_url)

            self.game_reports[p1["id"]]["action_history"].append(p1_action)
            self.game_reports[p2["id"]]["action_history"].append(p2_action)

            p1_util, p2_util = self.calculate_utils(p1_action, p2_action)
            self.game_reports[p1["id"]]["util_history"].append(p1_util)
            self.game_reports[p2["id"]]["util_history"].append(p2_util)

            p1_total_util += p1_util
            p2_total_util += p2_util

        print(f"Game {p1['id']} vs {p2['id']} finished.")

    def get_bot_action(self, bot_url):
        try:
            response = requests.post(f"{bot_url}/get_action", timeout=self.timeout)
            if response.status_code == 200:
                return response.json().get("action", -1)
        except requests.RequestException:
            logging.error(f"Bot at {bot_url} failed to respond.")
            return -1

    def run(self):
        for p1, p2 in combinations(self.players, 2):
            self.run_game(p1, p2)

        self.cleanup_players()
        return self.summarize_results()

    def summarize_results(self):
        agent_names = [str(player['id']) for player in self.players]
        df = pd.DataFrame(self.result_table, columns=agent_names, index=agent_names)

        # Add final utility columns
        df["Final Utility"] = [self.final_utilities[player['id']] for player in self.players]
        df["Average Utility"] = df.sum(axis=1) / (len(self.players) - 1)

        if self.save_path:
            df.to_csv(self.save_path)

        print("\nFinal Results:\n")
        print(df.to_string())

        return df
