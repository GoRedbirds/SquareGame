"""
Only works on the Codeskulptor

This is the basic square game that we all played back in 3rd grade
Click a line to fill it in
If you fill in the last line of a square, you get a point
You can tell whose turn it is by the color of the lines at the bottom
Link here:
https://py3.codeskulptor.org/#user305_PUOB8nqvCXL3OFe.py
"""

import simplegui

GHEIGHT = 5
GWIDTH = 5


class Square():
    def __init__(self):
        self.top = False
        self.bottom = False
        self.right = False
        self.left = False
        
        self.occupied = ""
        
    def changeLine(self, side, turn):
        if side == "top": self.top = True
        if side == "bottom": self.bottom = True
        if side == "right": self.right = True
        if side == "left": self.left = True
        
        if self.top and self.bottom and self.right and self.left:
            self.occupied = turn
            return 1
        else: return 0
    
    def getOccupied(self):
        return self.occupied

    
    
    #getters
    def getTop(self): return self.top
    def getBottom(self): return self.bottom
    def getRight(self): return self.right
    def getLeft(self): return self.left

    
class SquareGame():
    def __init__(self, width, height):
        self.player1 = "orange"
        self.player2 = "blue"
        
        self.turn = self.player1
        
        self.player1Score = 0
        self.player2Score = 0
        
        self.height = height
        self.width = width
        
        self.border = 30
        self.sLength = 40
        self.lLength = 6
        self.cExp = 2
        self.scoreHeight = 100
        
        self.board = [[Square() for dummy1 in range(self.width)]
                      for dummy2 in range(self.height)]
    
    def mouseClick(self, pos):
        dims = self.getDimensions()
        
        points = 0
        success = False
        #checks to see if click actually changed a line
        
        #horizontal lines
        if abs(((pos[1]-self.border+0.5*self.lLength)%self.sLength)) <= self.lLength:
            if (pos[0] > self.border - self.lLength and pos[0] < dims[0]-self.border-self.lLength):
                success = True
                #horizontal lines
                xIndex = int((pos[0]-self.border+self.lLength/2)/self.sLength)
                yIndex = int((pos[1]-self.border+self.lLength/2)/self.sLength)
                if yIndex < self.height:
                    points += self.board[yIndex][xIndex].changeLine('top', self.turn)
                    #add statement about score
                if yIndex > 0:
                    points += self.board[yIndex-1][xIndex].changeLine('bottom', self.turn)
                    
        elif (abs(((pos[0]-self.border+0.5*self.lLength)%self.sLength)) <= self.lLength):
            if (pos[1] > self.border - self.lLength and pos[1] < dims[1]-self.border-self.lLength-self.scoreHeight):
                success = True
                #horizontal lines
                xIndex = int((pos[0]-self.border+self.lLength/2)/self.sLength)
                yIndex = int((pos[1]-self.border+self.lLength/2)/self.sLength)
                if xIndex < self.width:
                    points += self.board[yIndex][xIndex].changeLine('left', self.turn)
                if xIndex > 0:
                    points += self.board[yIndex][xIndex-1].changeLine('right', self.turn)
                #scoring calculations
                
        if success:
            
            if self.turn == self.player1:
                self.player1Score += points
                self.turn = self.player2
            else:
                self.player2Score += points
                self.turn = self.player1
        
    
    def draw_circle(self, point, canvas):
        canvas.draw_circle(point, self.lLength/2*self.cExp, 1, "grey", "grey")
        
    def draw(self, canvas):
        #draw the points
        for index1 in range(self.height):
            for index2 in range(self.width):
                point = (self.border + index2*self.sLength,
                         self.border + index1*self.sLength)
                rightPoint = (point[0]+self.sLength, point[1])
                bottomPoint = (point[0], point[1] + self.sLength)
                
                #draw square(only here)
                color = self.board[index1][index2].getOccupied()
                if bool(color):
                    cornerPoint = (rightPoint[0], bottomPoint[1])
                    canvas.draw_polygon([point, rightPoint, cornerPoint, bottomPoint], 1, color, color) 
                
                #horizontal lines
                if (self.board[index1][index2].getTop()):
                    canvas.draw_line(point, rightPoint, self.lLength, "black")
                else: canvas.draw_line(point, rightPoint, self.lLength, "white")
                #vertical lines
                if (self.board[index1][index2].getLeft()):
                    canvas.draw_line(point, bottomPoint, self.lLength, "black")
                else: canvas.draw_line(point, bottomPoint, self.lLength, "white")             
                
                #draw circle
                self.draw_circle(point, canvas)
                
            #the end of the row (rightmost)
            cornerPoint = (rightPoint[0], bottomPoint[1])
            if (self.board[index1][index2].getRight()):
                canvas.draw_line(rightPoint, cornerPoint, self.lLength, "black")
            else: canvas.draw_line(rightPoint, cornerPoint, self.lLength, "white")
            self.draw_circle(rightPoint, canvas)
            
        #bottom row
        for index2 in range(self.width):
            point = [self.border + index2*self.sLength, self.border + self.height*self.sLength]
            rightPoint = (point[0]+self.sLength, point[1])

            if (self.board[index1][index2].getBottom()):
                canvas.draw_line(point, rightPoint, self.lLength, "black")
            else: canvas.draw_line(point, rightPoint, self.lLength, "white")
            self.draw_circle(point, canvas)
            
        #bottom right dot
        self.draw_circle(rightPoint, canvas)
    
        #score
        dims = self.getDimensions()
        WIDTH = dims[0]
        HEIGHT = dims[1]
        os_width = frame.get_canvas_textwidth(str(self.player1Score), self.scoreHeight*0.9)
        canvas.draw_text(str(self.player1Score), (WIDTH/2 - os_width-10, HEIGHT-self.scoreHeight*0.1), self.scoreHeight*0.9, self.player1)
        canvas.draw_text(str(self.player2Score), (WIDTH/2 + 10, HEIGHT -self.scoreHeight*0.1), self.scoreHeight*0.9, self.player2)
        #draw graphics lines to make things look nicer
        canvas.draw_line((0, HEIGHT-self.scoreHeight), (WIDTH, HEIGHT - self.scoreHeight), self.lLength*1.5, self.turn)
        canvas.draw_line((WIDTH/2, HEIGHT-self.scoreHeight), (WIDTH/2, HEIGHT), self.lLength*1.5, self.turn)
        
        
    def getDimensions(self):
        return (self.border*2 + self.width*self.sLength,
                self.border*2 + self.height*self.sLength + self.scoreHeight)
    
    
game = SquareGame(GWIDTH, GHEIGHT)
dims = game.getDimensions()


frame = simplegui.create_frame("Home", dims[0], dims[1])
frame.set_canvas_background("green")
frame.set_draw_handler(game.draw)
frame.set_mouseclick_handler(game.mouseClick)

frame.start()
