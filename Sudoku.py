__author__ = 'Karen Qian, Flint Song'
from Tkinter import *
import math
import copy

#input puzzle_size
puzzle_size = 16
length = int(math.sqrt(puzzle_size))
length_square = int(math.sqrt(length))
rows = []
sudoku = [0]*puzzle_size
solved = [0]*puzzle_size
yes = False

def create_constraint():
    constraint = dict()
    for n in range(puzzle_size):
        constraint[n] = range(1, length+1)
    print constraint
    for n in range(puzzle_size):
        if sudoku[n] is not '0':
            print "N: ", n
            constraint[n] = [0]*999
            x = n-n%int(math.pow(len(sudoku), 0.5))
            for a in range(int(math.pow(len(sudoku), 0.5))):
                if x+a in constraint and int(sudoku[n]) in constraint[x+a]:
                    constraint[x+a].remove(int(sudoku[n]))
            y = n%int(math.pow(len(sudoku), 0.5))
            for b in range(0,len(sudoku),int(math.pow(len(sudoku), 0.5))):
                if y+b in constraint and int(sudoku[n]) in constraint[y+b]:
                    constraint[y+b].remove(int(sudoku[n]))
            box_x = ((n%int(math.pow(len(sudoku), 0.5)))/int(math.pow(len(sudoku), 0.25)))*int(math.pow(len(sudoku), 0.25))
            box_y = ((n/int(math.pow(len(sudoku), 0.5)))/int(math.pow(len(sudoku), 0.25)))*int(math.pow(len(sudoku), 0.25))
            for c in range(0,int(math.pow(len(sudoku), 0.25))):
                for d in range(0,int(math.pow(len(sudoku), 0.25))):
                    if (box_y+c)*int(math.pow(len(sudoku), 0.5))+box_x+d in constraint and int(sudoku[n]) in constraint[(box_y+c)*int(math.pow(len(sudoku), 0.5))+box_x+d]:
                        constraint[(box_y+c)*int(math.pow(len(sudoku), 0.5))+box_x+d].remove(int(sudoku[n]))
    return constraint

def insert(num, pos, board, constraint):
    board[pos] = num
    constraint[pos] = [0]*999
    x = pos-pos%int(math.pow(len(board), 0.5))
    for a in range(int(math.pow(len(board), 0.5))):
        if x+a in constraint and num in constraint[x+a]:
            constraint[x+a].remove(num)
    y = pos%int(math.pow(len(board), 0.5))
    for b in range(0,len(board),int(math.pow(len(board), 0.5))):
        if y+b in constraint and num in constraint[y+b]:
            constraint[y+b].remove(num)
    box_x = ((pos%int(math.pow(len(board), 0.5)))/int(math.pow(len(board), 0.25)))*int(math.pow(len(board), 0.25))
    box_y = ((pos/int(math.pow(len(board), 0.5)))/int(math.pow(len(board), 0.25)))*int(math.pow(len(board), 0.25))
    for c in range(0,int(math.pow(len(board), 0.25))):
        for d in range(0,int(math.pow(len(board), 0.25))):
            if (box_y+c)*int(math.pow(len(board), 0.5))+box_x+d in constraint and num in constraint[(box_y+c)*int(math.pow(len(board), 0.5))+box_x+d]:
                constraint[(box_y+c)*int(math.pow(len(board), 0.5))+box_x+d].remove(num)

def solve(sudoku, constraint):
    trial = []
    boards = []
    constraints = []
    while '0' in sudoku:
        sort = sorted(constraint.items(), key=lambda x: len(x[1]))
        if len(sort[0][1]) == 999:
            print 'unsolvable board'
            sys.exit(0)
        elif len(sort[0][1]) == 1:
            insert(sort[0][1][0], sort[0][0], sudoku, constraint)
        elif len(sort[0][1]) > 1:
            boards.append(copy.deepcopy(sudoku))
            constraints.append(copy.deepcopy(constraint))
            trial.append(0)
            insert(sort[0][1][trial[-1]], sort[0][0], sudoku, constraint)
        elif len(sort[0][1]) == 0:
            if len(boards) != 0:
                sudoku = boards.pop()
            else:
                print 'unsolvable board'
                sys.exit(0)
            constraint = constraints.pop()
            sort = sorted(constraint.items(), key=lambda x: len(x[1]))
            trial[-1] += 1
            while trial[-1]+1 > len(sort[0][1]):
                sudoku = boards.pop()
                constraint = constraints.pop()
                trial.pop()
                trial[-1] += 1
                sort = sorted(constraint.items(), key=lambda x: len(x[1]))
            boards.append(copy.deepcopy(board))
            constraints.append(copy.deepcopy(constraint))
            insert(sort[0][1][trial[-1]], sort[0][0], sudoku, constraint)
    print "Board", sudoku
    return sudoku

class Grid(Frame):

    def onPlay(self):
        count = 0
        for row in rows:
            for col in row:
                if col.get() is not '0':
                    col['fg'] = "Dark Green"

    def onSolve(self):
        count = 0
        for row in rows:
            for col in row:
                sudoku[count] = col.get()
                count+=1
        count = 0
        solved = solve(sudoku, create_constraint())
        print "Sudoku", sudoku
        for row in rows:
            for col in row:
                col.delete(0, END)
                col.insert(0, solved[count])
                count+=1

    def onCheck(self):
        count = 0
        for row in rows:
            for col in row:
                sudoku[count] = col.get()
                count+=1
        solved = solve(sudoku, create_constraint())
        count = 0
        for row in rows:
            for col in row:
                if not int(col.get()) == int(solved[count]):
                    col['bg'] = "Red"
                else:
                    col['bg'] = "Green"
                count+=1

    #def onSize(self):
        #puzzle_size = int(self.size_text.get())
        #length = int(math.sqrt(float(puzzle_size)))
        #length_square = int(math.sqrt(length))
        #yes = True
        #rows = []
        #cols = []
        #Frame.destroy(self)

    def onClear(self):
        count = 0
        for row in rows:
            for col in row:
                r = int(count/length)
                c = (count%length)
                temp = length*2
                if (r%temp < length_square and c%temp < length_square) or (r%temp >= length_square and c%temp >= length_square):
                    col['bg'] = "LightCyan3"
                    col['fg'] = "Black"
                else:
                    col['bg'] = "White"
                    col['fg'] = "SteelBlue3"
                count+=1
                col.delete(0,END)
                col.insert(0, 0)


    def onQuit(self):
        sys.exit(0)

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        entryFrame = Frame(self, width=200, height=200)
        entryFrame.grid()
        for i in range(0, length):
            cols = []
            temp = length_square*2
            for j in range(0, length):
                if (i%temp < length_square and j%temp < length_square) or (i%temp >= length_square and j%temp >= length_square):
                    e = Entry(relief=RIDGE, bg="LightCyan3", width=5)
                else:
                    e = Entry(relief=RIDGE, fg = "SteelBlue3", width=5)
                e.grid(row=i, column=j+1, sticky=NSEW)
                e.insert(0, "0")
                cols.append(e)
            rows.append(cols)
        if not yes:
            #self.size_text = Entry(relief=RIDGE, bg="white", width=10)
            #self.size_text.grid(row=0, column=0)
            #sizebutton = Button(parent, text="Size?", command=self.onSize)
            #sizebutton.grid(row=1, column=0)
            generate = Button(parent, text="Play", command=self.onPlay)
            middle = int(length/2)
            generate.grid(row=middle-1, column=0)
            generate.config(width=12)
            solve = Button(parent, text="Solve for me", command=self.onSolve)
            solve.grid(row=middle, column=0)
            solve.config(width=12)
            check = Button (parent, text="Check", command=self.onCheck)
            check.grid(row=middle+1, column=0)
            check.config(width=12)
            clear = Button (parent, text="Clear", command=self.onClear)
            clear.grid(row=middle+2, column=0)
            clear.config(width=12)
            quit1 = Button(parent, text="Quit", command=self.onQuit)
            quit1.grid(row=middle+3, column=0)
            quit1.config(width=12)

if __name__ == '__main__':
    root = Tk()
    root.title('Sudoku')
    root.geometry("%dx%d%+d%+d" % ((400/9)*length, (215/9)*length, 0, 0))
    g = Grid(root)
    g.mainloop()