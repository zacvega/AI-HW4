import copy
import time


class Board:
    def __init__(self, xSquares = [], oSquares = [], rows = 5, columns = 6):
        """
        Initializes the space as a nxm matrix by rows and columns, 

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
        #the number of squares in the board that are not x or o
        self.eSquares = list() 
        for i in range(rows):
            for j in range(columns):
                if((i+1,j+1) not in oSquares and (i+1,j+1) not in xSquares): 
                    self.eSquares.append((i+1, j+1))
        #init values to themselves        
        self.oSquares = oSquares  
        self.xSquares = xSquares 
        self.rows = rows
        self.columns = columns


    #place a piece as 'x' or 'o' at a given board location
    def PlacePiece(self, owner, location):
        #validate location is on the board
        if(location[0]<1 or location[0]>= self.rows+1 or location[1]<1 or location[1] >= self.columns+1): 
            return
        
        #if pos is empty, place 
        if location in self.eSquares: 
            self.eSquares.remove(location)

        #if you are o's and location isn't an x, place here
        if (owner == 'o' and location not in self.xSquares): 
            self.oSquares.append(location)

        #if you are x's and location isn't an o, place here
        elif (owner == 'x' and location not in self.oSquares):
            self.xSquares.append(location)

        return location
    
    
    #clear a board space (just used for debugging)
    def clearPiece(self, location): 

        #clear from o spaces
        if location in self.oSquares: 
            self.oSquares.remove(location) 

        #clear from x spaces
        if location in self.xSquares: 
            self.xSquares.remove(location) 
        
        #if location not in empty spaces, add it
        if location not in self.eSquares: 
            self.eSquares.append(location)
        
        return location


    #given a location, return empty, x, or o, if not on board, return 'b' for out of bounds
    def locStatus(self, location):
        if location in self.eSquares:
            return ' '
        elif location in self.xSquares:
            return 'x'
        elif location in self.oSquares:
            return 'o'
        return 'b'
            
    # Function to check if a player has won or if there is a tie takes a location, and a player
    def CheckForWinner(self, player, loc):
        row = loc[0]     
        col = loc[1]        
        
        # Create horizontal list of possible horizontal 4 in a rows, based on given location
        for tCol in range(max(1, col - 3), min(col + 1, self.columns)): 
            a = (row,tCol)
            b = (row,tCol+1)
            c = (row,tCol+2)
            d = (row,tCol+3)
            # print("horiz", [a,b,c,d])

            #check list of 4 in a rows for matching winning sequence
            if(all(self.locStatus(i) == player for i in [a,b,c,d])):

                #return true, player, and winning sequence
                return True, player, [a,b,c,d]


        # Create vertical list of possible vertical 4 in a rows, based on given location
        for tRow in range(max(1, row - 3), min(row + 1, self.rows)):
            a = (tRow,col)
            b = (tRow+1,col)
            c = (tRow+2,col)
            d = (tRow+3,col)
            # print("vert", [a,b,c,d])

            #check list of 4 in a rows for matching winning sequence
            if(all(self.locStatus(i) == player for i in [a,b,c,d])):

                #return true, player, and winning sequence
                return True, player, [a,b,c,d]



        # Create diagonal list of possible diagonal 4 in a rows with upward slope, based on given location
        for offset in range(-4, 4):
            aUp = (row - offset, col + offset)
            bUp = (row - offset + 1, col + offset - 1)
            cUp = (row - offset + 2, col + offset - 2)
            dUp = (row - offset + 3, col + offset - 3)




            upList = [aUp,bUp,cUp,dUp]
            # print("up", upList)

            #check list of 4 in a rows for matching winning sequence
            if(all(self.locStatus(i) == player for i in upList)):
                
                #return true, player, and winning sequence
                return True, player, upList



            # Create diagonal list of possible diagonal 4 in a rows with downward slope, based on given location
            # print(row, col)
            aDown = (row + offset, col + offset)
            bDown = (row + offset+1, col +offset+1)
            cDown = (row + offset+2, col +offset+2)
            dDown = (row + offset+3, col +offset+3)
            # print("down", [aDown,bDown,cDown,dDown])

            #check list of 4 in a rows for matching winning sequence    
            downList = [aDown,bDown,cDown,dDown]
            if(all(self.locStatus(i) == player for i in downList)):

                #return true, player, and winning sequence
                return True, player, downList
        
        # if the board is full, return true without a winner set, this allows detect ties
        if(len(self.eSquares)==0): 
            return True, None, None
            
        return False, None, None

    #detect what spaces are placable (x or o can place there) given the state of the board    
    def placableSpaces(self):
        placeable = set() 
        moves = [0, 1, -1]

        #retrieve spaces from empty squares
        for space in self.eSquares:
            for x in moves:
                for y in moves:
                    if (x==0 and y==0):
                        pass
                    
                    #if the current space we are looking at is touching an x or an o it is a valid space, add it to the list of spaces
                    if (((space[0]+x, space[1]+y) in self.oSquares) or ((space[0]+x, space[1]+y) in self.xSquares)):
                        placeable.add(space)
        return placeable
    

    #this function contains the sequences that the heuristic_values function checks for to determine the state of the given board
    #it takes a string with the given slice of the board, and checks it for substrings that contain valid heuristic significant sequences
    def test_string(self,test_str,OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o):
        test_str = test_str.replace(" ", "_")
        # print(f'"{test_str.replace(" ", "_")}"')
        if '_xxx_' in test_str:
            #print("OE3x+=1")
            OE3x+=1
        if 'xxx_' in test_str and '_xxx_' not in test_str:
            #print("CE3x+=1")
            CE3x+=1
        if '_xxx' in test_str and '_xxx_' not in test_str:
            #print("CE3x+=1")
            CE3x+=1
        if '_xx_' in test_str:
            #print("OE2x+=1")
            OE2x+=1
        if 'xx__'  in test_str and '_xx_' not in test_str:
            #print("CE2x+=1")
            CE2x+=1
        if '__xx' in test_str and '_xx_' not in test_str:
            #print("CE2x+=1")
            CE2x+=1
        if '_ooo_' in test_str:
            #print("OE3o+=1")
            OE3o+=1
        if 'ooo_' in test_str and '_ooo_' not in test_str :
            #print("CE3o+=1")
            CE3o+=1
        if '_ooo' in test_str and '_ooo_' not in test_str:
            #print("CE3o+=1")
            CE3o+=1
        if '_oo_' in test_str:
            #print("OE2o+=1")
            OE2o+=1
        if 'oo__' in test_str and '_oo_' not in test_str:
            #print("CE2o+=1")
            CE2o+=1
        if '__oo' in test_str and '_oo_' not in test_str:    
            #print("CE2o+=1")
            CE2o+=1

        #return all the recorded heuristic significant figures
        return OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o

    #looks at the entire board, and returns the current heuristic significant places
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

        # variables to record all possible permutations, OE3x means (Open)(Ended)(3 length)(x sequences)
        OE3x=0
        CE3x=0
        OE2x=0
        CE2x=0
        
        
        OE2o=0
        CE2o=0
        OE3o=0
        CE3o=0

        #list to contain current sequence
        current_seq=[] 

        #run through all rows and calculate the given number of types
        for i in range(1,self.rows+1): #horizontal
            current_seq=[]
            test_str=""

            #each time you loop through the board, get the value at that given location, in this example, get a whole row as a list
            for j in range(1,self.columns+1):
                current_seq.append(self.locStatus((i,j)))
            #print("-"+test_str+"-")

            #convert the list into a string
            test_str=''.join(current_seq)
            
            #print("-"+test_str+"-")

            #using the above function where we use the "in" string function, detect the heuristic significant structures that form in a horizontal pattern
            (OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o)=self.test_string(test_str,OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o)
           
        #vertical
        #run through columns and find sequences
        for i in range(1,self.columns+1):
            current_seq=[]
            test_str=""

            #each time you loop through the board, get the value at that given location, in this example, get a whole column as a list
            for j in range(1,self.rows+1):
                    current_seq.append(self.locStatus((j,i)))
            #print("-"+test_str+"-")    

            #convert the list into a string
            test_str= ''.join(current_seq)
            #print("-"+test_str+"-")

            #using the above function where we use the "in" string function, detect the heuristic significant structures that form in a vertical pattern
            (OE3x,OE3o,CE3x,CE3o,  OE2x,OE2o,CE2x,CE2o)=self.test_string(test_str,OE3x,OE3o,CE3x,CE3o,OE2x,OE2o,CE2x,CE2o)
           
        
        

        #for diagonals, we restrict the board to only the diagonals that can form valid sequences (any thing less than length of 3 is not considered)
        #to do this, we get initial starting values of the rows where a valid diagonal can form, for this one we are doing downward
        initial_vals=[] 


        for i in range(3, self.rows+1):
            initial_vals.append((i, 1))


        for j in range(2, self.columns-1):
            initial_vals.append((self.rows, j))


        #loop through the board, retrieving the diagonals and running them through the same string checking we did before
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

       


        #same thing, but we get starting points for diagonals that slope upward
        initial_vals=[] 

        for i in range(1, self.rows-1):
            initial_vals.append((i, 1))


        for j in range(1, self.columns-1):
            initial_vals.append((1, j))


        #same as above, just with downward diagonals
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
         
        return OE3x,OE3o,CE3x,CE3o,  OE2x,OE2o,CE2x,CE2o


    #this function calculates the value of a potential board state for a player depending if they are x or o
    #the calculation for the heuristic is given by the instructor
    def Heuristic(self, player):
        values = self.Heuristic_values()
        #print(values)
        if player == 'x':
            # print(f'200 * {values[0]}') 
            # print(f'-80 * {values[1]}')
            # print(f'150 * {values[2]}')
            # print(f'-40 * {values[3]}')
            # print(f'20 * {values[4]}')
            # print(f'-15 * {values[5]}')
            # print(f'5 * {values[6]}')
            # print(f'-2 * {values[7]}')
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

            
#player class, allows for starting move, lookahead depth, and piece type params

#starting move is fixed location on the board where you start the game
#lookahead depth is for player AI on how many turns they should look ahead when considering placing a piece
#piece is x or o
class Player:
    def __init__(self, FirstMove, LookAheadDepth, piece):
        self.FirstMove = FirstMove
        self.LookAheadDepth = LookAheadDepth
        self.piece = piece

    #function for move

    #board, current board state
    #MaxLayer, same as look ahead depth
    def Move(self, board, MaxLayer):

        #records the starting time of move, to track how long it takes the AI player to make a move
        start = time.process_time()
        result, nodesGenerated = MinimaxDecision(board, self, 0, MaxLayer)
        board.PlacePiece(self.piece, result)
        return result, (time.process_time() - start), nodesGenerated



#function to find the highest board state for given a turn and a player

#it works by looping over all current valid playable spaces, adding the heuristic values of the board if a player were to place a piece there, then finding the best value
#after which, it calls Min and Max respectively to get the best and worst value at that board state, based on that, it decides where to place a piece

def MinimaxDecision(board, player, CurrentDepth, MaxLayer):

    Results = []
    Spaces = []
    nodesGenerated = 0
    # print("Starting player ", player.piece)
    for space in board.placableSpaces():
        nodesGenerated+=1
        newBoard = copy.deepcopy(board)
        newBoard.PlacePiece(player.piece,space)
        IsEnd, EndResult, downList = newBoard.CheckForWinner(player.piece,space)
        # print(space, IsEnd, EndResult, EndResult == player.piece)
        if(IsEnd and EndResult == player.piece):
            return space, nodesGenerated

        if player.piece == 'x':
            result, nodesMade = MinValue(newBoard,'o',CurrentDepth+1,MaxLayer)
            Results.append(result)
            Spaces.append(space)
            nodesGenerated += nodesMade
        else:
            result, nodesMade = MinValue(newBoard,'x',CurrentDepth+1,MaxLayer)
            Results.append(result)
            Spaces.append(space)
            nodesGenerated += nodesMade
    
    maxResult = max(Results)
    move = None 
    for count, space in enumerate(Spaces):
        if Results[count] == maxResult:
            if move == None:
                move = space
            else:
                if (space[1] < move[1]) or (space[1] == move[1] and space[0] < move[0]):
                    move = space
    #     print(Results[count], space)
    # print()
    # print(maxResult, move)
    return move, nodesGenerated

#find the largest value heuristic value from a given board and keep track of the ammount of nodes that are generated
def MaxValue(board, player, CurrentDepth, MaxDepth,):
    nodesGenerated = 0
    if CurrentDepth == MaxDepth:
        return board.Heuristic(player),nodesGenerated
    # print(f"\tplayer {player}, depth: {CurrentDepth}")

    value = -999999999
    Result = None
    placableSpaces = board.placableSpaces()
    for space in placableSpaces:
        nodesGenerated+=1
        newBoard = copy.deepcopy(board)
        newBoard.PlacePiece(player,space)
        IsEnd, EndResult, downList = newBoard.CheckForWinner(player,space)
        if(IsEnd and EndResult == player):
            return 1000,nodesGenerated
        elif (IsEnd):
            return 0,nodesGenerated


        if player == 'x':
            ResultVal,generated = MinValue(newBoard,'o',CurrentDepth+1,MaxDepth)
            nodesGenerated += generated
            if ResultVal > value:
                value = ResultVal       
        else:
            ResultVal,generated = MinValue(newBoard,'x',CurrentDepth+1,MaxDepth)
            nodesGenerated += generated
            if ResultVal > value:
                value = ResultVal

    return value,nodesGenerated
        
def MinValue(board, player, CurrentDepth, MaxDepth):
    nodesGenerated = 0
    if CurrentDepth == MaxDepth:
        return board.Heuristic(player), nodesGenerated

    # print(f"\tplayer {player}, depth: {CurrentDepth}")

    value = 999999999
    Result = None
    placableSpaces = board.placableSpaces()
    for space in placableSpaces:
        nodesGenerated+=1
        newBoard = copy.deepcopy(board)
        newBoard.PlacePiece(player,space)

        IsEnd, EndResult, downList = newBoard.CheckForWinner(player,space)
        if(IsEnd and EndResult == player):
            return -1000,nodesGenerated
        elif (IsEnd):
            return 0,nodesGenerated
        
        if player == 'x':
            ResultVal,generated = MaxValue(newBoard,'o',CurrentDepth+1,MaxDepth)
            nodesGenerated += generated
            if ResultVal < value:
                value = ResultVal
                Result = space
        else:
            ResultVal,generated = MaxValue(newBoard,'x',CurrentDepth+1,MaxDepth)
            nodesGenerated += generated
            if ResultVal < value:
                value = ResultVal
                Result = space       
    return value,nodesGenerated


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
            
def PlayGame(board, p1, p2, plAuto = True, p2Auto = True):
    IsEnd = False
    EndResult = None
    actionList = []
    if plAuto:
        board.PlacePiece('x',p1.FirstMove)
        actionList.append(('x', p1.FirstMove))
    else:
        start = time.process_time()
        print("P1: ")
        x = input("\trow: ")
        y = input("\tcolumn: ")
        movementX = board.PlacePiece('x',(int(x),int(y)))
        actionList.append(('x', movementX))
        IsEnd, EndResult, lst = board.CheckForWinner('x',(int(x),int(y)))
        print()

    board.printFloorLayout()
    print()
    if p2Auto:
        board.PlacePiece('o',p2.FirstMove)
        actionList.append(('o', p2.FirstMove))
    else:
        start = time.process_time()
        print("P2: ")
        x = input("\trow: ")
        y = input("\tcolumn: ")
        movementX = board.PlacePiece('o',(int(x),int(y)))
        actionList.append(('o', movementX))
        IsEnd, EndResult, lst = board.CheckForWinner('o',(int(x),int(y)))
        print()

        
    xTurns = 1
    oTurns = 1

    # player 1 goes then player 2 goes
    while(1):
        xTurns +=1
        board.printFloorLayout()
        if plAuto:
            movementX, timeTaken, nodesGenerated = p1.Move(board,p1.LookAheadDepth)
            IsEnd, EndResult, lst = board.CheckForWinner('x',movementX)
            movementX = actionList.append(('x', movementX, timeTaken, nodesGenerated))

            
        #Condition used in testing 
        else:
            print("P1: ")
            x = input("\trow: ")
            y = input("\tcolumn: ")
            movementX = board.PlacePiece('x',(int(x),int(y)))
            actionList.append(('x', movementX))
            IsEnd, EndResult, lst = board.CheckForWinner('x',(int(x),int(y)))
            print()
            
        if IsEnd:
            break
        print()
        board.printFloorLayout()

        oTurns +=1
        if p2Auto:
            movementO, timeTaken, nodesGenerated =  p2.Move(board,p2.LookAheadDepth)
            IsEnd, EndResult, lst = board.CheckForWinner('o',movementO)
            actionList.append(('o', movementO, timeTaken, nodesGenerated))

        else:
            print("P2: ")
            x = input("\trow: ")
            y = input("\tcolumn: ")
            movementO = board.PlacePiece('o',(int(x),int(y)))
            actionList.append(('o', movementO))
            IsEnd, EndResult, lst = board.CheckForWinner('o',(int(x),int(y)))
            print()

        if IsEnd:
            break
        print()

    print()
    board.printFloorLayout()

    print("Move list:")
    totalTime = 0
    for i in actionList:
        print(f'\t{i}')
        if len(i) > 2:
            totalTime += i[2]
    
    print(f'\nTotal time: {totalTime}')
    # print(actionList)
    print(f'X turns: {xTurns}, O turns: {oTurns}, Total turns {xTurns + oTurns}')
    if EndResult == None:
        print("Match was a draw")
    else:
        print(EndResult +" is the winner")


    return 0

def main():
    #create playing area
    board = Board(rows=5,columns=6)   
    # locations = [(2,4),(3,5),(4,3),(4,4),(5,3)]
    # locations2 = [(2,3),(3,3),(3,4),(4,2),(4,5)]

    # for loc in locations:
    #     board.PlacePiece('x', loc)

    # for loc in locations2:
    #     board.PlacePiece('o', loc)
    # board.printFloorLayout()
    # print(board.Heuristic('x'))
    # player 1 (Starting spot, look ahead, piece)  
    player1 = Player((3,4),2,'x') 

    # player 2 (Starting spot, look ahead, piece)
    player2 = Player((3,3),4,'o')

    #start game between player 1 and player 2
    PlayGame(board, player1, player2) 
    
    return 0

if(__name__ == "__main__"):
    main()