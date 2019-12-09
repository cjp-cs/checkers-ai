from random import randint
from BoardClasses import Move
from BoardClasses import Board
#from our_stuff.MinimaxNode import MinimaxNode
#The following part should be completed by students.
#Students can modify anything except the class name and existing functions and varibles.

tree_depth = 4

class MinimaxNode:
    def __init__(self, score, depth, move):
        self.children = []
        self.score = score
        self.depth = depth
        self.move = move

    def add_child(self, child):
        self.children.append(child)


class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2

    def get_score (self, board, our_color, opp_color):
        score = 0
        for r in range(len(board.board)):
            for c in range(len(board.board[r])):
                checker = board.board[r][c]
                base_score = 0
                if checker.color == our_color:
                    base_score += 1
                elif checker.color == opp_color:
                    base_score -= 1

                if checker.is_king:
                    base_score *= 7 + len(board.board)
                elif self.color == 1:
                    base_score *= 5 + r
                else:
                    base_score *= 5 + len(board.board) - r
                score += base_score
                #score += base_score * (2 if checker.is_king else 1)
        return score

    def generate_tree (self, node, curr_board, color, our_color, opp_color):
        if node.depth >= tree_depth:
            return
        moves = curr_board.get_all_possible_moves(color)
        for move_group in moves:
            for move in move_group:
                curr_board.make_move(move, color)
                score = self.get_score(curr_board, our_color, opp_color)
                child = MinimaxNode(score, node.depth+1, move)
                node.add_child(child)
                self.generate_tree(child, curr_board, (color%2)+1, our_color, opp_color)
                curr_board.undo()

    def get_move(self,move):
        # move is the opponent's move (e.g. '(2,1)-(3,2)')
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        our_color = 'B' if self.color == 1 else 'W'
        opp_color = 'B' if self.color == 2 else 'W'

        #print('score:', self.get_score(self.board, our_color, opp_color))

        root_node = MinimaxNode(self.get_score(self.board, our_color, opp_color), 0, None)
        self.generate_tree(root_node, self.board, self.color, our_color, opp_color)

        # def print_tree (root):
        #     print('depth:', root.depth)
        #     print('score:', root.score)
        #     print('move:', root.move, '\n')
        #     for kid in root.children:
        #         print_tree(kid)
        #print_tree(root_node)


        def minimax (curr_node, target_depth, is_max_turn):
            if len(curr_node.children) == 0 or curr_node.depth == target_depth:
                return (curr_node.score, curr_node)
            elif is_max_turn:
                result = max([minimax(node, target_depth, not is_max_turn) for node in curr_node.children], key=lambda y:y[0])
                if curr_node.depth == 0:
                    return result
                return (result[0], curr_node)
            else:
                result = min([minimax(node, target_depth, not is_max_turn) for node in curr_node.children], key=lambda y:y[0])
                return (result[0], curr_node)

        best_score, best_node = minimax(root_node, tree_depth, True)
        move = best_node.move
        #move = self.board.get_all_possible_moves(self.color)[0][0]

        #print(best_score, best_node.move)



        # vvv
        #moves = self.board.get_all_possible_moves(self.color)
        #index = randint(0,len(moves)-1)
        #inner_index =  randint(0,len(moves[index])-1)
        #move = moves[index][inner_index]
        # ^^^ this is StudentAI's move (e.g. '(2,1)-(3,2)')

        self.board.make_move(move,self.color)
        return move
