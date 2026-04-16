from tkinter import *
from  tkinter import ttk
from itertools import zip_longest

class PlayerTableClass:
  def __init__(self, root, grid_row, grid_col, captainsMap:dict, columnspan=8) -> None:
    self.root = root
    self.grid_row = grid_row
    self.grid_col = grid_col
    self.captainsMap = captainsMap
    game_frame = Frame(self.root)
    game_frame.grid(column=grid_col, row=grid_row, columnspan=columnspan)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="silver",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="silver")
    style.map('Treeview', 
              background=[('selected' , 'green')])
    
    captains_list = list(captainsMap.keys())
    self.PlayerTable = ttk.Treeview(game_frame)
    self.PlayerTable['columns'] = tuple(captains_list)
    self.PlayerTable.column("#0", width=0,  stretch=NO)
    self.PlayerTable.heading("#0",text="",anchor=CENTER)


    for cap in captains_list:
      self.PlayerTable.column(cap,anchor=CENTER, width=190)
      self.PlayerTable.heading(cap,text=cap,anchor=CENTER)
    self.PlayerTable.pack()

    self.updateTree()
  
  def updateTree(self):
    for i in self.PlayerTable.get_children():
      self.PlayerTable.delete(i)

    data = [self.captainsMap[cap].get_playerList() for cap in self.captainsMap]
    data = list(map(list, zip_longest(*data, fillvalue=None)))

    for id,each_row_data in enumerate(data):
      data = [each_data.name if each_data else 'Empty Slot' for each_data in each_row_data]
      self.PlayerTable.insert(parent='',index='end',iid=id,text='', 
                              values=data)
    