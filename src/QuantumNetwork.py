from tkinter import *
from operator import add
import numpy as np
import time
from src.Utils import start, setGlobalValues, periodic_update

from Quantum_Node import Node
from Quantum_Edge import Edge
from global_variables import *


class Quantum_Network():
    def __init__(self):
        self.window = Tk()
        self.window.title('Quantum Key Distribution Network')
        self.canvas_size = size_of_board
        # Create left and right frames
        self.left_frame = Frame(self.window, width= self.canvas_size+20, height=self.canvas_size+20)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)
        self.right_frame = Frame(self.window, width=200, height=400)
        self.right_frame.grid(row=0, column=1, padx=10, pady=5)

        self.canvas = Canvas(self.left_frame, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.click)
        self.canvas.bind('<Double-Button-1>', self.doubleclick)

        self.name_var=IntVar()
        self.name_var.set(5)
        self.setup_board()

        name_label = Label(self.right_frame, text = 'Number of Dots')
        name_entry = Entry(self.right_frame,textvariable = self.name_var)
        sub_btn=Button(self.right_frame,text = 'Submit', command = self.submit)
        start_transition_btn = Button(self.right_frame,text = 'Start transition', command = self.transition)
        reset_btn = Button(self.right_frame,text = 'Reset', command = self.reset)
        name_label.grid(row=0,column=0)
        name_entry.grid(row=1,column=0)
        sub_btn.grid(row=1,column=1, padx= 5)
        start_transition_btn.grid(row=2, column=0, pady=10)
        reset_btn.grid(row=2, column=1)
        self.resetting_board()

    def submit(self):
        global number_of_dots
        number_of_dots=self.name_var.get()
        global size_of_board
        size_of_board =number_of_dots * 100
        self.canvas_size = number_of_dots * 100
        self.canvas.delete('all')
        self.canvas.config(width=self.canvas_size, height=self.canvas_size)
        self.setup_board()
        self.resetting_board()

    def reset(self):
        self.canvas.delete('all')
        self.setup_board()
        self.resetting_board()
    
    def end_selection(self):
        end_node = [ i *distance_between_dots + distance_between_dots/2 for i in self.edge_list[-1].nodes[1]]
        node = next(x for x in self.node_list if x.position == end_node)
        print(node)
        self.update_node_color(node, dot_selected_color)
        [x.color != dot_selected_color and self.update_node_color(x, dot_disable_color) for x in self.node_list]

    def transition(self):
        global gate_count, gate_order, channel_order, channel_count
        self.end_selection()
        for i in range(len(self.edge_list)):
            channel_count = 0
            setGlobalValues(channel_order, channel_count, self.window)
            edge_coords = self.canvas.coords(self.edge_list[i].line_id)
            ball_coords = [edge_coords[0], edge_coords[1]]
            end_ball_coords = [edge_coords[2], edge_coords[3]]
            start_node = [ i *distance_between_dots + distance_between_dots/2 for i in self.edge_list[i].nodes[0]]
            if start_node != ball_coords:
                end_ball_coords = ball_coords
                ball_coords = [edge_coords[2],edge_coords[3]]
            ball = self.canvas.create_oval(ball_coords[0],ball_coords[1],ball_coords[0],ball_coords[1], fill="Red", outline="Red", width=10)
            while ball_coords != end_ball_coords :
                if(channel_count == 0):
                    channel_count = periodic_update()
                time.sleep(0.3)
                xinc = 0
                yinc = 0
                if ball_coords[0] < end_ball_coords[0]:
                    ball_coords[0] += 10
                    xinc = 10
                elif ball_coords[0] > end_ball_coords[0]:
                    ball_coords[0] -= 10
                    xinc = -10
                if ball_coords[1] < end_ball_coords[1]:
                    ball_coords[1] += 10
                    yinc = 10
                elif ball_coords[1] > end_ball_coords[1]:
                    ball_coords[1] -= 10
                    yinc = -10
                self.canvas.move(ball, xinc, yinc)
                self.canvas.update()

    def setup_board(self):
        self.edge_list =[]
        self.node_list =[]
        self.dot_colors = np.full((number_of_dots, number_of_dots), dot_color)
        for i in range(number_of_dots):
            x = i*distance_between_dots+distance_between_dots/2
            self.canvas.create_line(x, distance_between_dots/2, x, size_of_board-distance_between_dots/2, fill='gray', dash = (2, 2))
            self.canvas.create_line(distance_between_dots/2, x, size_of_board-distance_between_dots/2, x, fill='gray', dash=(2, 2))
        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i*distance_between_dots+distance_between_dots/2
                end_x = j*distance_between_dots+distance_between_dots/2
                oval_id = self.canvas.create_oval(start_x-dot_width/2, end_x-dot_width/2, start_x+dot_width/2, end_x+dot_width/2, fill=dot_color, outline=dot_color)
                node = Node(str(i)+str(j), oval_id, [start_x, end_x], -1, 0)
                self.node_list.append(node)

    def resetting_board(self):
        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        self.dot_colors = np.full((number_of_dots, number_of_dots), dot_color)
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))
        self.dot_selection_status = np.zeros(shape=(number_of_dots, number_of_dots))-1
        self.reset_board = False

    def mainloop(self):
        self.window.mainloop()

    def is_grid_occupied(self, logical_position, type):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True
        if type == 'node':
            occupied = False
        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False
        return occupied
    
    def round_off_to_nearest_node(self, position):
        return (distance_between_dots) * np.round(position / distance_between_dots)+0

    def convert_grid_to_logical_position(self, grid_position): 
        grid_position = np.array(grid_position)
        position = (grid_position-distance_between_dots/5)//(distance_between_dots/2)
        type = False
        logical_position = []
        if all(abs(grid_position - (self.round_off_to_nearest_node(grid_position - distance_between_dots/2)+ distance_between_dots/2))< dot_width//2):
            r = int((position[0])//2)
            c = int(position[1]//2)  
            type = node
        elif position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0]-1)//2)
            c = int(position[1]//2)
            type = row
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            type = col
        logical_position = [r, c]
        return [logical_position, type]
    
    def update_node_color(self, node, dot_color):
        self.canvas.itemconfig(node.oval_id, fill= dot_color, outline= dot_color )
        node.color = dot_color
        self.canvas.tag_raise(node.oval_id)

    def include_edge_error(self, edge):
        if edge.id == 2:
            self.canvas.after(3000, self.canvas.delete, edge.line_id)
            self.canvas.after(6000, lambda :self.delete_edge(edge))
            self.row_status[edge.position[1]][edge.position[0]] = 0
        
    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        if c <= (number_of_dots-1) and r <= (number_of_dots-1):
            if type == 'node':
                [x.color != dot_selected_color and self.update_node_color(x, dot_disable_color) for x in self.node_list]
                self.dot_selection_status[c][r] = 1
                oval = next(x for x in self.node_list if x.id == str(r)+str(c))
                if oval.color != dot_selected_color:
                    self.update_node_color(oval, dot_selection_color)
                [x.id in [str(r)+str(c-1), str(r)+str(c+1), str(r-1)+str(c), str(r+1)+str(c)] and x.color != dot_selected_color and self.update_node_color(x, dot_color)
                  for x in self.node_list]
            if c > 0:
                self.dot_selection_status[c-1][r] = 0
            if c < number_of_dots-1:    
                self.dot_selection_status[c+1][r] = 0
            if r > 0:
                self.dot_selection_status[c][r-1] = 0
            if r < number_of_dots-1:
                self.dot_selection_status[c][r+1] = 0

    def delete_edge(self,edge):
        self.canvas.delete(edge.line_id2)
        node2 = str(int(edge.position[0])+1)+str(edge.position[1]) if edge.type == row else str(edge.position[0])+str(int(edge.position[1])+1)
        node_id = [str(edge.position[0])+str(edge.position[1]), node2]
        for node in self.node_list:
            if node.id in node_id:
               node.edges-=1
               if node.edges < 1 and node.color != dot_selection_color:
                   self.update_node_color(node, dot_disable_color)

    def make_edge(self, type, logical_position, nodes):
        r = logical_position[0]
        c = logical_position[1]
        if type == row:
            start_x = distance_between_dots / 2 + r*distance_between_dots
            end_x = start_x+distance_between_dots
            start_y = distance_between_dots / 2 + c*distance_between_dots
            end_y = start_y
            if self.row_status[c][r] == 0:
                row_id = c * (number_of_dots-1) + r
                line_id = self.canvas.create_line(start_x, start_y, end_x, end_y, fill=edge_color, width=edge_width)
                line_id2 = self.canvas.create_line(start_x, start_y, end_x, end_y, fill=edge_color, width=edge_width, dash=(2,2))
                edge = Edge(row_id, line_id, line_id2, row, logical_position, 0, nodes )
                self.edge_list.append(edge)
                self.row_status[c][r] = 1
                self.include_edge_error(edge)
            else:
                row_id = c * (number_of_dots-1) + r
                line = next(x for x in self.edge_list if x.id == row_id).line_id
                line2 = next(x for x in self.edge_list if x.id == row_id).line_id2
                self.canvas.delete(line)
                self.canvas.delete(line2)
                [x.color != dot_selected_color and self.update_node_color(x,dot_color)
                  for x in self.node_list]
                self.row_status[c][r] = 0    
        elif type == col:
            start_y = distance_between_dots / 2 + c* distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + r * distance_between_dots
            end_x = start_x
            if self.col_status[c][r] == 0:
                col_id =( c * (number_of_dots-1) + r) *2
                line_id = self.canvas.create_line(start_x, start_y, end_x, end_y, fill=edge_color, width=edge_width)
                line_id2 = self.canvas.create_line(start_x, start_y, end_x, end_y, fill=edge_color, width=edge_width, dash=(2,2))
                edge = Edge(col_id, line_id, line_id2, col, logical_position, 0, nodes )
                self.edge_list.append(edge)
                self.col_status[c][r] = 1
            else:
                col_id = ( c * (number_of_dots-1) + r) *2
                line = next(x for x in self.edge_list if x.id == col_id).line_id
                line2 = next(x for x in self.edge_list if x.id == col_id).line_id2
                self.canvas.delete(line)
                self.canvas.delete(line2)
                [x.color != dot_selected_color and self.update_node_color(x, dot_color)
                  for x in self.node_list]
                self.col_status[c][r] = 0 
        ''' this is needed for edge deletion need to check later        
        oval = next(x for x in self.node_list if x.id == str(r)+str(c))
        self.update_node_color(oval, dot_selected_color)
        oval.edges += 1
        ovalSelecter = str(r+1)+str(c) if type == row else str(r)+str(c+1)
        oval1 = next(x for x in self.node_list if x.id == ovalSelecter)
        oval1.edges += 1'''

    def find_selected_node(self, logical_position):
        adjacent_nodes=[[-1,0], [1,0], [0,-1], [0,1]]
        for index in adjacent_nodes:
            adjacent_index = list( map(add, logical_position, index) )
            if adjacent_index[1] <= number_of_dots-1 and adjacent_index[0] <= number_of_dots-1 and self.dot_selection_status[adjacent_index[1]][adjacent_index[0]] > 0:
                return adjacent_index

    def minimum(self, a, b):
        if a <= b:
            return a
        else:
            return b
    
    def update_nodes(self, valid_input, logical_position):
        global parent_node
        if self.dot_selection_status[logical_position[1]][logical_position[0]] == 0:
            [r,c] = self.find_selected_node(logical_position)
            nodes = [[r,c],logical_position]
            if r == logical_position[0]:
                self.make_edge('col', [r,self.minimum(c,logical_position[1])], nodes)
            else:
                self.make_edge('row', [self.minimum(r,logical_position[0]),c], nodes)
            oval = next(x for x in self.node_list if x.id == str(r)+str(c))
            self.update_node_color(oval, dot_selected_color)
        self.update_board(valid_input, logical_position)
        if (len(self.edge_list)) == 0:
            start(self.window)

    def click(self, event):
        if not self.reset_board:
            grid_position = [event.x, event.y]
            [logical_positon, valid_input] = self.convert_grid_to_logical_position(grid_position)
            if valid_input == node:
                self.update_nodes(valid_input, logical_positon)
            else:
                self.make_edge(valid_input, logical_positon, [])
        else:
            self.canvas.delete("all")
            self.resetting_board()
            self.reset_board = False


    def doubleclick(self, event):
        myLabel = Label(self.window, text = 'Hello world')
        myLabel.pack()
        if not self.reset_board:
            grid_position = [event.x, event.y]
            [logical_positon, valid_input] = self.convert_grid_to_logical_position(grid_position)
            if valid_input == row and not self.is_grid_occupied(logical_positon, valid_input):
                self.update_nodes(valid_input, logical_positon)
        else:
            self.canvas.delete("all")
            self.resetting_board()
            self.reset_board = False

game_instance = Quantum_Network()
game_instance.mainloop()
