import copy

import players as p
from score import (score_hand, score_count)
from card import Deck

import random
import math


class MonteCarloPlayer(p.Player):
    def ask_for_discards(self):
        # Does a simple check of every combination and discards the cards with the lowest total point value.
        # Uses a randomly drawn card to simulate the card flip when counting points.
        cards_to_discard = []
        max_points = 0
        deck = Deck()
        random_card = list(deck.draw(1))
        for card1 in self.hand:
            discarded_cards = [card1]
            self.hand.remove(card1)
            for card2 in self.hand:
                discarded_cards.append(card2)
                self.hand.remove(card2)
                score = score_hand(self.hand, random_card[0])
                if score > max_points:
                    max_points = score
                    cards_to_discard.clear()
                    cards_to_discard.extend([card1, card2])
                discarded_cards.remove(card2)
                self.hand.append(card2)
            discarded_cards.remove(card1)
            self.hand.append(card1)
        return cards_to_discard

    def ask_for_play(self, plays):
        deck = Deck()
        # get the number of cards to simulate for the opponent hand
        num_to_draw = 4 - len(plays) + (4 - len(self.hand))
        # Implements Monte-Carlo tree search to find the best card to play
        initial_game_state = CribbageGameState(player_hand=self.hand, opponent_hand=list(deck.draw(num_to_draw)),
                                               player_score=0, opponent_score=0, plays=plays)
        state = monte_carlo_tree_search(initial_game_state, 100)
        card_to_play = [item for item in self.hand if item not in state.player_hand]
        return card_to_play[0]


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0


def select(node):
    while node.children:
        node = max(node.children, key=lambda child: uct_score(child))
    return node


def expand(node):
    legal_actions = get_legal_moves(node.state)
    if legal_actions:
        for action in legal_actions:
            new_state = perform_move(node.state, action)
            new_node = Node(new_state, parent=node)
            node.children.append(new_node)
        return random.choice(node.children)
    else:
        return node


def uct_score(node):
    if node.visits == 0:
        return float('inf')
    exploitation = node.score / node.visits
    exploration = math.sqrt(math.log(node.parent.visits) / node.visits)
    return exploitation + C * exploration


class CribbageGameState:
    def __init__(self, player_hand, opponent_hand, player_score, opponent_score, plays):
        self.player_hand = player_hand
        self.opponent_hand = opponent_hand
        self.player_score = player_score
        self.opponent_score = opponent_score
        self.plays = plays


def get_legal_moves(state):
    # Returns the available cards to play
    return state.player_hand


def perform_move(state, move):
    # Move is the card played by the current player
    # Update the state accordingly, considering the opponent's turn
    new_state = copy.deepcopy(state)
    new_state.player_hand.remove(move)
    new_state.plays.append(move)
    new_state.player_score += score_count(new_state.plays)  # Update the player's score based on the played card

    # Simulate the opponent's move (randomly selecting a card)
    if new_state.opponent_hand:
        opponent_move = random.choice(new_state.opponent_hand)
        new_state.opponent_hand.remove(opponent_move)
        new_state.plays.append(opponent_move)
        new_state.opponent_score += score_count(new_state.plays)  # Update the opponent's score
    return new_state


def is_terminal(state):
    # Check if the player has any cards left to play
    return not state.player_hand


def simulate_game(state):
    # Simulate a random playthrough of the game from the given state
    while not is_terminal(state):
        legal_moves = get_legal_moves(state)
        move = random.choice(legal_moves)
        state = perform_move(state, move)
    return state.player_score


def backpropagate(node, score):
    # Update the tree nodes along the path with the simulation result
    while node:
        node.visits += 1
        node.score += score
        node = node.parent


def monte_carlo_tree_search(root_state, iterations):
    root = Node(state=root_state)

    for _ in range(iterations):
        selected_node = select(root)
        expanded_node = expand(selected_node)
        simulation_result = simulate_game(expanded_node.state)
        backpropagate(expanded_node, simulation_result)

    best_child = max(root.children, key=lambda child: child.visits)
    return best_child.state


# Constants
C = 1.4  # Exploration constant
