from game import Game
from player import Player
import random
import time

class AimaUtils(object):
    
    @staticmethod
    def argmin(seq, fn):
        """Return an element with lowest fn(seq[i]) score; tie goes to first one.
        >>> argmin(['one', 'to', 'three'], len)
        'to'
        """
        count_negative_inf = 0

        best = seq[0]
        best_score = fn(best)
        if best_score == SeachMethod.INFINITY:
            count_negative_inf +=1

        for x in seq:
            x_score = fn(x)
            if x_score == SeachMethod.INFINITY:
                count_negative_inf +=1
            if x_score < best_score:
                best, best_score = x, x_score
        if len(seq) == count_negative_inf:
            print "You should surrender, all movement are suicide"
        return best




    @staticmethod
    def argmax(seq, fn):
        """Return an element with highest fn(seq[i]) score; tie goes to first one.
        >>> argmax(['one', 'to', 'three'], len)
        'three'
        """

        return AimaUtils.argmin(seq, lambda x: -fn(x))


class SeachMethod(object):
    """ This class have some python AIMA version adapted to thos proyect"""
    
    AIMA_ALPHABETA_SEARCH = "AlphaBeta"
    AIMA_MINMAX_SEARCH = "MinMax"
    INFINITY = 99999999

    def __init__(self, algorith, *optional_params):
        self.__algorimth = algorith
        if optional_params:
            self.__depth = optional_params[0]

        self.__exp_nodes = 0

    def search(self, state, game):
        if self.__algorimth is self.AIMA_ALPHABETA_SEARCH:
            return self.alphabeta_search(state, game, self.__depth)
        elif self.__algorimth is self.AIMA_MINMAX_SEARCH:
            return self.minimax_search(state, game, self.__depth)

    def minimax_search(self, state, game, d):
        """Given a state in a game, calculate the best move by searching forward all the way to the terminal states."""

        player = game.get_player_turn()

        def max_value(st, depth):
            if cutoff_test(st, depth):
                return game.utility(st, player)
            v = -self.INFINITY
            for (a, s) in game.successors(st, player):
                self.__exp_nodes += 1
                v = max(v, min_value(s, depth+1))

            return v

        def min_value(st, depth):
            if cutoff_test(st, depth):
                return game.utility(st, player)
            v = self.INFINITY
            for (a, s) in game.successors(st, game.get_enemy_player()):
                self.__exp_nodes += 1
                v = min(v, max_value(s, depth+1))

            return v

        cutoff_test = lambda sta, depth: depth >= d or game.is_terminal(sta)
        action, state = AimaUtils.argmax(game.successors(state, player), lambda ((a, s)): min_value(s, 0))
        return action

    def alphabeta_search(self, state, game, d):
        """ALPAH BETA SEARCH WITH MAX DEPH"""
        player = game.get_player_turn()

        def max_value(st, alpha, beta, depth):

            if cutoff_test(st, depth):
                ut = game.utility(st, player)
                return ut
            v = -self.INFINITY
            for (a, s) in game.successors(st, player):
                self.__exp_nodes += 1
                v = max(v, min_value(s, alpha, beta, depth+1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(st, alpha, beta, depth):

            if cutoff_test(st, depth):
                ut = game.utility(st, player)
                return ut
            v = self.INFINITY
            for (a, s) in game.successors(st, game.get_enemy_player()):
                self.__exp_nodes += 1
                v = min(v, max_value(s, alpha, beta, depth+1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v
        time_start = time.time()
        cutoff_test = lambda state,depth: depth>d or game.is_terminal(state)
        action, state = AimaUtils.argmax(game.successors(state, player), lambda ((a, s)): min_value(s, -self.INFINITY, self.INFINITY, 0))
        print time.time() - time_start
        return action

    def get_expand_nodes(self):
        return self.__exp_nodes

    def reset_expand_nodes(self):
        self.__exp_nodes = 0
