# class Board:
#     def __init__(self):
#         self.board = [5][6]

#     def placeableSpaces(self):

#     def CheckForWinner(self):


class Player:
    def __init__(self, FirstMove, LookAheadDepth):
        self.FirstMove = FirstMove
        self.LookAheadDepth = LookAheadDepth

    def Move(self, board):
        result = MinimaxDecision(board, self)
        board.PlacePiece(result)


def MinimaxDecision(board, player):
    placeableSpaces = board.placeableSpaces()

    for space in placeableSpaces:
        newBoard = copy.deepcopy(board)

    

def MaxValue(board, player, CurrentDepth):
    IsEnd, EndResult = board.CheckForWinner()

def MinValue(board, player, CurrentDepth):
    IsEnd, EndResult = board.CheckForWinner()


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
    while(1):
        p1.Move(board)
        IsEnd, EndResult = board.CheckForWinner()
        if IsEnd:
            break
        p2.Move(board)
        IsEnd, EndResult = board.CheckForWinner()
        if IsEnd:
            break
    if EndResult == "Draw":
        print("Match was a draw")
    else:
        print(EndResult +" is the winner")
    return 0

def main():
    board = Board()
    player1 = Player((3,4),2)
    player2 = Player((3,3),4)
    PlayGame(board, player1, player2)

    return 0

if(__name__ == "__main__"):
    main()