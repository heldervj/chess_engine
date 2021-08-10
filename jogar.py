import chess
import time
import random
from IPython.display import display, HTML, clear_output

import logging
logging.basicConfig(filename='logs.txt',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

def cor(jogador):
    return 'White' if jogador == chess.WHITE else 'Black'

def display_board(board, use_svg=True):
    if use_svg:
        return board._repr_svg_()
    else:
        return "<pre>" + str(board) + "</pre>"

def jogador_random_esp(board):
    board = board.copy()

    scores = {}

    moves = list(board.legal_moves)

    for move in moves:
        board_c = board.copy()
        board_c.push_uci(move.uci())
        scores[move] = len(list(board_c.legal_moves))

    # logging.debug(scores)
    scores = dict(filter(lambda elem: elem[1] == min(scores.values()), scores.items()))
    # logging.debug(scores)
    move = random.choice(list(scores.keys()))

    return move.uci()

def jogador_random(board):
    move = random.choice(list(board.legal_moves))
    
    return move.uci()

def joga_random(move, board, tipo_jogador='jogador_random'):
    
    if tipo_jogador=='jogador_random':
        tipo_jogador = jogador_random
    elif tipo_jogador=='jogador_random_esp':
        tipo_jogador = jogador_random_esp

    board = board.copy()
    peca = board.turn
    
    board.push_uci(move.uci())
    
    resultado, _, _ = play_game(tipo_jogador, tipo_jogador, board, visual=None)

    if resultado == peca:
        score_move = 1
    elif resultado == None:
        score_move = 0
    else:
        score_move = -1
    
    return score_move

def joga_random_valores(move, board, tipo_jogador='jogador_random', profundidade=5):
    
    if tipo_jogador=='jogador_random':
        tipo_jogador = jogador_random
    elif tipo_jogador=='jogador_random_esp':
        tipo_jogador = jogador_random_esp

    board = board.copy()
    peca = board.turn
    
    board.push_uci(move.uci())
    
    resultado, _, _ = play_game(tipo_jogador, tipo_jogador, board, visual=None, max_moves=profundidade)

    score_move = analise_tabuleiro(board, peca)
    
    return score_move

def analise_tabuleiro(board, my_color):
    score = random.random()
    ## Check some things about this move:
    # score += 10 if board.is_capture(move) else 0
    # Now check some other things:
    for (piece, value) in [(chess.PAWN, 1), 
                           (chess.BISHOP, 4), 
                           (chess.KING, 0), 
                           (chess.QUEEN, 10), 
                           (chess.KNIGHT, 5),
                           (chess.ROOK, 3)]:
        score += len(board.pieces(piece, my_color)) * value
        score -= len(board.pieces(piece, not my_color)) * value
        # can also check things about the pieces position here
    # Check global things about the board
    winner = not board.turn

    if board.is_checkmate():
        if winner == my_color:
            score += 100
        else:
            score -= 100

    return score

def play_game(player1, player2, board=None, visual="svg", pause=0.1, max_moves=1000):
    """
    playerN1, player2: functions that takes board, return uci move
    visual: "simple" | "svg" | None
    """
    use_svg = (visual == "svg")
    if not board:
        board = chess.Board()

    try:
        while (not board.is_game_over(claim_draw=True)) and (max_moves > 0.0):
            if board.turn == chess.WHITE:
                uci = player1(board)
            else:
                uci = player2(board)
            name = cor(board.turn)
            board.push_uci(uci)
            board_stop = display_board(board, use_svg)
            html = "<b>Move %s %s, Play '%s':</b><br/>%s" % (
                       len(board.move_stack), name, uci, board_stop)
            if visual is not None:
                if visual == "svg":
                    clear_output(wait=True)
                display(HTML(html))
                if visual == "svg":
                    time.sleep(pause)

            max_moves += -.5

    except KeyboardInterrupt:
        msg = "Game interrupted!"
        return (None, msg, board)
    result = None
    if board.is_checkmate():
        msg = "checkmate: " + cor(not board.turn) + " wins!"
        result = not board.turn
    elif board.is_stalemate():
        msg = "draw: stalemate"
    elif board.is_fivefold_repetition():
        msg = "draw: 5-fold repetition"
    elif board.is_insufficient_material():
        msg = "draw: insufficient material"
    elif board.can_claim_draw():
        msg = "draw: claim"
    else:
        msg = "break"
    if visual is not None:
        print(msg)
    return (result, msg, board)

