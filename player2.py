from __future__ import annotations
from consts import Board, Color, Edge, NUM_NODES


class Player2:
    """
    Implements a winning strategy for the second player in a game of Sim
    """

    @staticmethod
    def get_move(board: Board) -> Edge:
        """
        Return a possible move for the second player (blue) that follows the optimal strategy laid out in the handout,
        given the input board state. If multiple moves are viable, this method can return any of them.
        """
        #this function uses the others to get the move to be made
        miniBoard = Player2.get_miniboard(board)

        p2_moves = Player2.get_allowed_moves(Color.P2, miniBoard)

        # if there is only one move
        if len(p2_moves) == 1:
            return p2_moves[0]

        #find the most used move in the p2 move set
        p2_sets = Player2.get_maximal_allowed_sets(Color.P2, miniBoard)

        p2_counts = {move: 0 for move in p2_moves}

        for move_set in p2_sets:
            for move in move_set:
                p2_counts[move] += 1

        highest_frequency = max(p2_counts.values())

        potential_moves = []
        for move in p2_moves:
            if p2_counts[move] == highest_frequency:
                potential_moves.append(move)

        #only one highest move
        if len(potential_moves) == 1:
            return potential_moves[0]

        #check against p1 moves
        p1_sets = Player2.get_maximal_allowed_sets(Color.P1, miniBoard)
        #counts moves only in potential moves for p2
        p1_counts = {move: 0 for move in potential_moves}

        for move_set in p1_sets:
            for move in move_set:
                if move in p1_counts:
                    p1_counts[move] += 1

        highest_frequency = max(p1_counts.values())
        #checks for p2 move that overlaps the most with p1 moves
        for move in potential_moves:
            if p1_counts[move] == highest_frequency:
                return move

        raise NotImplementedError

    #checks if a move is valid, ie if it makes a triangle then it is not valid
    #assumes current edge is uncolored
    @staticmethod
    def is_valid_move(move: Edge, board: Board, color: Color) -> bool:
        col1 = move[0]
        col2 = move[1]

        for i in range(NUM_NODES):
            if i != col1 and i != col2:
                #checks for triangle
                if(board[i][col1] == color and
                        board[i][col2] == color):
                    return False
        #no triangles found
        return True
    @staticmethod
    def get_miniboard(board: Board) -> Board | None:
        """
        Return a miniboard from the input board state. If there are multiple miniboards, this method can return any of them.
        """
        # itterate through the top right of the board,
        # mini board must have a valid p2 move
        #finds used nodes
        used_nodes = set()
        for i in range(NUM_NODES):
            for j in range(i+1, NUM_NODES):
                if board[i][j] != Color.UNCOLORED and board[i][j] != Color.NONE:
                    #adds both nodes to used set
                    used_nodes.add(i)
                    used_nodes.add(j)

        #creates current mini board out of only used nodes
        miniBoard = [row.copy() for row in board]

        for i in range(NUM_NODES):
            if i not in used_nodes:
                #make all edges None ie not in the board
                for j in range(NUM_NODES):
                    miniBoard[i][j] = Color.NONE
                    miniBoard[j][i] = Color.NONE

        #check if board has a valid move
        moves = Player2.get_allowed_moves(Color.P2, miniBoard)
        if moves:
            return miniBoard

        # add back unused node
        for i in range(NUM_NODES):
            if i not in used_nodes:
                for j in used_nodes:
                    miniBoard[i][j] = board[i][j]
                    miniBoard[j][i] = board[j][i]

                return miniBoard

        return None
        raise RuntimeError("get miniboard failed")

    @staticmethod
    def get_maximal_allowed_sets(player: Color, board: Board) -> set[frozenset[Edge]]:
        """
        Return a set of all distinct maximal allowed sets for the given player over the input board state.
        If player is Color.P1, find all maximal p1-allowed sets; if player is Color.P2, find all maximal p2-allowed sets.
        """
        # could use a helper function that determines if a move is valid or not
        # use a queue and add all of the posible moves. for each move in the queue
        # loop through and check if that move can be combined with any other move
        # in the original move list. If it can then add the two moves to the end of
        # the queue. This process checks every combination of valid moves.
        moves = Player2.get_allowed_moves(player, board)

        # Keep track of combinations already checked
        checked_sets = set()
        # store valid combinations
        move_set = set()
        #queue to check possible moves
        move_queue = []
        for move in moves:
            move_queue.append([move])
        while move_queue:
            #current moves are already validated
            current_move = move_queue.pop(0)
            current_set = frozenset(current_move)

            if current_set in checked_sets:
                continue
            checked_sets.add(current_set)
            # reset board
            temp_board = [row.copy() for row in board]

            #theroetically make the move(s)
            for move in current_move:
                row, col = move[0], move[1]
                temp_board[row][col] = player
                temp_board[col][row] = player

            move_set.add(current_set)

            #this tests if the combination of current move and another move is valid
            for move in moves:
                if move not in current_move:
                    if Player2.is_valid_move(move, temp_board, player):
                        new_move_set = current_move.copy()
                        new_move_set.append(move)
                        #adds valid combination to move set
                        move_queue.append(new_move_set)

        if not move_set:
            return set()

        largest_size = max(len(current_set) for current_set in move_set)

        maximal_sets = set()
        for current_set in move_set:
            if len(current_set) == largest_size:
                maximal_sets.add(current_set)

        return maximal_sets

        raise NotImplementedError

    @staticmethod
    def get_allowed_moves(player: Color, board: Board) -> list[Edge]:
        """
        Return a list of all distinct valid moves for the given player over the input board state.
        """
        # use the helper on every position
        valid_moves = []
        for i in range(NUM_NODES):
            for j in range(i+1, NUM_NODES):
                if(board[i][j] == Color.UNCOLORED):
                    move = (i, j)
                    if Player2.is_valid_move(move, board, player):
                        valid_moves.append(move)
        return valid_moves
        raise NotImplementedError


