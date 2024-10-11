import copy

class Board:
    def __init__(self, xSquares = [], oSquares = [], rows = 5, columns = 6):
        """
        Initializes the space with a vacuum and dirty rooms

        ## Parameters
        * rows:  Number of rows for space 
            * Type: int

        * columns: Number of columns for space 
            * Type: int
         * oSquares: List of location(s) (ordered pairs) for squares claimed by no one 
            * Type: [(int, int),...]
            * (1 based index)
        * oSquares: List of location(s) (ordered pairs) for squares claimed by player o 
            * Type: [(int, int),...]
            * (1 based index)
        * xSquares: List of location(s) (ordered pairs) for squares claimed by player x 
            * Type: [(int, int),...]
            * (1 based index)
        """
        
        self.eSquares = list()
        for i in range(rows):
            for j in range(columns):
                if((i+1,j+1) not in oSquares and (i+1,j+1) not in xSquares):
                    self.eSquares.append((i+1, j+1))
                
        self.oSquares = oSquares
        self.xSquares = xSquares 
        self.rows = rows
        self.columns = columns

    def PlacePiece(self, owner, location):
        if(location[0]<1 or location[0]>= self.rows+1 or location[1]<1 or location[1] >= self.columns+1):
            print("Error OOBA", location)
            return
        if location in self.eSquares:
            self.eSquares.remove(location)
        if (owner == 'o' and location not in self.xSquares):
            self.oSquares.append(location)
        elif (owner == 'x' and location not in self.oSquares):
            self.xSquares.append(location)
        return location

    def clearPiece(self, location):
        if location in self.oSquares:
            self.oSquares.remove(location)
        if location in self.xSquares:
            self.xSquares.remove(location)
        if location not in self.eSquares:
            self.eSquares.append(location)
        return location

    def locStatus(self, location):
        if location in self.eSquares:
            return ' '
        elif location in self.xSquares:
            return 'x'
        elif location in self.oSquares:
            return 'o'
        return 'b'
            
    # Function to check if a player has won
    def CheckForWinner(self, player, loc):
        row = loc[0]
        col = loc[1]

        if(len(self.eSquares)==0):
            return True, None, None
        # Check horizontal
        # print("horizontal")
        # print("range", range(max(1, col - 3), min(col + 1, self.columns)))
        for tCol in range(max(1, col - 3), min(col + 1, self.columns)):
            a = (row,tCol)
            b = (row,tCol+1)
            c = (row,tCol+2)
            d = (row,tCol+3)
            # print([a,b,c,d])
            if(all(self.locStatus(i) == player for i in [a,b,c,d])):
                return True, player, [a,b,c,d]
            
        # Check vertical
        # print("vertical")
        # print("range", range(max(1, row - 3), min(row + 1, self.rows)))
        for tRow in range(max(1, row - 3), min(row + 1, self.rows)):
            a = (tRow,col)
            b = (tRow+1,col)
            c = (tRow+2,col)
            d = (tRow+3,col)
            # print([a,b,c,d])
            if(all(self.locStatus(i) == player for i in [a,b,c,d])):
                return True, player, [a,b,c,d]

        # Check diagonals
        # print("diagonal")
        for offset in range(0, 4):
            if row + offset >= 1 and row + offset < self.rows:
                # print(offset)
                aUp = (row - offset, col + offset)
                bUp = (row - offset + 1, col + offset - 1)
                cUp = (row - offset + 2, col + offset - 2)
                dUp = (row - offset + 3, col + offset - 3)
                # print("up", [aUp,bUp,cUp,dUp])


                upList = [aUp,bUp,cUp,dUp]
                if col - offset >= 0 and col - offset < self.columns:
                    if(all(self.locStatus(i) == player for i in upList)):
                        return True, player, upList

                # print(row, col)
                aDown = (row + offset, col + offset)
                bDown = (row + offset+1, col + offset+1)
                cDown = (row + offset+2, col + offset+2)
                dDown = (row + offset+3, col + offset+3)
                # print("down", [aDown,bDown,cDown,dDown])

                    
                downList = [aDown,bDown,cDown,dDown]
                if col + offset >= 0 and col + offset < self.columns and loc in downList:
                    # print("check")
                    if(all(self.locStatus(i) == player for i in downList)):
                        return True, player, downList
        
        return False, None, None

        
    def placableSpaces(self):
        placeable = set() 
        moves = [0, 1, -1]
        for space in self.eSquares:
            for x in moves:
                for y in moves:
                    if (x==0 and y==0):
                        pass
                    
                    # print(x, y)
                    # print(space[0]+x, space[1]+y)
                    if (((space[0]+x, space[1]+y) in self.oSquares) or ((space[0]+x, space[1]+y) in self.xSquares)):
                        placeable.add(space)
        return placeable
    
    def test_string(self,test_str,OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o):
        if ' xxx ' in test_str:
            #print("OE3x+=1")
            OE3x+=1
        if 'xxx ' in test_str and ' xxx ' not in test_str:
            #print("CE3x+=1")
            CE3x+=1
        if ' xxx' in test_str and ' xxx ' not in test_str:
            #print("CE3x+=1")
            CE3x+=1
        if ' xx ' in test_str:
            #print("OE2x+=1")
            OE2x+=1
        if 'xx '  in test_str and ' xx ' not in test_str:
            #print("CE2x+=1")
            CE2x+=1
        if ' xx' in test_str and ' xx ' not in test_str:
            #print("CE2x+=1")
            CE2x+=1
        if ' ooo ' in test_str:
            #print("OE3o+=1")
            OE3o+=1
        if 'ooo ' in test_str and ' ooo ' not in test_str :
            #print("CE3o+=1")
            CE3o+=1
        if ' ooo' in test_str and ' ooo ' not in test_str:
            #print("CE3o+=1")
            CE3o+=1
        if ' oo ' in test_str:
            #print("OE2o+=1")
            OE2o+=1
        if 'oo ' in test_str and ' oo ' not in test_str:
            #print("CE2o+=1")
            CE2o+=1
        if ' oo' in test_str and ' oo ' not in test_str:    
            #print("CE2o+=1")
            CE2o+=1

        return OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o




    def Heuristic_values(self):
        ' xxx '#valid  x perms
        'xxx '
        ' xxx'
        ' xx '
        'xx '
        ' xx'
        

        ' ooo '#valid o perms
        'ooo '
        ' ooo'
        ' oo '
        'oo '
        ' oo'

        OE3x=0# variables to record all possible perumtations, OE3x means (Open)(Ended)(3 length)(x sequences)
        CE3x=0
        OE2x=0
        CE2x=0
        
        
        OE2o=0
        CE2o=0
        OE3o=0
        CE3o=0
        current_seq=[]
        #run through all rows and calculate the given number of types
        for i in range(1,self.rows+1): #horizontal
            current_seq=[]
            test_str=""
            for j in range(1,self.columns+1):
                      current_seq.append(self.locStatus((i,j)))
            #print("-"+test_str+"-")
            test_str=''.join(current_seq)
            
            #print("-"+test_str+"-")
            (OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o)=self.test_string(test_str,OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o)
            # if ' xxx ' in test_str:
            #     print("OE3x+=1")
            #     OE3x+=1
            # if 'xxx ' in test_str and ' xxx ' not in test_str:
            #     print("CE3x+=1")
            #     CE3x+=1
            # if ' xxx' in test_str and ' xxx ' not in test_str:
            #     print("CE3x+=1")
            #     CE3x+=1
            # if ' xx ' in test_str:
            #     print("OE2x+=1")
            #     OE2x+=1
            # if 'xx '  in test_str and ' xx ' not in test_str:
            #     print("CE2x+=1")
            #     CE2x+=1
            # if ' xx' in test_str and ' xx ' not in test_str:
            #     print("CE2x+=1")
            #     CE2x+=1
            # if ' ooo ' in test_str:
            #     print("OE3o+=1")
            #     OE3o+=1
            # if 'ooo ' in test_str and ' ooo ' not in test_str :
            #     print("CE3o+=1")
            #     CE3o+=1
            # if ' ooo' in test_str and ' ooo ' not in test_str:
            #     print("CE3o+=1")
            #     CE3o+=1
            # if ' oo ' in test_str:
            #     print("OE2o+=1")
            #     OE2o+=1
            # if 'oo ' in test_str and ' oo ' not in test_str:
            #     print("CE2o+=1")
            #     CE2o+=1
            # if ' oo' in test_str and ' oo ' not in test_str:    
            #     print("CE2o+=1")
            #     CE2o+=1




        for i in range(1,self.columns+1): #vertical
            current_seq=[]
            test_str=""
            for j in range(1,self.rows+1):
                    current_seq.append(self.locStatus((j,i)))
            #print("-"+test_str+"-")    
            test_str= ''.join(current_seq)
            #print("-"+test_str+"-")
            (OE3x,OE3o,CE3x,CE3o,  OE2x,OE2o,CE2x,CE2o)=self.test_string(test_str,OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o)
            # if ' xxx ' in test_str:
            #     print("OE3x+=1")
            #     OE3x+=1
            # if 'xxx ' in test_str and ' xxx ' not in test_str:
            #     print("CE3x+=1")
            #     CE3x+=1
            # if ' xxx' in test_str and ' xxx ' not in test_str:
            #     print("CE3x+=1")
            #     CE3x+=1
            # if ' xx ' in test_str:
            #     print("OE2x+=1")
            #     OE2x+=1
            # if 'xx '  in test_str and ' xx ' not in test_str:
            #     print("CE2x+=1")
            #     CE2x+=1
            # if ' xx' in test_str and ' xx ' not in test_str:
            #     print("CE2x+=1")
            #     CE2x+=1
            # if ' ooo ' in test_str:
            #     print("OE3o+=1")
            #     OE3o+=1
            # if 'ooo ' in test_str and ' ooo ' not in test_str :
            #     print("CE3o+=1")
            #     CE3o+=1
            # if ' ooo' in test_str and ' ooo ' not in test_str:
            #     print("CE3o+=1")
            #     CE3o+=1
            # if ' oo ' in test_str:
            #     print("OE2o+=1")
            #     OE2o+=1
            # if 'oo ' in test_str and ' oo ' not in test_str:
            #     print("CE2o+=1")
            #     CE2o+=1
            # if ' oo' in test_str and ' oo ' not in test_str:    
            #     print("CE2o+=1")
            #     CE2o+=1
        #initial_vals = [(3,1), (4,1), (5,1), (5,2), (5,3) , (5,4)]
        initial_vals=[] 

        for i in range(3, self.rows+1):
            initial_vals.append((i, 1))


        for j in range(2, self.columns-1):
            initial_vals.append((self.rows, j))

        #print(initial_vals,"upward diags")
        for initial in initial_vals:
            current_seq=[]
            test_str=""
            for i in range(0,self.rows+1):
                current_seq.append(self.locStatus(((initial[0]-i, initial[1]+i))))
            #print("-"+test_str+"-")
            test_str= ''.join(current_seq)    
            test_str=test_str.strip('b')
            #print("-"+test_str+"-")
            (OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o)=self.test_string(test_str,OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o)

            # if ' xxx ' in test_str:
            #     print("OE3x+=1")
            #     OE3x+=1
            # if 'xxx ' in test_str and ' xxx ' not in test_str and 'bxxx' not in test_str:
            #     print("CE3x+=1")
            #     CE3x+=1
            # if ' xxx' in test_str and ' xxx ' not in test_str and 'xxxb' not in test_str:
            #     print("CE3x+=1")
            #     CE3x+=1
            # if ' xx ' in test_str:
            #     print("OE2x+=1")
            #     OE2x+=1
            # if 'xx '  in test_str and ' xx ' not in test_str:
            #     print("CE2x+=1")
            #     CE2x+=1
            # if ' xx' in test_str and ' xx ' not in test_str:
            #     print("CE2x+=1")
            #     CE2x+=1
            # if ' ooo ' in test_str:
            #     print("OE3o+=1")
            #     OE3o+=1
            # if 'ooo ' in test_str and ' ooo ' not in test_str :
            #     print("CE3o+=1")
            #     CE3o+=1
            # if ' ooo' in test_str and ' ooo ' not in test_str:
            #     print("CE3o+=1")
            #     CE3o+=1
            # if ' oo ' in test_str:
            #     print("OE2o+=1")
            #     OE2o+=1
            # if 'oo ' in test_str and ' oo ' not in test_str:
            #     print("CE2o+=1")
            #     CE2o+=1
            # if ' oo' in test_str and ' oo ' not in test_str:    
            #     print("CE2o+=1")
            #     CE2o+=1


                






        initial_vals=[] 

        for i in range(1, self.rows-1):
            initial_vals.append((i, 1))


        for j in range(1, self.columns-1):
            initial_vals.append((1, j))

        #print(initial_vals,"downward diags")
        for initial in initial_vals:
            current_seq=[]
            test_str=""
            for i in range(0,self.rows+1):
                current_seq.append(self.locStatus(((initial[0]+i, initial[1]+i))))
            #print("-"+test_str+"-")
            test_str= ''.join(current_seq)    
            test_str=test_str.strip('b')
            #print("-"+test_str+"-")
            (OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o)=self.test_string(test_str,OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o)
            # if ' xxx ' in test_str:
            #     print("OE3x+=1")
            #     OE3x+=1
            # if 'xxx ' in test_str and ' xxx ' not in test_str and 'bxxx' not in test_str:
            #     print("CE3x+=1")
            #     CE3x+=1
            # if ' xxx' in test_str and ' xxx ' not in test_str and 'xxxb' not in test_str:
            #     print("CE3x+=1")
            #     CE3x+=1
            # if ' xx ' in test_str:
            #     print("OE2x+=1")
            #     OE2x+=1
            # if 'xx '  in test_str and ' xx ' not in test_str:
            #     print("CE2x+=1")
            #     CE2x+=1
            # if ' xx' in test_str and ' xx ' not in test_str:
            #     print("CE2x+=1")
            #     CE2x+=1
            # if ' ooo ' in test_str:
            #     print("OE3o+=1")               
            #     OE3o+=1
            # if 'ooo ' in test_str and ' ooo ' not in test_str :
            #     print("CE3o+=1")
            #     CE3o+=1
            # if ' ooo' in test_str and ' ooo ' not in test_str:
            #     print("CE3o+=1")
            #     CE3o+=1
            # if ' oo ' in test_str:
            #     print("OE2o+=1")
            #     OE2o+=1
            # if 'oo ' in test_str and ' oo ' not in test_str:
            #     print("CE2o+=1")
            #     CE2o+=1
            # if ' oo' in test_str and ' oo ' not in test_str:    
            #     print("CE2o+=1")
            #     CE2o+=1

        
        return OE3x,OE3o,CE3x,CE3o,  OE2x,OE2o,CE2x,CE2o

    def Heuristic(self, player):
        values = self.Heuristic_values()
        #print(values)
        if player == 'x':
            # print(200* values[0]) 
            # print(-80 *   values[1])
            # print(+150*   values[2])
            # print(-40 *   values[3])
            # print(+20 *   values[4])
            # print(-15 *   values[5])
            # print(+5  *   values[6])
            # print(-2  *   values[7])
            return 200* values[0] \
                -80 *   values[1] \
                +150*   values[2] \
                -40 *   values[3] \
                +20 *   values[4] \
                -15 *   values[5] \
                +5  *   values[6] \
                -2  *   values[7]
        else:
            # print(200 *   values[1]) 
            # print(-80 *   values[0])
            # print(+150*   values[3])
            # print(-40 *   values[2])
            # print(+20 *   values[5])
            # print(-15 *   values[4])
            # print(+5  *   values[7])
            # print(-2  *   values[6])
            return 200* values[1] \
                -80 *   values[0] \
                +150*   values[3] \
                -40 *   values[2] \
                +20 *   values[5] \
                -15 *   values[4] \
                +5  *   values[7] \
                -2  *   values[6] 
   
    def printFloorLayout(self):
        """
        Displays the layout of the space
        each sell has format (row, colum)
        * If the space contains a piece it will display 'x' or 'o'
        """
        
        print("  | ", end="")

        for i in range(self.rows+1):
            for j in range(self.columns+1):
                if (i==0):
                    if j != self.columns:
                        print(j+1, end=" | ")
                else:
                    if(j==0):
                        print(i, end=" | ")
                    else:
                        # print(" ", end="")
                        print(self.locStatus((i,j)), end=" | ")
            print()

            
class Player:
    def __init__(self, FirstMove, LookAheadDepth, piece):
        self.FirstMove = FirstMove
        self.LookAheadDepth = LookAheadDepth
        self.piece = piece

    def Move(self, board, MaxLayer):
        result = MinimaxDecision(board, self, 0, MaxLayer)
        board.PlacePiece(self.piece, result)
        return result

def MinimaxDecision(board, player, CurrentDepth, MaxLayer):

    placableSpaces = board.placableSpaces()
    Results = []
    Spaces = []
    #print(placableSpaces)
    for space in placableSpaces:
        newBoard = copy.deepcopy(board)
        newBoard.PlacePiece(player,space)
        IsEnd, EndResult, downList = newBoard.CheckForWinner(player,(3,3))
        if(IsEnd and EndResult == player):
            return space
        if player.piece == 'x':
            Results.append(MinValue(newBoard,'o',CurrentDepth+1,MaxLayer))
            Spaces.append(space)
        else:
            Results.append(MinValue(newBoard,'x',CurrentDepth+1,MaxLayer))
            Spaces.append(space)
    maxResult = max(Results)
    index = Results.index(maxResult)
    return Spaces[index]

def MaxValue(board, player, CurrentDepth, MaxDepth):
    IsEnd, EndResult, downList = board.CheckForWinner(player,(3,3))
    if(IsEnd and EndResult == player):
        return 1000
    elif (IsEnd and EndResult == None):
        return 0
    elif (IsEnd):
        return -1000
    if CurrentDepth == MaxDepth:
        return board.Heuristic(player)
    
    value = -999999999
    Result = None
    placableSpaces = board.placableSpaces()
    for space in placableSpaces:
        newBoard = copy.deepcopy(board)
        newBoard.PlacePiece(player,space)
        IsEnd, EndResult, downList = board.CheckForWinner(player,(3,3))
        if IsEnd and EndResult == player:
            return space
        if player == 'x':
            ResultVal = MinValue(newBoard,'o',CurrentDepth+1,MaxDepth)
            if ResultVal > value:
                value = ResultVal       
        else:
            ResultVal = MinValue(newBoard,'x',CurrentDepth+1,MaxDepth)
            if ResultVal > value:
                value = ResultVal
    return value
        
def MinValue(board, player, CurrentDepth, MaxDepth):
    IsEnd, EndResult, downList = board.CheckForWinner(player,(3,3))
    if(IsEnd and EndResult == player):
        return 1000
    elif (IsEnd and EndResult == None):
        return 0
    elif (IsEnd):
        return -1000
    
    if CurrentDepth == MaxDepth:
        return board.Heuristic(player)
    
    value = 999999999
    Result = None
    placableSpaces = board.placableSpaces()
    for space in placableSpaces:
        newBoard = copy.deepcopy(board)
        newBoard.PlacePiece(player,space)
        if player == 'x':
            ResultVal = MaxValue(newBoard,'o',CurrentDepth+1,MaxDepth)
            if ResultVal < value:
                value = ResultVal
                Result = space
        else:
            ResultVal = MaxValue(newBoard,'x',CurrentDepth+1,MaxDepth)
            if ResultVal < value:
                value = ResultVal
                Result = space       
    return value


# function Minimax-Decision(state) returns an action
# inputs: state, current state in game
# return the a in Actions(state) maximizing Min-Value(Result(a, state))

# function Max-Value(state) returns a utility value
# if Terminal-Test(state) then return Utility(state)
# v← − ∞
# for a, s in Successors(state) do v← Max(v, Min-Value(s))
# return v

# function Min-Value(state) returns a utility value
# if Terminal-Test(state) then return Utility(state)
# v← ∞
# for a, s in Successors(state) do v← Min(v, Max-Value(s))
# return v   
            
def PlayGame(board, p1, p2):
    IsEnd = False
    EndResult = None
    board.PlacePiece('x',(3,4))
    board.PlacePiece('o',(3,3))
    #board.printFloorLayout()
    while(1):
        board.printFloorLayout()
        movement = p1.Move(board,2)
        IsEnd, EndResult, lst = board.CheckForWinner('x',movement)
        if IsEnd:
            break
        board.printFloorLayout()
        print("\n")
        #p2.Move(board,4)
        x = input("row: ")
        y = input("column: ")
        board.PlacePiece('o',(int(x),int(y)))
        IsEnd, EndResult, lst = board.CheckForWinner('o',movement)
        if IsEnd:
            break
        print("\n")
    if EndResult == None:
        print("Match was a draw")
    else:
        print(EndResult +" is the winner")
    return 0

def main():
    board = Board(rows=5,columns=6)    
    player1 = Player((3,4),2,'x')
    player2 = Player((3,3),4,'o')
    PlayGame(board, player1, player2)

    # print(board.placableSpaces())
    # # board.PlacePiece('o',(1,4))
    # # board.PlacePiece('o',(1,2))
    # print(board.placableSpaces())
    # # board.printFloorLayout()
    # # for d in range(0,4):    
    # #     for i in range(0, board.rows):
    # #         for j in range(1, board.columns):
    # #                 board.PlacePiece('o', (i+j+d,i+j+d))
    # initial_vals = [(3,1)]  #, (4,1), (5,1), (5,2), (5,3) , (5,4)
    # for initial in initial_vals:
    #     for i in range(1, board.rows):
    #         new = (initial[0]-i, initial[1]+i)
    #         board.PlacePiece('o', new)


    # initial_vals = [(4,2)]  #, (4,1), (5,1), (5,2), (5,3) , (5,4)
    # for initial in initial_vals:
    #     for i in range(0, 3):
    #         new = (abs(initial[0]-i-7), initial[1]+i)
    #         board.PlacePiece('o', new)

    # board.PlacePiece('o',(1,4))
    # board.PlacePiece('o',(1,2))

    # # for i in range(0, board.rows):
    # #     new = (initial[0]+i, initial[1]+i)
    # #     board.PlacePiece('o', new)
    


    # # for j in range(1,3):
    # #     board.PlacePiece('o', (1,j))
    # # for i in range(4,6):
    # #     board.PlacePiece('x', (1,i))    
    # print()
    # board.printFloorLayout()
    # place = (1,4)
    # # print(board.CheckForWinner('o',place ))


    # print(board.Heuristic('x'))
    # print("\n\n")
    # print(board.Heuristic('o'))



    return 0

if(__name__ == "__main__"):
    main()