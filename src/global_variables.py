from sympy import false

size_of_board = 500
number_of_dots = 5
dot_color = '#7BC043'
edge_color = '#808080'
dot_selection_color = '#ADD8E6'
dot_selected_color = '#FF0000'
dot_disable_color = '#DCDCDC'
distance_between_dots = size_of_board / number_of_dots
dot_width = 0.4*distance_between_dots
edge_width = 0.03*distance_between_dots
node = 'node'
col = 'col'
row = 'row'

# Create a canvas_widget variable to hold the FigureCanvasTkAgg instance
channel_order = ["xgate", "ugate", "igate", "hgate"]
channel_count = 0
parent_node = false