from tkinter import *

class AuctionButtonClass:
  def __init__(self, root, display_text, grid_row, grid_col) -> None:
    self.root =  root
    self.display_text = display_text
    self.grid_row = grid_row
    self.grid_col = grid_col
    self.textfont =('calibri', 13, 'bold')
    self.button_foregroundColor = "green"
    self.button_height = 4
    self.button_width = 20
    self.btn = None
    self.create_button()

  def create_button(self):
     self.btn = Button(self.root.root, text = self.display_text , font = self.textfont,
                       fg = self.button_foregroundColor, command=self.clicked,
                       height=self.button_height, width=self.button_width)
     self.btn.grid(column=self.grid_col, row=self.grid_row)
     self.disbale_button()
  
  def enable_button(self):
    self.btn.config(state="normal")
  
  def disbale_button(self):
    self.btn.config(state="disabled")

  def clicked(self):
    self.root.auctioned_captain(self.display_text)
