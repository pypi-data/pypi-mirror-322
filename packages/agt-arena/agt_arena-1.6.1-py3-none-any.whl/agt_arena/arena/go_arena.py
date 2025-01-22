import os
import logging
from typing import Dict, List
import requests
import time
from datetime import datetime
from agt_arena.matchmaker.elo import EloMatchmaker
from agt_arena.game.go.go_search_problem import GoState, GoProblem
import json
import docker
from tqdm import tqdm

class GoArena:
    def __init__(self, submission_ids: List[int], board_size, setupTimeout: int = 5, totalMoveTimeout: int = 15, grace_time_per_move: float = 0.05, port = 5000):
        """
        Args:
            submission_ids: List of unique id submissions
            board_size: Size of the Go board
            setupTimeout: Timeout in seconds for bot setup
            totalMoveTimeout: Total timeout in seconds for all moves
            grace_time_per_move: Additional grace time added to the total time after each move
        """
        
        self.bot_names = {}
        self.bot_urls = {}
        self.board_size = board_size
        self.setupTimeout = setupTimeout
        self.totalMoveTimeout = totalMoveTimeout
        self.grace_time_per_move = grace_time_per_move
        self.port = port
        self.health_checks(submission_ids)
        
        # Setup logging with timestamped filenames
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"logs/go/tournament_{timestamp}.log"
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        
        self.totals_path = "meta/go/totals.json"
        self.results_path = "meta/go/results.json"
    
    def health_checks(self, submission_ids): 
        for bot_id in tqdm(submission_ids, desc = "Running Health Checks"): 
            _, url = GoArena.build_and_run_container(bot_id, self.port, self.board_size)
            print(f"URL sucessfully built: {url}")
            try: 
                name = self.health_check(url)
                print(name)
                if name:
                    print(f"{name} has sucessfully joined to the arena")
                    self.bot_names[bot_id] = name
                    self.bot_urls[bot_id] = url
                    
                else:
                    print(f"Health check failed for bot-id: {bot_id}")
            finally: 
                GoArena.cleanup_container_and_image(bot_id)
            
    
    def health_check(self, url): 
        try:
            response = requests.get(f"{url}/health", timeout=15)
            if response.status_code == 200:
                status = response.json()
                if status.get("status") == "healthy" and "name" in status and isinstance(status["name"], str):
                    return status["name"]
            return None
        except requests.exceptions.RequestException as e:
            print(f"Health check failed for {url}: {e}")
            return None
        
        
    def build_and_run_container(bot_id, app_port, board_size, delay = 10):
        client = docker.from_env()
        image_name = f"bot_{bot_id}"
        container_name = f"bot_container_{bot_id}"
        bot_port = app_port  # Port for this bot

        # Build the Docker image
        print(f"Building Docker image for bot {bot_id}...")
        try:
            build_logs = client.api.build(
                path=os.path.abspath("./"),
                dockerfile=os.path.abspath(f"./submissions/go/submissions/{bot_id}/Dockerfile"),
                tag=image_name,
                rm=True,
                decode=True
            )
            for log in build_logs:
                if 'stream' in log:
                    print(log['stream'].strip())
                elif 'error' in log:
                    print(f"Build error: {log['error']}")
            print(f"Image for bot {bot_id} built successfully.")
        except docker.errors.BuildError as e:
            print(f"Error building image for bot {bot_id}: {e}")
            return None, None

        # Check if the image exists locally
        try:
            client.images.get(image_name)
        except docker.errors.ImageNotFound:
            print(f"Image {image_name} was not found after building. Exiting.")
            return None, None

        # Run the container
        print(f"Starting container for bot {bot_id}...")
        try:
            container = client.containers.run(
                image_name,
                name=container_name,
                detach=True,
                environment={
                    "BOT_PORT": bot_port,
                    "FLASK_ENV": "development",
                    "FLASK_DEBUG": "1",
                    "BOARD_SIZE": board_size,
                },
                healthcheck={
                    "test": ["CMD", "curl", "-f", f"http://{container_name}:{bot_port}/health"],
                    "interval": int(5e9),  # 5 seconds
                    "timeout": int(3e9),   # 3 seconds
                    "retries": 3,
                },
                volumes={
                    "/Users/johnwu/Documents/Brown CS/cs410_arena/logs/go": {"bind": "/logs", "mode": "rw"},
                },
                network="tournament",
                tty=True,
                stdin_open=True
            )
            print(f"Container for bot {bot_id} is running.")
            time.sleep(delay)
            return container, f"http://{container_name}:{bot_port}"
        except docker.errors.APIError as e:
            print(f"Error starting container for bot {bot_id}: {e}")
            return None, f"http://{container_name}:{bot_port}"


    def cleanup_container_and_image(bot_id):
        client = docker.from_env()
        container_name = f"bot_container_{bot_id}"
        image_name = f"bot_{bot_id}"

        #Stop and remove container
        # print(f"Stopping and removing container for bot {bot_id}...")
        # try:
        #     container = client.containers.get(container_name)
        #     container.stop()
        #     container.remove()
        # except Exception as e:
        #     print(f"Error cleaning up container {container_name}: {e}")

        # # Remove image
        # print(f"Removing image for bot {bot_id}...")
        # try:
        #     client.images.remove(image_name, force=True)
        # except Exception as e:
        #     print(f"Error removing image {image_name}: {e}")
            
    def setup_bot(self, bot_url: str, player: int) -> bool:
        try:
            response = requests.post(
                f"{bot_url}/setup",
                json={'player': player},
                timeout=self.setupTimeout
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logging.error(f"Error setting up bot at {bot_url}: {e}")
            return False

    def get_bot_move(self, bot_url: str, game_state: GoState, time_remaining: float) -> int:
        try:
            start_time = time.time()
            print(game_state.serialize())
            response = requests.post(
                f"{bot_url}/get_move",
                json={
                    'game_state': game_state.serialize(),
                    'time_remaining': time_remaining 
                },
                timeout=min(self.totalMoveTimeout, time_remaining)
            )
            elapsed_time = time.time() - start_time
            move_data = response.json()['move']
            return move_data, elapsed_time
        except requests.exceptions.RequestException as e:
            logging.error(f"Error getting move from bot at {bot_url}: {e}")
            return -1, 0
        except Exception as e:
            logging.error(f"Bot at {bot_url} encountered an error: {e}")
            return -1, 0

    def save_sgf(self, moves, black_bot, white_bot):
        """Save the match to an SGF file."""
        try: 
            sgf_data = "(;GM[1]FF[4]SZ[{}]PB[{}]PW[{}]".format(self.board_size, black_bot, white_bot)
            count = 0
            for move in moves:
                row, col = divmod(move, self.board_size)
                sgf_move = f";B[{chr(97 + col)}{chr(97 + row)}]" if count % 2 == 1 else f";W[{chr(97 + col)}{chr(97 + row)}]"
                sgf_data += sgf_move
                count += 1
            sgf_data += ")"

            # Create directories for each bot
            black_dir = os.path.join("logs/go", black_bot)
            white_dir = os.path.join("logs/go", white_bot)
            os.makedirs(black_dir, exist_ok=True)
            os.makedirs(white_dir, exist_ok=True)

            # Save SGF files in each bot's directory
            match_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            black_sgf_path = os.path.join(black_dir, f"{match_timestamp}_vs_{white_bot}.sgf")
            white_sgf_path = os.path.join(white_dir, f"{match_timestamp}_vs_{black_bot}.sgf")

            with open(black_sgf_path, "w") as black_file, open(white_sgf_path, "w") as white_file:
                black_file.write(sgf_data)
                white_file.write(sgf_data)
        except:
            pass
    

    def run_match(self, black_bot: str, black_bot_id: int, white_bot: str, white_bot_id: int) -> dict:
        """Run a single match between two bots"""
        _, black_bot_url = GoArena.build_and_run_container(black_bot_id, self.port, self.board_size)
        _, white_bot_url = GoArena.build_and_run_container(white_bot_id, self.port, self.board_size)
        
        my_go = GoProblem(size=self.board_size)
        state = my_go.start_state
        remaining_time = {black_bot_url: self.totalMoveTimeout, white_bot_url: self.totalMoveTimeout}
        move_counts = 0

        moves = []
        
        try: 
            current_bot_url = black_bot_url
        
            while not my_go.is_terminal_state(state):
                move, elapsed_time = self.get_bot_move(current_bot_url, state, remaining_time[current_bot_url])
                print(move, elapsed_time)
                
                if move not in state.legal_actions() or elapsed_time > (remaining_time[current_bot_url] + self.grace_time_per_move):
                    logging.error(f"Bot at {current_bot_url} ran out of time or failed to provide a move.")
                    return {
                        'winner': 'white' if current_bot_url == black_bot_url else 'black',
                        'resigned': True,
                        'duration': elapsed_time, 
                        'move_counts': move_counts
                    }
                    
                moves.append(move)
                move_counts += 1

                # Update remaining time and add grace time
                remaining_time[current_bot_url] -= elapsed_time
                remaining_time[current_bot_url] = min(
                    remaining_time[current_bot_url] + self.grace_time_per_move, self.totalMoveTimeout
                )

                state = my_go.transition(state, move)
                current_bot_url = white_bot_url if current_bot_url == black_bot_url else black_bot_url

            result = state.terminal_value()
            
            self.save_sgf(moves, black_bot, white_bot)
            
            return {
                'winner': 'black' if result[0] > 0 else 'white',
                'score': str(result),
                'duration': elapsed_time,
                'move_counts': move_counts
            }
        finally:
            GoArena.cleanup_container_and_image(white_bot_id)
            GoArena.cleanup_container_and_image(black_bot_id)

    def run_tournament(self) -> List[dict]:
        """Run a round-robin tournament between all bots"""
        results = []
        bot_ids = list(self.bot_names.keys())
        
        try:
            # Load existing stats from totals_path
            with open(self.totals_path, "r") as f:
                existing_stats = json.load(f)
        except FileNotFoundError:
            # If totals_path doesn't exist, start fresh
            existing_stats = {}

        # Initialize bot stats, loading from existing stats if available, or using defaults otherwise
        bot_stats = {
            bot_id: existing_stats.get(
                bot_id, 
                {'wins': 0, 'losses': 0, 'total_score': 0.0, 'matches': 0, 'total_moves': 0, 'total_duration': 0.0}
            )
            for bot_id in bot_ids
        }
    
        matchmaker = EloMatchmaker(order_matters=True, meta_file=self.totals_path)
        matchmaker.add_new_bots(bot_ids)
        matchups = matchmaker.generate_matches(bot_ids)
        num_matchups = matchmaker.n_closest * len(bot_ids)

    
        for black_bot_id, white_bot_id in tqdm(matchups, desc="Running matches", total=num_matchups):
            black_bot = self.bot_names[black_bot_id]
            white_bot = self.bot_names[white_bot_id]
            print(f"\nStarting match: {black_bot} (B) vs {white_bot} (W)")
            result = self.run_match(black_bot, black_bot_id, white_bot, white_bot_id)

            if 'error' in result:
                logging.error(f"Error in match: {result['error']}")
                continue

            result.update({'black': black_bot, 'white': white_bot})
            results.append(result)
            logging.info(f"Match {black_bot} (B) vs {white_bot} (W) Result: {result}")

            # Update bot stats
            bot_stats[black_bot_id]['name'] = black_bot
            bot_stats[white_bot_id]['name'] = white_bot
            
            bot_stats[black_bot_id]['matches'] += 1
            bot_stats[white_bot_id]['matches'] += 1

            winner = result['winner']                 
            loser = black_bot_id if winner == 'white' else white_bot_id
            winner = black_bot_id if winner == 'black' else white_bot_id
            bot_stats[winner]['wins'] += 1
            bot_stats[loser]['losses'] += 1
            
            matchmaker.update_elo(winner = winner, loser = loser)
            bot_stats[black_bot_id]['elo'] = matchmaker.get_elo(black_bot_id)

            bot_stats[black_bot_id]['total_duration'] += result['duration']
            bot_stats[white_bot_id]['total_duration'] += result['duration']
            
            bot_stats[black_bot_id]['total_moves'] += result['move_counts']
            bot_stats[white_bot_id]['total_moves'] += result['move_counts']
            
            with open(self.totals_path, "w") as f:
                json.dump(bot_stats, f, indent=4)
        
        # Log detailed bot statistics
        results_data = {}
        for bot, stats in tqdm(bot_stats.items(), desc="Calculating Stats"):
            avg_score = stats['total_score'] / stats['matches'] if stats['matches'] > 0 else 0.0
            avg_moves = stats['total_moves'] / stats['matches'] if stats['matches'] > 0 else 0.0
            avg_dur = stats['total_duration'] / stats['matches'] if stats['matches'] > 0 else 0.0
            elo = matchmaker.get_elo(bot)
            logging.info(f"Bot {stats['name']}: Wins: {stats['wins']}, Losses: {stats['losses']}, Average Score: {avg_score}, Average Moves per Game: {avg_moves}, Average Duration: {avg_dur}, Elo: {elo}")
            results_data[bot] = {
                "name": stats['name'],
                "average_score": (stats["wins"] - stats['losses']) / stats["matches"] if stats["matches"] > 0 else 0.0,
                "average_moves": stats["total_moves"] / stats["matches"] if stats["matches"] > 0 else 0.0,
                "average_duration": stats["total_duration"] / stats["matches"] if stats["matches"] > 0 else 0.0,
                "elo": elo
            }
            
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_path_timestamp = f"{self.results_path.rstrip('.json')}_{timestamp}.json"
        with open(results_path_timestamp, "w") as f:
            json.dump(results_data, f, indent=4)

        return results
