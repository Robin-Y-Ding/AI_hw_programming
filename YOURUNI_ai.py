#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: YOUR NAME AND UNI 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

state_value_dict = dict()

def compute_utility(board, color):
    """
    Return the utility of the given board state
    (represented as a tuple of tuples) from the perspective
    of the player "color" (1 for dark, 2 for light)
    """
    dark, light = get_score(board)
    if color == 1:
        return dark - light
    elif color == 2:
        return light - dark


############ MINIMAX ###############################

def minimax_min_node(board, color):
    v= float("inf")
    opp_color = 3 - color
    if board in state_value_dict.keys():
        v = state_value_dict[board]
    else:
        moves = []
        moves = get_possible_moves(board, opp_color)
        if moves == []:
            v = compute_utility(board, color)
        else:
            for move in moves:
                suc_board = play_move(board, opp_color, move[0], move[1])
                v = min(v, minimax_max_node(suc_board, color))
        state_value_dict[board] = v
    return v


def minimax_max_node(board, color):
    v = float("-inf")
    if board in state_value_dict.keys():
        v = state_value_dict[board]
    else:
        moves = []
        moves = get_possible_moves(board, color)
        if moves == []:
            v = compute_utility(board, color)
        else:
            for move in moves:
                suc_board = play_move(board, color, move[0], move[1])
                v = max(v, minimax_min_node(suc_board, color))
        state_value_dict[board] = v
    return v

    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """
    next_move_i = 0
    next_move_j = 0
    max_value = float("-inf")
    mvs = get_possible_moves(board, color)
    for mv in mvs:
        suc_board = play_move(board, color, mv[0], mv[1])
        value = minimax_min_node(suc_board, color)
        if max_value < value:
            next_move_i = mv[0]
            next_move_j = mv[1]
            max_value = value
    # state_value_dict[board] = max_value
    return next_move_i, next_move_j




############ ALPHA-BETA PRUNING #####################

def alphabeta_min_node(board, color, alpha, beta, level, limit):
    v = float("inf")
    level += 1
    if board in state_value_dict.keys():
        v = state_value_dict[board]
    else:
        opp_color = 3 - color
        moves = []
        h_mvs = dict()
        moves = get_possible_moves(board, opp_color)
        if moves == [] or level == limit:
            v = compute_utility(board, color)
        else:
            for move in moves:
                suc_board = play_move(board, opp_color, move[0], move[1])
                utility = compute_utility(suc_board, color)
                h_mvs[move] = utility
            heuristic = sorted(h_mvs.items(), key=lambda kv: kv[1])
            for i in range(0, len(heuristic)):
                new_suc_board = play_move(board, opp_color, heuristic[i][0][0], heuristic[i][0][1])
                v = min(v, alphabeta_max_node(new_suc_board, color, alpha, beta, level, limit))
                if v <= alpha:
                    return v
                beta = min(beta, v)
        state_value_dict[board] = v
    return v
"""
def alphabeta_min_node(board, color, alpha, beta):
    v = float("inf")
    if board in state_value_dict.keys():
        v = state_value_dict[board]
    else:
        opp_color = 3 - color
        moves = []
        h_mvs = dict()
        moves = get_possible_moves(board, opp_color)
        if moves == []:
            v = compute_utility(board, color)
        else:
            for move in moves:
                suc_board = play_move(board, opp_color, move[0], move[1])
                utility = compute_utility(suc_board, color)
                h_mvs[move] = utility
            heuristic = sorted(h_mvs.items(), key=lambda kv: kv[1])
            for i in range(0, len(heuristic)):
                new_suc_board = play_move(board, opp_color, heuristic[i][0][0], heuristic[i][0][1])
                v = min(v, alphabeta_max_node(new_suc_board, color, alpha, beta))
                if v <= alpha:
                    return v
                beta = min(beta, v)
        state_value_dict[board] = v
    return v
"""


def alphabeta_max_node(board, color, alpha, beta, level, limit):
    v = float("-inf")
    level += 1
    if board in state_value_dict.keys():
        v = state_value_dict[board]
    else:
        moves = []
        h_mvs = dict()
        moves = get_possible_moves(board, color)
        if moves == [] or level == limit:
            v = compute_utility(board, color)
        else:
            for move in moves:
                suc_board = play_move(board, color, move[0], move[1])
                utility = compute_utility(suc_board, color)
                h_mvs[move] = utility
            heuristic = sorted(h_mvs.items(), key=lambda kv: kv[1], reverse=True)
            for i in range(0, len(heuristic)):
                new_suc_board = play_move(board, color, heuristic[i][0][0], heuristic[i][0][1])
                v = max(v, alphabeta_min_node(new_suc_board, color, alpha, beta, level, limit))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
        state_value_dict[board] = v
    return v
"""
def alphabeta_max_node(board, color, alpha, beta):
    v = float("-inf")
    if board in state_value_dict.keys():
        v = state_value_dict[board]
    else:
        moves = []
        h_mvs = dict()
        moves = get_possible_moves(board, color)
        if moves == []:
            v = compute_utility(board, color)
        else:
            for move in moves:
                suc_board = play_move(board, color, move[0], move[1])
                utility = compute_utility(suc_board, color)
                h_mvs[move] = utility
            heuristic = sorted(h_mvs.items(), key=lambda kv: kv[1], reverse=True)
            for i in range(0, len(heuristic)):
                new_suc_board = play_move(board, color, heuristic[i][0][0], heuristic[i][0][1])
                v = max(v, alphabeta_min_node(new_suc_board, color, alpha, beta))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
        state_value_dict[board] = v
    return v
"""

def select_move_alphabeta(board, color):
    next_move_i = 0
    next_move_j = 0
    max_value = float("-inf")
    mvs = get_possible_moves(board, color)
    alpha = float("-inf")
    beta = float("inf")
    level = 0
    limit = 6
    for mv in mvs:
        suc_board = play_move(board, color, mv[0], mv[1])
        value = alphabeta_min_node(suc_board, color, alpha, beta, level, limit)
        if max_value < value:
            next_move_i = mv[0]
            next_move_j = mv[1]
            max_value = value
    # state_value_dict[board] = max_value

    return next_move_i, next_move_j


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()

    """  board = tuple()
    board = ((0, 2, 0, 0),
            (0, 2, 1, 1),
            (0, 2, 1, 0),
            (0, 0, 0, 0))
    alphabeta_max_node(board, 1, float("-inf"), float("inf"))"""
"""x = {(1,2): 2, (3,4): 4, (4,5): 3, (2,8): 1, (0,6): 0}
    sorted_by_value = sorted(x.items(), key=lambda kv: kv[1])
    print (sorted_by_value)
    print (sorted_by_value[0][0][0])"""



