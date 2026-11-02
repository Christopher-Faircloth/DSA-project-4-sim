from __future__ import annotations
from consts import Board, Color, Edge, NUM_NODES


class GameBoard:
    """
    Game board manager class. Encapsulates behaviors concerning the state of the board.
    """

    def __init__(self):
        """
        Initialize `board` as the adjacency matrix for the starting board.
        Use `Color.NONE` for edges that do not exist, and `Color.UNCOLORED` for the other edges.
        """
        self.board = []
        # it is a set board size of 6x6 array "None" is the diagonal from 0,0 to 5,5
        for i in range(NUM_NODES):
            row = []
            for j in range(NUM_NODES):
                if i == j :
                    row.append(Color.NONE)
                else:
                    row.append(Color.UNCOLORED)

            self.board.append(row)

        #raise NotImplementedError

    def color_edge(self, edge: Edge, color: Color) -> None:
        """
        Update `board` to reflect coloring the given edge.
        """
        #given the edge and the color just call board at that
        # edge point and update the color
        row, col = edge[0], edge[1]
        self.board[row][col] = color
        self.board[col][row] = color


        return None
        raise NotImplementedError

    def get_winner(self) -> Color | None:
        """
        Return the color of the player that has won (Color.P1 or Color.P2).
        If the game is still in progress (no one has won yet), return None.
        """
        #maybe use a helper to check if there is any triangles on the board
        #if so return the color of the triangle, if false return none
        #a triangle happens when there is a closed loop with length 3
        # i only need to find the first one, I should also only have to check
        # half the board (top right triangle or bottom left triangle).

        # method, there must be two of the same colred edges in a row for there to potentially be a triangle,
        # if there is two or more check for the pairs of those edges if that point is the same color, if there
        # is than that is a triangle, ie is (0,1) and (0,2) are the same color then if (1,2) is also that color
        # than there is a triangle, for more than just two eges the same color you must check every combination
        # for a triangle.

        p2Edges = []
        p1Edges = []

        #loop through only top right corner
        for row in range(6):
            #avoids diagonals
            for col in range(row+1, 6):
                boardColor = self.board[row][col]
                #if they are colored add them to their list
                if boardColor == Color.P1:
                    p1Edges.append(col)
                if boardColor == Color.P2:
                    p2Edges.append(col)
            #potential triangle from this row
            if len(p1Edges) >=2:
                for i in range(len(p1Edges)):
                    for j in range(i+1, len(p1Edges)):
                        col1 = p1Edges[i]
                        col2 = p1Edges[j]
                        if self.board[col1][col2] == Color.P1:
                            # Triangle detected!!!
                            return Color.P2

            #potential triangle from this row
            if len(p2Edges) >=2:
                for i in range(len(p2Edges)):
                    for j in range(i+1, len(p2Edges)):
                        col1 = p2Edges[i]
                        col2 = p2Edges[j]
                        if self.board[col1][col2] == Color.P2:
                            # Triangle detected!!!
                            return Color.P1

            p2Edges = []
            p1Edges = []

        return None
        raise NotImplementedError

    def __str__(self):
        """
        Formats the board as a string. Provided for your convenience while debugging.
        """
        string = ""
        for row in self.board:
            for item in row:
                string += "{edge:<10}".format(edge=item.name)
            string += "\n"
        return string
