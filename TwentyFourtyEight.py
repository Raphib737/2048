__author__ = 'Raphael Baysa'
import numpy as np
from numpy import random

'''
    A class to store a 2048 game object.
'''

class P2048(object):

    #region Constructor
    def __init__(self):
        '''
        Each game object has two members. An array of tiles, and an array named
        freeTiles that will be dynamically used to store freeTiles
        :return: Instantiates class
        '''
        self.tiles = np.array([[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]
                               ])
        self.freeTiles = []
        self.tilesBackup = []
        self.largest = 0
    #endregion

    # region Game functions
    def startGame(self):
        '''
        Starts the game by clearing the board, and then generating two
        new tiles.
        Prints game after
        HOWEVER TODO:
        make it run the game or something instead of just printing
        right now it is printing just for testing purposes.
        '''
        self.clearBoard()
        self.generateTile()
        self.generateTile()
        self.printGame()
        print("The moves are 1)Right, 2)Left, 3)Up, 4)Down.")

    def doMove(self):
        '''
        Does a move.
        Asks user for which move to do.
        Checks if move is possible.
        As of right now, only prints out if move is possible or not.
        At end, generates an additional tile.
        :return: Nothing
        '''
        move = input('Choose a move: ')
        move = int(move)
        if move == 1:
            if self.canSlideRight():
                self.slideRight()
            else:
                print("Movement not possible")
        elif move == 2:
            if self.canSlideRight():
                self.slideLeft()
            else:
                print("Movement not possible")
        elif move == 3:
            if self.canSlideUp():
                self.slideUp()
            else:
                print("Movement not possible")
        elif move == 4:
            if self.canSlideDown():
                self.slideDown()
            else:
                print("Movement not possible")
        else:
            print("Error, no move inputted.")

    def playGame(self):
        '''
        Plays the game.
        Starts the game, and initiates flags for winning and losing.
        Each turn a move is made, and the game is printed.
        Conditions for the flags are then checked, and appropriate
        actions are taken if the flags are set.
        '''
        self.startGame()
        gameover = False
        gamewon = False
        while not ((gameover) or (gamewon)):
            self.doMove()
            self.printGame()
            if len(self.findFreeTiles()) == 0:
                gameover = True
                print("You have lost the game. Better luck next time.")
            if self.largest == 2048:
                gamewon = True
                print("You have won! Now go do some work you bum.")

    def clearBoard(self):
        '''
        Clears the board, resetting every position to 0.
        :return:
        '''
        for i in range(4):
            for j in range(4):
                self.tiles[i][j] = 0

    # endregion

    #region Tile Generation/Search
    def generateTile(self):
        '''
        Generates a random tile in tiles.
        First finds all the free tiles.
        From the free tiles, it chooses a random tile, into which it
        then either places a 2 or a 4.
        :return: Nothing
        '''
        self.freeTiles = self.findFreeTiles()
        slot = random.randint(0, len(self.freeTiles))
        if (random.rand() <= .9):
            self.tiles[self.freeTiles[slot][0]][self.freeTiles[slot][1]] = 2
        else:
            self.tiles[self.freeTiles[slot][0]][self.freeTiles[slot][1]] = 4

    def findFreeTiles(self):
        '''
        Finds free tiles in the board.
        Uses enumerate() to enumerate each row.
        Stores each free tile in an array as a
        list of (row, col)
        :return: Array of free tile positions
        '''
        free = []
        for i in range(4):
            for idx, val in enumerate(self.tiles[i]):
                if val == 0:
                    free.append((i, idx))
        return free

    #endregion

    #region Movement Possible?
    def canSlideRight(self):
        '''
        Checks each row if a movement left is possible.
        Sends row to checkRow() method to check.
        :return: True if movement is possible, false otherwise.
        '''
        for i in range(4):
            if self.checkRow(i):
                return True
        return False

    def canSlideLeft(self):
        '''
        Checks if a slide right is possible.
        Stores a backup of tiles.
        Flips tiles right/left.
        Calls self.canSlideLeft() to see if a movement
        left is possible on flipped tiles.
        Restores tiles from the backup
        :return: True if a move right is possible, false otherwise.
        '''
        self.tilesBackup = np.copy(self.tiles)
        self.tiles = np.fliplr(self.tiles)
        check = self.canSlideRight()
        self.tiles = self.tilesBackup
        return check

    def canSlideDown(self):
        '''
        Checks if a slide down is possible.
        Stores a backup of tiles, and then rotates tiles
        90 degrees.
        Calls self.canSlideLeft() to see if a movement
        left is possible on flipped tiles.
        Restores tiles from backup.
        :return: True if a move down is possible, false otherwise.
        '''
        self.tilesBackup = np.copy(self.tiles)
        self.tiles = np.rot90(self.tiles)
        check = self.canSlideRight()
        self.tiles = self.tilesBackup
        return check

    def canSlideUp(self):
        '''
        Checks if a slide down is possible.
        Stores a backup of tiles, and then rotates tiles
        90 degrees and then flips in left/right direction.
        Calls self.canSlideLeft() to see if a movement
        left is possible on flipped tiles.
        Restores tiles from backup.
        :return: True if a move up is possible, false otherwise.
        '''
        self.tilesBackup = np.copy(self.tiles)
        self.tiles = np.rot90(self.tiles)
        self.tiles = np.fliplr(self.tiles)
        check = self.canSlideRight()
        self.tiles = self.tilesBackup
        return check

    # Row checking method used by all movement checks
    def checkRow(self, rownum):
        '''
        Checks if there are possible moves in a single row.
        Assumes moving left.
        :param rownum: Row number to check.
        :return: True if a move is possible, false otherwise.
        '''
        row = self.tiles[rownum]
        for i in range(3):
            if(row[i] != 0 and (row[i+1] == 0 or row[i+1] == row[i])):
                return True
        return False

    #endregion

    # region Movement
    def slideRight(self):
        '''
        Slides all rows in the board right.
        Each row is passed to the helper function self.pushRow()
        one by one.
        At the end of the sliding, a tile is generated.
        Tile is generated here because tiles should only be
        generated when a move is made.
        '''
        for i in range(4):
            self.pushRow(self.tiles[i])
        self.generateTile()

    def slideLeft(self):
        '''
        A method for sliding all rows in then board left.
        Does this by first flipping the board, then calling
        self.slideRight() to move the flipped board right
        Then flip the board after to return to its original
        orientation.
        '''
        self.tiles = np.fliplr(self.tiles)
        self.slideRight()
        self.tiles = np.fliplr(self.tiles)

    def slideUp(self):
        '''
        Slides a row up. First rotates it so that the
        row is able to be pushed right.
        Pushes row right.
        Returns to original orientation.
        '''
        self.tiles = np.rot90(self.tiles)
        self.tiles = np.fliplr(self.tiles)
        self.slideRight()
        self.tiles = np.fliplr(self.tiles)
        self.tiles = np.rot90(self.tiles)
        self.tiles = np.rot90(self.tiles)
        self.tiles = np.rot90(self.tiles)

    def slideDown(self):
        '''
        Slides a row down. First rotates it so that the
        row is able to be pushed right.
        Pushes row right.
        Returns to original orientation.
        :return:
        '''
        self.tiles = np.rot90(self.tiles)
        self.slideRight()
        self.tiles = np.rot90(self.tiles)
        self.tiles = np.rot90(self.tiles)
        self.tiles = np.rot90(self.tiles)

    def pushRow(self, row):
        '''
        Pushes all tiles in the row using an algorithm.
        Upon pushing a tile forward, it saves the current
        position and moves up to the forward position, and
        rechecks for possible moves from there.
        If no move possible, it moves back to the saved state.
        If move possible, it continues forward until no move
        is left or ii == 3 (end of row).
        All pushes are done to then left.
        :param row: The row to push
        '''
        i = 2
        save = 3
        #print("Original row: {0}".format(row))
        while(i >= 0):
            if i == 3:
                i = save - 1
                continue
            if row[i] == 0:
                i = i - 1
                continue
            if row[i+1] == 0:
                row[i+1] = row[i]
                row[i] = 0
                if save > i:
                    save = i
                i = i + 1
                continue
            if row[i+1] == row[i]:
                row[i+1] = row[i+1] * 2
                if(row[i+1] > self.largest):
                    self.largest = row[i+1]
                row[i] = 0
                if save > i:
                    save = i
                i = i + 1
                continue
            else:
                if save < i:
                    i = save - 1
                else:
                    i = i - 1
                continue
        #print("New row: {0}".format(row))
    #endregion

    # region Test Utilities
    def printGame(self):
        '''
        Prints the game object
        Should be in the following format:
        =====================
        |2048|    |   2|   4|
        |    |    |    |    |
        |   2|    |    |  16|
        |    |    |    |  32|
        =====================
        '''
        result = []
        result.append("=====================\n")
        for i in range(4):
            result.append("|")
            for j in range(4):
                if (self.tiles[i][j] != 0):
                    result.append(str(self.tiles[i][j]))
                    for k in range(4 - len(str(self.tiles[i][j]))):
                        result.append(" ")
                    result.append("|")
                elif (self.tiles[i][j] == 0):
                    result.append("    |")
            result.append('\n')
        result.append("=====================\n")
        print("".join(result))
# endregion

if __name__ == '__main__':
    test = P2048()
    test.playGame()

