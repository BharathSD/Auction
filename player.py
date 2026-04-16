import pandas as pd
import os
from urllib.parse import urlparse
from urllib.parse import unquote

class Player:
  def __init__(self, name, gender, bowling_rating, batting_rating, photo_path, uid) -> None:
    self.name = name
    self.gender = gender
    self.bowling_rating = bowling_rating
    self.batting_rating = batting_rating
    self.photo_path = photo_path
    self.base_price = 5000
    self.uid = uid
    self.is_sold = False
    self.sold_for = 'NA'
    self.team_name = 'NA'
  
  def set_sold_for(self, cost):
    self.sold_for = cost
    self.is_sold = True
  
  def set_team_name(self, team_name):
    self.team_name = team_name
  
  def is_player_sold(self):
    return self.team_name != "NA"

class CaptainClass:
  def __init__(self, name, max_num_of_players, initial_budget=150000) -> None:
    self.name = name
    self.max_num_of_players = max_num_of_players
    self.playersList = [None] * max_num_of_players
    self.num_of_players_selected = 0
    self.remaining_cap = int(initial_budget)

  def add_player(self, player: Player):
    if self.num_of_players_selected < self.max_num_of_players:
      self.playersList[self.num_of_players_selected] = player
      self.remaining_cap -= int(player.sold_for)
      self.num_of_players_selected += 1
  
  def get_playerList(self):
    return self.playersList
  
  def is_cap_remaining(self, cost):
    cost_after_deduction = self.remaining_cap - cost
    return cost_after_deduction >= 0
  
class PlayerManager:
  def __init__(self, config=None) -> None:
    self.config = config or {}
    self.players = dict()
    self.file_name = self.config.get('player_data_file', 'PL_Safety_Box_Cricket_League.xlsx')
    self.availability_column = self.config.get('availability_column', 'Availbale')
    self.read_data()
    self.createPlayers()
    self.playerKeys = list(self.players.keys())
    self.cur_index = 0
    self.max_index = len(self.playerKeys)
  
  def read_data(self):
    if not os.path.exists(self.file_name):
      raise FileNotFoundError(f"Player data file not found: {self.file_name}")

    self.df = pd.read_excel(self.file_name)
    self.df_orig = self.df.copy()

    required_columns = {
      'UID',
      'Photo',
      'Name',
      'Gender',
      'Bowl_rating',
      'Bat_rating',
      self.availability_column,
    }
    missing_columns = [col for col in required_columns if col not in self.df.columns]
    if missing_columns:
      missing_cols = ', '.join(missing_columns)
      raise ValueError(f"Missing required columns in {self.file_name}: {missing_cols}")

    columns_2_delete = ['ID', 'Start time', 'Completion time', 'Email', 'Last modified time', 'Name2', 
                        'Extracted uid',"Are the Uid's Same", 'Reporting Manager', 'Mobile No']
    self.df.drop(columns=columns_2_delete, inplace=True, errors='ignore')
    self.df.set_index('UID', inplace=True)

    # filter the columns based on Availability
    column_2_filter = self.availability_column
    self.df = self.df[self.df[column_2_filter] == 'Yes']
    self.df.drop(columns=[column_2_filter], inplace=True)
   
  def createPlayers(self):
    for index, row in self.df.iterrows():
      a = urlparse(unquote(row['Photo']))
      file_name = os.path.basename(a.path)
      self.players[index] = Player(name= row['Name'], gender=row['Gender'], 
                                    bowling_rating=row['Bowl_rating'], 
                                    batting_rating= row['Bat_rating'], 
                                    photo_path= file_name, uid=index)
  
  def get_curr_player(self):
    return self.players[self.playerKeys[self.cur_index]]
  
  def get_next_player(self):
    player = None
    if self.cur_index < self.max_index - 1:
      self.cur_index += 1
      player = self.players[self.playerKeys[self.cur_index]]
    return player
  
  def get_previous_player(self):
    player = None
    if self.cur_index > 0:
      self.cur_index -= 1
      player = self.players[self.playerKeys[self.cur_index]]
    return player
  
  def check_if_player_exist(self, player_uid):
    return player_uid in self.playerKeys

