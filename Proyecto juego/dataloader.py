import json

class GameDataLoader:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.game_data = None
        self.load_data()

    def load_data(self):
        try:
            with open(self.json_file_path, 'r') as file:
                self.game_data = json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{self.json_file_path}' not found.")

    def get_stage_data(self, stage_name):
        try:
            return self.game_data['stages'][stage_name]
        except KeyError:
            print(f"Error: Stage '{stage_name}' not found in the JSON data.")
            return None

    def get_player_data(self, stage_name):
        stage_data = self.get_stage_data(stage_name)
        if stage_data:
            try:
                return stage_data['player']
            except KeyError:
                print(f"Error: Player data not found for stage '{stage_name}'.")
                return None
        else:
            return None

    def get_enemy_data(self, stage_name):
        stage_data = self.get_stage_data(stage_name)
        if stage_data:
            try:
                return stage_data['enemies']
            except KeyError:
                print(f"Error: Enemy data not found for stage '{stage_name}'.")
                return None
        else:
            return None
