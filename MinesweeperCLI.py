import random
import pandas as pd

class Board:
    def __init__(self, row_count, col_count, mine_count):
        self.row_count = row_count
        self.col_count = col_count
        self.mine_count = mine_count
        self.dataBoard = []
        self.displayBoard = [["?"] * self.col_count for i in range(self.row_count)]
        self.mineRevealed = False

    def getData(self, row, col): #Getter from self.dataBoard for given row and col
        return self.dataBoard[row][col]

    def setup(self): 
        #Generate Board
        self.dataBoard = self.dataBoard = [[0] * self.col_count for i in range(self.row_count)]
        #Fill Board
        ##Generate and plant mines
        self.minesloc = []
        for i in range(self.mine_count):
            tempRow = random.randrange(self.row_count)
            tempCol = random.randrange (self.col_count)
            while [tempRow, tempCol] in self.minesloc:
                tempRow = random.randrange(self.row_count)
                tempCol = random.randrange (self.col_count)
            self.minesloc.append([tempRow, tempCol])
            self.dataBoard[tempRow][tempCol] = 'X'
        ##Generate and plant indicators
            for x in range(-1, 2):
                for y in range(-1, 2):
                    tempIndRow = tempRow + x
                    tempIndCol = tempCol + y
                    if x == 0 and y ==0:
                        continue
                    elif (tempIndRow < 0 or tempIndRow >=self.row_count):
                        continue
                    elif (tempIndCol < 0 or tempIndCol >=self.col_count):
                        continue
                    elif self.dataBoard[tempIndRow][tempIndCol] == 'X':
                        continue
                    elif self.getData(tempIndRow, tempIndCol) == 0:
                        self.dataBoard[tempIndRow][tempIndCol] = 1
                    elif self.getData(tempIndRow, tempIndCol) == 1:
                        self.dataBoard[tempIndRow][tempIndCol] += 1
                        
    def play(self):
        def reveal(row, col): #For revealing display board based on row and col of self.dataBoard
            self.displayBoard[row][col] = self.getData(row, col)
            displayed.append([row, col])

        def cascade(row, col): #For auto-revealing when user reveal a 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    tempRow = row + x
                    tempCol = col + y
                    #use cases if out of index
                    if x == 0 and y == 0:
                        continue
                    elif tempRow < 0 or tempRow > 9:
                        continue
                    elif tempCol < 0 or tempCol > 9:
                        continue
                    elif self.getData(tempRow, tempCol) == 'X':
                        continue
                    elif [self.getData(tempRow, tempCol)] in displayed:
                        continue
                    elif self.getData(tempRow, tempCol) in range(1, 9) and [tempRow, tempCol] not in displayed:
                        reveal(tempRow, tempCol)
                    elif self.getData(tempRow, tempCol) == 0 and [tempRow, tempCol] not in displayed:
                        reveal(tempRow, tempCol)
                        cascade(tempRow, tempCol)

        def printDisplay(): #Convert regular python lists into more presentable formmat (Pandas DataFrame)
            print(pd.DataFrame(self.displayBoard))

        def catchAndProcess(): #For catching user input, and determining if game is still legitimate for running
            inputRowCol = ((input("Reveal (row, col) = ")).replace(" ", "")).split(",")
            #Purpose : Ask input, delete blankspace inside input, convert input into list
            #Necessary because this will enable you to still do valid input even with space/blankspace in between.
            while len(inputRowCol) != 2:
                print("Invalid Input, Try again")
                inputRowCol = ((input("Reveal (row, col) = ")).replace(" ", "")).split(",")
            row = int(inputRowCol[0])
            col = int(inputRowCol[1])
            if self.getData(row, col) != 0 and [row, col] not in displayed:
                if self.getData(row, col) == 'X':
                    print("YOU'VE REVEALED A MINE, YOU LOSE!!!!")
                    self.displayBoard = self.dataBoard
                    self.mineRevealed = True
                    printDisplay()
                elif self.getData(row, col) in range(1, 9):
                    reveal(row, col)
                    printDisplay()
            elif self.getData(row, col) == 0 and [row, col] not in displayed:
                cascade(row, col)
                printDisplay()
            elif [row, col] in displayed:
                print("This cell has been revealed before")
                printDisplay()

        def resetState(): #for resetting board property and the game overall
            self.dataBoard = []
            self.displayBoard = [["?"] * self.col_count for i in range(self.row_count)]
            self.mineRevealed = False
            displayed = []
            remainingCell = self.row_count * self.col_count - self.mine_count - len(displayed)
            return remainingCell

        #Required varibles
        displayed = []
        remainingCell = self.row_count * self.col_count - self.mine_count - len(displayed)

        printDisplay()
        while remainingCell != 0 and self.mineRevealed is False: #To keep the game-flow running
            catchAndProcess()
            remainingCell = self.row_count * self.col_count - self.mine_count - len(displayed)
            print(remainingCell)
        if remainingCell == 0 and self.mineRevealed is False: #Winninng Conditions
            print("CONGRATULATIONS! YOU WIN!!!")
        elif self.mineRevealed: #Retry option
            choice = input("Try Again? (y/n) ")
            if choice.lower() == "y":
                self.resetState()
                self.play()
            elif choice.lower() == "n":
                exit()

if __name__ == '__main__':
    board = Board(10, 10, 10)
    board.setup()
    board.play()