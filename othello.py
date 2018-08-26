from games import (GameState, Game, query_player, random_player,
                   alphabeta_player, play_game, minimax_decision,
                   alphabeta_full_search, alphabeta_search)

class Othello(Game):
    """Juega Othello en un tablero 8 x 8, con Max (primer jugador) jugando con
    las fichas negras. Un estado tiene el jugador al que le toca jugar, una
    utilidad en caché, una lista de movimientos en la forma de una lista de
    posiciones (x, y), y un tablero, en la forma de un diccionario de entradas
    {(x, y): Jugador}, donde Jugador es 'B' para las fichas blancas y 'N' para
    las fichas negras."""

    def __init__(self):
        moves = [(x, y) for x in range(1, 9) for y in range(1, 9)]
        moves.remove((4, 4))
        moves.remove((4, 5))
        moves.remove((5, 4))
        moves.remove((5, 5))
        # siempre inicia 'N'
        self.initial = GameState(to_move='N', utility=0,
                                 board={(4, 4):'B',(4, 5):'N',
                                        (5, 4):'N',(5, 5):'B'}, moves=moves)

    def actions(self, state):
        """Los movimientos legales son las posiciones que se alinean con otra
        pieza del mismo color del jugador que mueve formando una segmento de
        línea recta que contenga al menos una pieza del contrincante."""
        return self.legal_moves(state.moves, state.board, state.to_move)

    def legal_moves(self, smoves, board, player):
        """Determina los movimientos legales de un jugador sobre un tablero"""
        moves = []
        for (x, y) in smoves:
            if self.change_dir(x, y, -1, -1, board, player) \
               or self.change_dir(x, y, -1, 0, board, player) \
               or self.change_dir(x, y, -1, 1, board, player) \
               or self.change_dir(x, y, 0, -1, board, player) \
               or self.change_dir(x, y, 0, 1, board, player) \
               or self.change_dir(x, y, 1, -1, board, player) \
               or self.change_dir(x, y, 1, 0, board, player) \
               or self.change_dir(x, y, 1, 1, board, player):     
                moves.append((x, y))
        return moves

    def change_dir(self, x, y, xd, yd, board, player):
        """Determina una dirección que cambiará el color de al menos una
        pieza del contrincante"""

        def find_player(x, y):
            """Determina si se encuentra otra pieza del jugador en una
            dirección"""
            x += xd
            y += yd
            while (x, y) in board:
                if board[(x, y)] == player:
                    return True
                else:
                    x += xd
                    y += yd
            return False

        x1 = x + xd
        y1 = y + yd
        if (x1, y1) in board and player != board[(x1, y1)]:
            return find_player(x1, y1)
        else:
            return False


    def result(self, state, move):

        def change_player(xd, yd):
            """Cambia las piezas al color del jugador en una dirección"""
            x, y = move
            if self.change_dir(x, y, xd, yd, board, player):
                x += xd
                y += yd
                while (x, y) in board:
                    if board[(x, y)] == player: return
                    else:
                        board[(x, y)] = player
                        x += xd
                        y += yd

        board = state.board.copy()
        moves = list(state.moves)
        player = state.to_move
        if move in self.actions(state):
            board[move] = player
            change_player(-1, -1)
            change_player(-1, 0)
            change_player(-1, 1)
            change_player(0, -1)
            change_player(0, 1)
            change_player(1, -1)
            change_player(1, 0)
            change_player(1, 1)
            moves.remove(move)
            return GameState(to_move=('B' if player == 'N' else 'N'),
                             utility=self.compute_utility(board, move, player),
                             board=board, moves=moves)
        else:
            return GameState(to_move=('B' if player == 'N' else 'N'),
                             utility=self.compute_utility(board, move, player),
                             board=board, moves=moves)
                    
    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        return state.utility if player == 'N' else -state.utility

    def terminal_test(self, state):
        "Un estado es terminal si ninguno de los jugadores tiene acciones"
        laN = len(self.legal_moves(state.moves, state.board, 'N'))
        laB = len(self.legal_moves(state.moves, state.board, 'B'))
        return (laN + laB) == 0

    def display(self, state):
        """despliega el estado del tablero de juego"""
        board = state.board
        print(' ', end=' ')
        for y in range(1, 9): print(y, end=' ')
        print()
        for x in range(1, 9):
            print(x, end=' ')
            for y in range(1, 9):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, move, player):
        """Regresa la diferencia entre el número de piezas de 'N' y
        el número de piezas de 'B'"""
        pieces = list(board.values())
        return pieces.count('N') - pieces.count('B')

    
