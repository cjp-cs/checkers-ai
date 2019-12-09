


class MinimaxNode:
    def __init__(self, score, depth, move):
        self.children = []
        self.score = score
        self.depth = depth
        self.move = move

    def add_child(self, child):
        self.children.append(child)