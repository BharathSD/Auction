from tkinter import *
from  tkinter import ttk
import json
import urllib.request
from io import BytesIO

from PIL import Image, ImageTk
from button import AuctionButtonClass
from star import StarCanvasClass
from playerTable import PlayerTableClass
from player import PlayerManager, CaptainClass
import pandas as pd
import os
from pathlib import Path
from PIL import ImageFont, ImageDraw

CONFIG_FILE_NAME = "AuctionConfig.json"

class RemaningCapLabelClass:
  def __init__(self, root, grid_row, grid_col, text) -> None:
    self.root =  root
    self.grid_row = grid_row
    self.grid_col = grid_col
    self.foreground_color = "black"
    self.textfont =('calibri', 13, 'bold', 'italic')
    self.button_height = 2
    self.button_width = 20
    self.lbl = None
    self.create_label(text)

  def create_label(self, text):
    self.lbl = Label(self.root,  text=text, fg = self.foreground_color,
                     font = self.textfont, relief= 'ridge',
                     height= self.button_height, width= self.button_width)
    self.lbl.grid(column=self.grid_col, row=self.grid_row)
  
  def update_remaining_budget(self, text):
    self.lbl.config(text=text)
    
class DisplayWindow:
  def __init__(self, AuctionMgr) -> None:

    self.AuctionMgr = AuctionMgr

    self.root = Tk()

    # set the title and dimension
    self.root.title("PL Safety Box Cricket League")

    # Set geometry (widthxheight)
    self.root.geometry('1536x1152')

    self.add_headerLabel()

    self.captains_buttons = dict()
    self.RemainingCapLabel = dict()
    self.CreateCaptainsButtonAndLabel()
    self.image_folder = self.AuctionMgr.config.get('images_folder', 'images')
    self.ImageLabel = None
    image = self.get_opening_image()
    
    self.CreateImageLabel(image)

    self.Name = None # Name of the player
    self.Batting_Rating = None # Batting rating
    self.Bowling_Rating = None # Bowling rating
    self.BasePrice = None # Base Price of the Player
    self.SoldForPrice = None # Sold for Price
    self.SelectedCaptain = None # Selected Captain
    self.AddPlayerProfileLabels()

    # Tree view for plyers selected
    self.PlayerTable = None
    self.createTable()

    # Add load Auction label
    self.load_auction_button = None
    self.createLoadAuctionButton()

    self.load_pre_auction_buttion = None
    self.createLoadPreAuctionButton()

    # direction buttons
    self.createDirectionButtons()

    # Auction profile
    self.current_auction_Cap = None
    self.current_bid = None
    self.AddAuctionDetails()

    # Sold Button
    self.sold_button = None
    self.AddSoldButton()

    # Undo Button
    self.undo_button = None
    self.AddUndoButton()

    self.is_load_acution = False

  def add_headerLabel(self):
    lbl = Label(self.root,  text="Cricket League -  Auction",
                fg = "light green", bg = "dark green",
                font = "Helvetica 35 bold italic", borderwidth=2, relief= 'ridge')
    lbl.grid(row=0, column=0, columnspan=8)


  def CreateCaptainsButtonAndLabel(self):
    for cap_cnt, captain_name in enumerate(self.AuctionMgr.captains_dict):
      captain = self.AuctionMgr.captains_dict[captain_name]
      self.captains_buttons[captain.name] = AuctionButtonClass(root=self, display_text=captain.name, grid_row=2, grid_col=cap_cnt)
      self.RemainingCapLabel[captain.name] = RemaningCapLabelClass(root=self.root, grid_row=3, grid_col=cap_cnt, 
                                                                   text=str(captain.remaining_cap))

  def CreateImageLabel(self, image):
    # Create a PhotoImage object from the image
    photo_image = ImageTk.PhotoImage(image)
    self.ImageLabel = Label(self.root, image=photo_image, borderwidth=5, relief= 'ridge', height=300, width=550)
    self.ImageLabel.grid(column=0, row=4, columnspan=3, rowspan=7)
    self.ImageLabel.image = photo_image

  def AddPlayerProfileLabels(self):
    textfont =('calibri', 20, 'bold')

    # Name of the player
    Name_label = Label(self.root, borderwidth=5, relief= 'ridge', text='Name:', font=textfont, anchor="w", 
                       width=13, background='silver')
    Name_label.grid(column=3, row=4, sticky = W)
    self.Name = Label(self.root, borderwidth=5, relief= 'ridge', text='Name of the player', font=textfont, justify="left",
                      anchor="w", width=26)
    self.Name.grid(column=4, row=4, columnspan=2, sticky = W)

    # Player Profile
    player_profile = Label(self.root, borderwidth=5, relief= 'ridge', text='PLAYER PROFILE', font=textfont, justify="center",
                           anchor="n", width=40, background='silver')
    player_profile.grid(column=3, row=5, columnspan=3, sticky = N)

    # Batting Ability
    Batting_Rating_label = Label(self.root, borderwidth=5, relief= 'ridge', text='Batting Ability:', font=textfont,
                                 anchor="w", width=13, background='silver')
    Batting_Rating_label.grid(column=3, row=6, sticky = W)
    self.Batting_Rating =  StarCanvasClass(self.root,grid_col=4, grid_row=6)

    # Bowling Ability
    Bowling_Rating_label = Label(self.root, borderwidth=5, relief= 'ridge', text='Bowling Ability:',
                                 font=textfont, anchor="w", width=13, background='silver')
    Bowling_Rating_label.grid(column=3, row=7, sticky = W)
    self.Bowling_Rating = StarCanvasClass(self.root,grid_col=4, grid_row=7)

    # Base price
    BasePrice_label = Label(self.root, borderwidth=5, relief= 'ridge', text='Base Price:',
                            font=textfont, anchor="w", width=13, background='silver')
    BasePrice_label.grid(column=3, row=8, sticky = W)
    self.BasePrice = Label(self.root, borderwidth=5, relief= 'ridge', text='NA',
                           font=textfont, justify="left", anchor="w", width=26)
    self.BasePrice.grid(column=4, row=8, columnspan=2, sticky = W)

    # Sold For 
    SoldFor_label = Label(self.root, borderwidth=5, relief= 'ridge', text='Sold For:',
                          font=textfont, anchor="w", width=13, background='silver')
    SoldFor_label.grid(column=3, row=9, sticky = W)
    self.SoldForPrice = Label(self.root, borderwidth=5, relief= 'ridge', text='NA',
                           font=textfont, justify="left", anchor="w", width=26)
    self.SoldForPrice.grid(column=4, row=9, columnspan=2, sticky = W)
    
    # Selected Captain
    SelectedCaptain_label = Label(self.root, borderwidth=5, relief= 'ridge', text='Team:',
                                  font=textfont, anchor="w", width=13, background='silver')
    SelectedCaptain_label.grid(column=3, row=10, sticky = W)
    self.SelectedCaptain = Label(self.root, borderwidth=5, relief= 'ridge', text='NA',
                           font=textfont, justify="left", anchor="w", width=26)
    self.SelectedCaptain.grid(column=4, row=10, columnspan=2, sticky = W)

  def createTable(self):
    table_columnspan = max(1, len(self.AuctionMgr.captains_dict))
    self.PlayerTable = PlayerTableClass(self.root, 11, 0, self.AuctionMgr.captains_dict, table_columnspan)

  def get_opening_image(self):
    poster_file = self.AuctionMgr.config.get('poster_image_file')
    if poster_file and os.path.exists(poster_file):
      image = Image.open(poster_file)
      return image.resize((int(image.size[0]/5), int(image.size[1]/5)))
    return self.get_placeholder_image('Auction', size=(300, 300))

  def get_placeholder_image(self, text, size=(150, 250)):
    image = Image.new('RGB', size, color=(220, 220, 220))
    draw = ImageDraw.Draw(image)
    draw.rectangle((5, 5, size[0] - 5, size[1] - 5), outline=(120, 120, 120), width=2)
    draw.multiline_text((12, size[1] // 2 - 18), text=text, fill=(80, 80, 80), align='left')
    return image

  def get_player_image(self, player):
    image_path = os.path.join(self.image_folder, player.photo_path)
    if os.path.exists(image_path):
      return Image.open(image_path).resize((150,250))
    return self.get_placeholder_image(f"Missing image:\n{player.photo_path}", size=(150, 250))
  
  def createLoadPreAuctionButton(self):
    textfont =('calibri', 13, 'bold')
    button_foregroundColor = "green"
    button_height = 1
    button_width = 18
    self.load_pre_auction_buttion = Button(self.root, text = 'Load Pre Auction' , font = textfont,
                       fg = button_foregroundColor, command=self.load_Pre_Auction,
                       height=button_height, width=button_width, borderwidth=2)
    self.load_pre_auction_buttion.grid(column=6, row=4)
  

  def createLoadAuctionButton(self):
    textfont =('calibri', 13, 'bold')
    button_foregroundColor = "green"
    button_height = 1
    button_width = 18
    self.load_auction_button = Button(self.root, text = 'Load Auction' , font = textfont,
                       fg = button_foregroundColor, command=self.load_Auction,
                       height=button_height, width=button_width, borderwidth=2)
    self.load_auction_button.grid(column=7, row=4)
  
  def createDirectionButtons(self):
    textfont =('calibri', 15, 'bold')
    button_foregroundColor = "green"
    button_height = 1
    button_width = 10
    left_button = Button(self.root, text = '<' , font = textfont,
                       fg = button_foregroundColor, command=self.previous_player,
                       height=button_height, width=button_width, borderwidth=2)
    left_button.grid(column=6, row=5)

    right_button = Button(self.root, text = '>' , font = textfont,
                       fg = button_foregroundColor, command=self.next_player,
                       height=button_height, width=button_width, borderwidth=2)
    right_button.grid(column=7, row=5)
  
  def AddAuctionDetails(self):
    textfont =('calibri', 20, 'bold')
    auction = Label(self.root, borderwidth=5, relief= 'ridge', text='Current BID', font=textfont, justify="center",
                           anchor="n", width=25, background='silver')
    auction.grid(column=6, row=7, columnspan=2, sticky = N)

    self.current_auction_Cap = Label(self.root, borderwidth=2, relief= 'ridge', text='NA', font=textfont,
                                     anchor="n", width=13, background='silver')
    self.current_auction_Cap.grid(column=6, row=8, sticky = N)

    self.current_bid = Label(self.root, borderwidth=2, relief= 'ridge', text='NA', font=textfont,
                             anchor="n", width=13, background='silver')
    self.current_bid.grid(column=7, row=8, sticky = N)
  
  def AddSoldButton(self):
    textfont =('calibri', 15, 'bold')
    button_foregroundColor = "green"
    button_height = 1
    button_width = 10
    self.sold_button = Button(self.root, text = 'SOLD' , font = textfont,
                       fg = button_foregroundColor, command=self.on_sold,
                       height=button_height, width=button_width, borderwidth=2)
    self.sold_button.grid(column=7, row=10)
    self.sold_button.config(state="disabled")
  
  def AddUndoButton(self):
    textfont =('calibri', 15, 'bold')
    button_foregroundColor = "green"
    button_height = 1
    button_width = 10
    self.undo_button = Button(self.root, text = 'UNDO' , font = textfont,
                       fg = button_foregroundColor, command=self.on_undo,
                       height=button_height, width=button_width, borderwidth=2)
    self.undo_button.grid(column=6, row=10)

  def load_Auction(self):
    self.is_load_acution = True
    player = self.AuctionMgr.load_player()
    if player:
      self.update_display(player)
  
  def load_Pre_Auction(self):
    self.AuctionMgr.load_pre_auction_data()
    self.load_Auction()
  
  def next_player(self):
    if self.is_load_acution:
      self.update_default_Auction()
      player = self.AuctionMgr.get_next_player()
      if player:
        self.update_display(player)
  
  def previous_player(self):
    if self.is_load_acution:
      self.update_default_Auction()
      player = self.AuctionMgr.get_prev_player()
      if player:
        self.update_display(player)
  
  def update_display(self, player):
    self.Name.config(text=player.name)
    self.Batting_Rating.set_active_stars(player.batting_rating)
    self.Bowling_Rating.set_active_stars(player.bowling_rating)
    self.BasePrice.config(text=str(player.base_price))

    if player.is_player_sold():
      sold_price = str(player.sold_for)
      cap_name = player.team_name
    else:
      sold_price = 'NA'
      cap_name = 'NA'

    self.SoldForPrice.config(text=sold_price)
    self.SelectedCaptain.config(text=cap_name)
    self.update_auction_details()

    # Load player image with fallback so missing files do not crash the UI.
    image = self.get_player_image(player)

    if player.is_sold:
      try:
        font = ImageFont.truetype("BERNHC.TTF", 72)
      except OSError:
        font = ImageFont.load_default()
      draw2 = ImageDraw.Draw(image)
      draw2.text((8, 150), text="SOLD", fill=(255, 0, 0), font=font)
    
 

    self.CreateImageLabel(image)
    self.PlayerTable.updateTree()
    for cap in self.RemainingCapLabel:
      captain = self.AuctionMgr.captains_dict[cap]
      self.RemainingCapLabel[cap].update_remaining_budget(str(captain.remaining_cap))
    
    for cap in self.captains_buttons:
      if player.is_player_sold():
        self.captains_buttons[cap].disbale_button()
      else:
        self.captains_buttons[cap].enable_button()
    
  def on_sold(self):
    player = self.AuctionMgr.get_curr_player()
    sold_for_amt = self.current_bid.cget('text')
    sold_for_cap = self.current_auction_Cap.cget('text')
    player.set_sold_for(sold_for_amt)
    player.set_team_name(sold_for_cap)
    self.AuctionMgr.add_player(player, sold_for_cap)
    self.update_default_Auction()
    self.update_display(player)
    self.AuctionMgr.save()
  
  def auctioned_captain(self, new_cap_name):
    current_bid = self.current_bid.cget('text')

    if current_bid == 'NA':
      current_bid = 0
    else:
      current_bid = int(current_bid)
    
    is_updated = self.AuctionMgr.auctioned_captain(current_bid, new_cap_name)

    if is_updated:
      self.update_auction_details()
    else:
      # to raise a pop up, tbd
      pass
    self.check_and_activate_sold_button()

  def update_auction_details(self):
    last_bid_details = self.AuctionMgr.get_last_bid_details()
    if last_bid_details is None:
      self.update_default_Auction()
    else:
      self.current_auction_Cap.config(text= last_bid_details[0])
      self.current_bid.config(text=str(last_bid_details[1]))
  
  def check_and_activate_sold_button(self):
    if self.current_bid.cget('text') != "NA":
      self.sold_button.config(state='normal')
    
  def update_default_Auction(self):
    self.current_bid.config(text='NA')
    self.current_auction_Cap.config(text='NA')
    self.sold_button.config(state="disabled")
    self.AuctionMgr.clear_auction_list()
  
  def on_undo(self):
    self.AuctionMgr.undo_previous_auction_data()
    player = self.AuctionMgr.get_curr_player()
    self.update_display(player)

  def run(self):
    # all widgets will be here
    # Execute Tkinter
    self.root.mainloop()

class AuctionManager:
  def __init__(self) -> None:
    self.config = None
    self.readCaptains()
    self.playerManager = PlayerManager(self.config)
    self.captains = None
    self.captains_dict = dict()
    self.create_captains_dict()

    self.current_auction_list = list()

    self.dispWin = DisplayWindow(self)
    self.pre_auctioned_file_name = self.config.get('auctioned_players_file', 'AuctionedPlayers.xlsx')
  
  def readCaptains(self):
    config_path = Path(CONFIG_FILE_NAME)
    if not config_path.exists():
      raise FileNotFoundError(f"Missing configuration file: {CONFIG_FILE_NAME}")

    with config_path.open() as f:
      self.config = json.load(f)

    self.validate_config()

  def validate_config(self):
    if not isinstance(self.config, dict):
      raise ValueError("Configuration must be a JSON object.")

    self.config.setdefault('player_data_file', 'PL_Safety_Box_Cricket_League.xlsx')
    self.config.setdefault('auctioned_players_file', 'AuctionedPlayers.xlsx')
    self.config.setdefault('availability_column', 'Availbale')
    self.config.setdefault('max_players_per_captain', 8)
    self.config.setdefault('initial_budget_per_captain', 150000)
    self.config.setdefault('images_folder', 'images')

    captains = self.config.get('captains')
    if not isinstance(captains, list) or len(captains) == 0:
      raise ValueError("Configuration must include a non-empty 'captains' list.")

    for cap in captains:
      if isinstance(cap, dict) and not cap.get('name'):
        raise ValueError("Each captain object must include a non-empty 'name'.")

    player_data_file = self.config.get('player_data_file')
    if not os.path.exists(player_data_file):
      raise FileNotFoundError(f"Configured player data file not found: {player_data_file}")
  
  def create_captains_dict(self):
    default_max_players = int(self.config.get('max_players_per_captain', 8))
    default_initial_budget = int(self.config.get('initial_budget_per_captain', 150000))
    for cap in self.config['captains']:
      if isinstance(cap, dict):
        cap_name = cap['name']
        max_players = int(cap.get('max_players', default_max_players))
        initial_budget = int(cap.get('initial_budget', default_initial_budget))
      else:
        cap_name = cap
        max_players = default_max_players
        initial_budget = default_initial_budget
      self.captains_dict[cap_name] = CaptainClass(
        name=cap_name,
        max_num_of_players=max_players,
        initial_budget=initial_budget,
      )
  
  def add_player(self, player, cap_name):
    self.captains_dict[cap_name].add_player(player)
  
  def load_player(self):
    return self.playerManager.get_curr_player()
  
  def get_next_player(self):
    return self.playerManager.get_next_player()
  
  def get_prev_player(self):
    return self.playerManager.get_previous_player()
  
  def get_curr_player(self):
    return self.playerManager.get_curr_player()
  
  def check_if_previous_cap_is_same(self, cap_name):
    is_same = False
    if len(self.current_auction_list) > 0:
      is_same = self.current_auction_list[-1][0] == cap_name
    return is_same
    
  def auctioned_captain(self, current_bid, new_cap_name):
    value_updated = False

    if self.check_if_previous_cap_is_same(cap_name=new_cap_name):
      value_updated = False
    else:
      if current_bid == 0:
        new_bid_value = self.playerManager.get_curr_player().base_price
      else:
        if current_bid < 10000:
          increment_val = 500
        elif current_bid < 25000:
          increment_val = 1000
        else:
          increment_val = 2500

        new_bid_value = current_bid + increment_val
      # check if new_bid can be accomodated to captain
      if self.captains_dict[new_cap_name].is_cap_remaining(new_bid_value):
        self.current_auction_list.append((new_cap_name, new_bid_value))
        value_updated = True
    return value_updated
  
  def get_last_bid_details(self):
    if len(self.current_auction_list) > 0:
      return self.current_auction_list[-1]
    else:
      return None
  
  def clear_auction_list(self):
    self.current_auction_list.clear() 
  
  def undo_previous_auction_data(self):
    if len(self.current_auction_list) > 0:
      self.current_auction_list.pop()
  
  def load_pre_auction_data(self):
    if os.path.exists(self.pre_auctioned_file_name):
      df = pd.read_excel(self.pre_auctioned_file_name)
      for index,row in df.iterrows():
        if self.playerManager.check_if_player_exist(row['UID']):
          player = self.playerManager.players[row['UID']]
          player.team_name = row['cap_name']
          player.name = row['player_name']
          player.gender = row['gender']
          player.bowling_rating = row['bowl_rat']
          player.batting_rating = row['bat_rat']
          player.photo_path = row['photo_path']
          player.base_price = row['base_price']
          player.sold_for = row['sold_for']
          player.uid = row['UID']
          player.is_sold = True
          self.captains_dict[player.team_name].add_player(player)
  
  def save(self):
    data = list()
    for cap in self.captains_dict:
      for player in self.captains_dict[cap].playersList:
        if player:
          data_dict = dict()
          data_dict['cap_name'] = player.team_name
          data_dict['player_name'] = player.name
          data_dict['gender'] = player.gender
          data_dict['bowl_rat'] = player.bowling_rating
          data_dict['bat_rat'] = player.batting_rating
          data_dict['photo_path'] = player.photo_path
          data_dict['base_price'] = player.base_price
          data_dict['sold_for'] = player.sold_for
          data_dict['UID'] = player.uid

          data.append(data_dict)
    df = pd.DataFrame(data)
    
    if os.path.exists(self.pre_auctioned_file_name):
      os.remove(self.pre_auctioned_file_name)
    df.to_excel(self.pre_auctioned_file_name)
  
  def run(self):
    self.dispWin.run()


if __name__ == "__main__":
  inst = AuctionManager()
  inst.run()
  inst.save()