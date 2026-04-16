from tkinter import *

class StarCanvasClass:
  def __init__(self, root, grid_row, grid_col, num_of_stars=5) -> None:
    self.root = root
    self.grid_row = grid_row
    self.grid_col = grid_col
    self.fill_color_nonActive = "black"
    self.fill_color_active = "gold"
    self.num_of_stars = num_of_stars
    # star points
    self.points = list()
    self.create_star_points()
    self.canvas = None
    self.create_canvas()
  
  def create_star_points(self):
    points = [100,10,40,198,190,78,10,78,160,198]
    points = [point/8 for point in points]

    for j in range(self.num_of_stars):
      self.points.append([points[i]+ j*75 + 10 if i % 2 == 0 else points[i] + 10 for i in range(0, len(points))])


  def create_canvas(self):
    self.canvas = Canvas(width=365, height=35, borderwidth=5, relief= 'ridge')
    for points in self.points:
      self.canvas.create_polygon(points, fill=self.fill_color_nonActive, width=1)
    self.canvas.grid(column=self.grid_col, row=self.grid_row, columnspan=2)
  
  def set_active_stars(self, active_stars):
    for i in range(self.num_of_stars):
      if i < active_stars:
        fill_color=self.fill_color_active
      else:
        fill_color=self.fill_color_nonActive
      self.canvas.create_polygon(self.points[i], fill=fill_color, width=1)