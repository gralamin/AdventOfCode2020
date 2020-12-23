import time
from collections import deque


class Deck:
    def __init__(self, input_str):
        lines = input_str.split("\n")
        self.player = int(lines[0].split(" ")[-1][:-1])
        self.deck = deque([int(x) for x in lines[1:] if x.strip() != ""])
        self.original_deck = self.deck.copy()

    def play_card(self):
        return self.deck.popleft()

    def add_card_to_bottom(self, card):
        self.deck.append(card)

    def reset(self):
        self.deck = self.original_deck.copy()

    def __repr__(self):
        return f"Player {self.player}'s deck: {', '.join([str(x) for x in self.deck])}"

    @property
    def is_empty(self):
        return len(self.deck) == 0

    @property
    def score(self):
        value = len(self.deck)
        score = 0
        for card in self.deck:
            score += value * card
            value -= 1
        return score


class GameEngine:
    def __init__(self, player_decks):
        self.decks = player_decks
        self.round = 1

    def reset(self):
        for deck in self.decks:
            deck.reset()
        self.round = 1

    def play_round(self, debug=False):
        if debug:
            print(f"-- Round {self.round} --")
            for deck in self.decks:
                print(deck)
        # Each player plays a card
        cards = [deck.play_card() for deck in self.decks]
        if debug:
            for card, deck in zip(cards, self.decks):
                print(f"Player {deck.player} plays: {card}")
        # determine winner of round
        top_card = -1
        top_deck = None
        for card, deck in zip(cards, self.decks):
            if card > top_card:
                top_card = card
                top_deck = deck
        if debug:
            print(f"Player {top_deck.player} wins the round!")
        top_deck.add_card_to_bottom(top_card)
        for card in cards:
            if card != top_card:
                top_deck.add_card_to_bottom(card)
        self.round += 1

    @property
    def is_game_over(self):
        return any(deck.is_empty for deck in self.decks)

    def get_score(self, debug=False):
        if debug:
            print("== Post-game results ==")
            for deck in self.decks:
                print(deck)
        return max(deck.score for deck in self.decks)


def part1(decks, debug=False):
    engine = GameEngine(decks)
    while not engine.is_game_over:
        engine.play_round(debug=debug)
    return engine.get_score(debug=debug)


def get_input():
    with open("input", "r") as f:
        cur_player = []
        for x in f:
            a = x.strip()
            if a == "":
                yield Deck("\n".join(cur_player))
                cur_player = []
            else:
                cur_player.append(a)
        if cur_player:
            yield Deck("\n".join(cur_player))


if __name__ == "__main__":
    decks = list(get_input())
    start = time.perf_counter()
    print("Part1:", part1(decks))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
    print("\n")
