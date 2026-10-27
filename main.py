import os
#Input Verification Function
def verifyInput(typeWanted, message, valid):
  answer = input(message)
  try:
    answer = typeWanted(answer)
    if type(answer) == typeWanted and answer in valid:
      return answer
    else:
      #Recursively enter the verifyType until the correct input is entered.
      return (verifyInput(typeWanted, message, valid))
  except:
    return (verifyInput(typeWanted, message, valid))

#Game Board
class game():
    def __init__(self): #Col 0   1   2    3    4    5
        self.currBoard = [["+", "+", "+", "+", "+", "+", "+", "+"], #Row 0
                          ["+", "+", "+", "+", "+", "+", "+", "+"], #Row 1
                          ["+", "+", "+", "+", "+", "+", "+", "+"],
                          ["+", "+", "+", "+", "+", "+", "+", "+"],
                          ["+", "+", "+", "+", "+", "+", "+", "+"],
                          ["+", "+", "+", "+", "+", "+", "+", "+"],
                          ["+", "+", "+", "+", "+", "+", "+", "+"],
                          ["+", "+", "+", "+", "+", "+", "+", "+"]]
        self.movesMade = 0
        self.movesSkipped = 0
        self.blackCaptured = 0 #Black pieces which white has captured. This adds to white's score at the end.
        self.whiteCaptured = 0 #White pieces which black has captured. This adds to black's score at the end.
        self.validWSkip = [0, 1, 2, 3, 4, 5, 6, 7, -1]
        self.valid = [0, 1, 2, 3, 4, 5, 6, 7]

    def printBoard(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("----New Board----")
        count = 0
        for row in self.currBoard:
            for col in range(len(row)):
                if col == len(row)-1:
                    print (f"{row[col]} {count}")
                else:
                    print(row[col], end=" ")
            count += 1
        print("0 1 2 3 4 5 6 7")
        print("----End Board----")

    def setTile(self, col, row, value):
        self.currBoard[row][col] = value

    def getTile(self, col, row):
        return self.currBoard[row][col]

    def makeMove(self):
        selected = ""
        suicide = False
        captureOther = False
        while selected != "+" or (suicide and not captureOther):
            suicide = False
            captureOther = False
            desireCol = verifyInput(int, "Please enter the desired column (-1 to skip turn): ", self.validWSkip)
            if desireCol == -1:
                self.movesSkipped += 1
                self.movesMade += 1
                return
            desireRow = verifyInput(int, "Please enter the desired row: ", self.valid)
            selected = self.getTile(desireCol, desireRow)
            if selected != "+":
                continue
            toCheck = [[-1, 0], [1, 0], [0, -1], [0, 1]]
            self.setTile(desireCol, desireRow, "B") if self.movesMade % 2 == 0 else self.setTile(desireCol, desireRow, "W")
            for moveRow, moveCol in toCheck:
                newRow, newCol = desireRow + moveRow, desireCol + moveCol
                if (0 <= newRow < 8) and (0 <= newCol < 8):
                    if self.movesMade % 2 == 0:
                        newTile = self.getTile(newCol, newRow)
                        if newTile == "W":
                            captureOther = self.captured(newRow, newCol) if not captureOther else captureOther
                    else:
                        newTile = self.getTile(newCol, newRow)
                        if newTile == "B":
                            captureOther = self.captured(newRow, newCol) if not captureOther else captureOther
            suicide = self.captured(desireRow, desireCol)
            self.setTile(desireCol, desireRow, "+")
            if suicide and not captureOther:
                selected = ""
        if self.movesMade % 2 == 0:
            self.setTile(desireCol, desireRow, "B")
        else:
            self.setTile(desireCol, desireRow, "W")
        self.movesMade += 1
        self.movesSkipped = 0
        self.performExactCaptures(desireRow, desireCol)

    def findLiberties(self, row, col, colour, visited=None):
        if visited is None:
            visited = []

        if not (0 <= row < 8 and 0 <= col < 8) or [row, col] in visited:
            return [] #Return an empty list if we are out of bounds or have already checked
        visited.append([row, col])
        liberties = []
        toCheck = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for moveRow, moveCol in toCheck:
            newRow, newCol = row + moveRow, col + moveCol
            if (0 <= newRow < 8) and (0 <= newCol < 8):
                newTile = self.getTile(newCol, newRow)
                if newTile == "+" and [newRow, newCol] not in liberties:
                    liberties.append([newRow, newCol])
                elif newTile == colour:
                    liberties.extend(self.findLiberties(newRow, newCol, colour, visited))
        return liberties

    def captured(self, row, col):
        lookItem = self.getTile(col, row)
        if lookItem == "+":
            return False
        liberties = self.findLiberties(row, col, lookItem)
        if len(liberties) == 0:
            return True
        else:
            return False

    def findChain(self, row, col, visited=None):
        if visited is None:
            visited = []
        lookItem = self.getTile(col, row)
        if lookItem == "+" or not (0 <= row < 8 and 0 <= col < 8) or [row, col] in visited: #if out of bounds or item is a plus then return an empty list.
            return []
        chain = []
        if [row, col] not in visited:
            chain.append([row, col])
        visited.append([row, col])
        toCheck = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for moveRow, moveCol in toCheck:
            newRow, newCol = row + moveRow, col + moveCol
            if (0 <= newRow < 8) and (0 <= newCol < 8):
                newTile = self.getTile(newCol, newRow)
                if newTile == lookItem and [newRow, newCol] not in chain:
                    chain.extend(self.findChain(newRow, newCol, visited))
        return chain

    def performExactCaptures(self, rowIn, colIn):
        tempBoard = [row[:] for row in self.currBoard]
        toCheck = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        considered = []
        myColour = self.getTile(colIn, rowIn)
        enemyColour = "W" if myColour == "B" else "B"
        for moveRow, moveCol in toCheck:
            newRow, newCol = rowIn + moveRow, colIn + moveCol
            if (0 <= newRow < 8) and (0 <= newCol < 8):
                colour = self.getTile(newCol, newRow)
                if colour == enemyColour:
                    if self.captured(newRow, newCol):
                        chainPos = self.findChain(newRow, newCol)
                        if all(chainPos[0] not in i for i in considered):
                            considered.append(chainPos)
                            if colour == "B":
                                self.blackCaptured += len(chainPos)
                            elif colour == "W":
                                self.whiteCaptured += len(chainPos)
                            for cRow, cCol in chainPos:
                                tempBoard[cRow][cCol] = "+"
        self.currBoard = tempBoard

    def end(self):
        if self.movesSkipped == 2:
            return True
        else:
            return False
'''
*********************
      Main Code
*********************
'''
def main():
    end = False
    gameTest = game()
    gameTest.printBoard()
    while not end:
        gameTest.makeMove()
        gameTest.printBoard()
        end = gameTest.end()

    print("Game Over, the board state is: ")
    gameTest.printBoard()

    input("Press enter to close the game.")

if __name__ == "__main__":
    main()