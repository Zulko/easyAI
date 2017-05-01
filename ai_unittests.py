#######################################
#
#  TESTING FOR AIs IN EASYAI
#
#  To run tests, simply run this script.
#
#######################################

import unittest

import easyAI
import easyAI.games as examples


class Test_Negamax(unittest.TestCase):

    def test_play_knights_against_self(self):
        ai_algo_K1 = easyAI.Negamax(8)
        ai_algo_K2 = easyAI.Negamax(10)
        game = examples.Knights([easyAI.AI_Player(ai_algo_K1), easyAI.AI_Player(ai_algo_K2)])
        move_list_K1 = []
        move_list_K2 = []
        while not game.is_over():
            move = game.get_move()
            if game.nplayer==1:
                move_list_K1.append(move)
            else:
                move_list_K2.append(move)
            game.play_move(move)
        K1_correct = ['B3', 'C5', 'D7', 'E5', 'F7', 'G5', 'H7', 'F6', 'G8', 'H6', 'G4', 'H2', 'F3', 'G1', 'H3', 'F2', 'E4', 'D6', 'C8', 'B6', 'C4', 'A3', 'B1', 'D2', 'F1', 'G3', 'H5']
        K2_correct = ['G6', 'F8', 'E6', 'D8', 'C6', 'B8', 'A6', 'B4', 'C2', 'D4', 'E2', 'F4', 'G2', 'H4', 'F5', 'G7', 'E8', 'C7', 'D5', 'E3', 'D1', 'C3', 'A4', 'B2', 'D3', 'C1', 'A2']
        self.assertEqual(move_list_K1, K1_correct)
        self.assertEqual(move_list_K2, K2_correct)

    def test_play_awele_against_self(self):
        ai_algo_P1 = easyAI.Negamax(3)
        ai_algo_P2 = easyAI.Negamax(4)
        game = examples.AweleTactical([easyAI.AI_Player(ai_algo_P1), easyAI.AI_Player(ai_algo_P2)])
        move_list_P1 = []
        move_list_P2 = []
        while not game.is_over():
            move = game.get_move()
            if game.nplayer==1:
                move_list_P1.append(move)
            else:
                move_list_P2.append(move)
            game.play_move(move)
        P1_correct = ['c', 'e', 'f', 'f', 'a', 'c', 'e', 'f', 'd', 'b', 'c', 'a', 'f', 'd', 'b', 'e']
        P2_correct = ['i', 'j', 'l', 'h', 'g', 'k', 'j', 'i', 'l', 'h', 'j', 'l', 'k', 'l', 'i', 'g']
        self.assertEqual(move_list_P1, P1_correct)
        self.assertEqual(move_list_P2, P2_correct)


class Test_NonRecursiveNegamax(unittest.TestCase):

    def test_play_knights_against_self(self):
        ai_algo_K1 = easyAI.NonRecursiveNegamax(8)
        ai_algo_K2 = easyAI.NonRecursiveNegamax(10)
        game = examples.Knights([easyAI.AI_Player(ai_algo_K1), easyAI.AI_Player(ai_algo_K2)])
        move_list_K1 = []
        move_list_K2 = []
        while not game.is_over():
            move = game.get_move()
            if game.nplayer==1:
                move_list_K1.append(move)
            else:
                move_list_K2.append(move)
            game.play_move(move)
        K1_correct = ['B3', 'C5', 'D7', 'E5', 'F7', 'G5', 'H7', 'F6', 'G8', 'H6', 'G4', 'H2', 'F3', 'G1', 'H3', 'F2', 'E4', 'D6', 'C8', 'B6', 'C4', 'A3', 'B1', 'D2', 'F1', 'G3', 'H5']
        K2_correct = ['G6', 'F8', 'E6', 'D8', 'C6', 'B8', 'A6', 'B4', 'C2', 'D4', 'E2', 'F4', 'G2', 'H4', 'F5', 'G7', 'E8', 'C7', 'D5', 'E3', 'D1', 'C3', 'A4', 'B2', 'D3', 'C1', 'A2']
        self.assertEqual(move_list_K1, K1_correct)
        self.assertEqual(move_list_K2, K2_correct)

    def test_play_awele_against_self(self):
        ai_algo_P1 = easyAI.NonRecursiveNegamax(3)
        ai_algo_P2 = easyAI.NonRecursiveNegamax(4)
        game = examples.AweleTactical([easyAI.AI_Player(ai_algo_P1), easyAI.AI_Player(ai_algo_P2)])
        move_list_P1 = []
        move_list_P2 = []
        while not game.is_over():
            move = game.get_move()
            if game.nplayer==1:
                move_list_P1.append(move)
            else:
                move_list_P2.append(move)
            game.play_move(move)
        P1_correct = ['c', 'e', 'f', 'f', 'a', 'c', 'e', 'f', 'd', 'b', 'c', 'a', 'f', 'd', 'b', 'e']
        P2_correct = ['i', 'j', 'l', 'h', 'g', 'k', 'j', 'i', 'l', 'h', 'j', 'l', 'k', 'l', 'i', 'g']
        self.assertEqual(move_list_P1, P1_correct)
        self.assertEqual(move_list_P2, P2_correct)


class Test_SSS(unittest.TestCase):

    def test_play_knights_against_self(self):
        ai_algo_K1 = easyAI.SSS(8)
        ai_algo_K2 = easyAI.SSS(10)
        game = examples.Knights([easyAI.AI_Player(ai_algo_K1), easyAI.AI_Player(ai_algo_K2)])
        move_list_K1 = []
        move_list_K2 = []
        while not game.is_over():
            move = game.get_move()
            if game.nplayer==1:
                move_list_K1.append(move)
            else:
                move_list_K2.append(move)
            game.play_move(move)
        K1_correct = ['B3', 'C5', 'D7', 'E5', 'F7', 'G5', 'H7', 'F6', 'G8', 'H6', 'G4', 'H2', 'F3', 'G1', 'H3', 'F2', 'E4', 'D6', 'C8', 'B6', 'C4', 'A3', 'B1', 'D2', 'F1', 'G3', 'H5']
        K2_correct = ['G6', 'F8', 'E6', 'D8', 'C6', 'B8', 'A6', 'B4', 'C2', 'D4', 'E2', 'F4', 'G2', 'H4', 'F5', 'G7', 'E8', 'C7', 'D5', 'E3', 'D1', 'C3', 'A4', 'B2', 'D3', 'C1', 'A2']
        self.assertEqual(move_list_K1, K1_correct)
        self.assertEqual(move_list_K2, K2_correct)

class Test_DUAL(unittest.TestCase):

    def test_play_knights_against_self(self):
        ai_algo_K1 = easyAI.DUAL(8)
        ai_algo_K2 = easyAI.DUAL(10)
        game = examples.Knights([easyAI.AI_Player(ai_algo_K1), easyAI.AI_Player(ai_algo_K2)])
        move_list_K1 = []
        move_list_K2 = []
        while not game.is_over():
            move = game.get_move()
            if game.nplayer==1:
                move_list_K1.append(move)
            else:
                move_list_K2.append(move)
            game.play_move(move)
        K1_correct = ['B3', 'C5', 'D7', 'E5', 'F7', 'G5', 'H7', 'F6', 'G8', 'H6', 'G4', 'H2', 'F3', 'G1', 'H3', 'F2', 'E4', 'D6', 'C8', 'B6', 'C4', 'A3', 'B1', 'D2', 'F1', 'G3', 'H5']
        K2_correct = ['G6', 'F8', 'E6', 'D8', 'C6', 'B8', 'A6', 'B4', 'C2', 'D4', 'E2', 'F4', 'G2', 'H4', 'F5', 'G7', 'E8', 'C7', 'D5', 'E3', 'D1', 'C3', 'A4', 'B2', 'D3', 'C1', 'A2']
        self.assertEqual(move_list_K1, K1_correct)
        self.assertEqual(move_list_K2, K2_correct)


if __name__ == "__main__":
    unittest.main(exit=False)
