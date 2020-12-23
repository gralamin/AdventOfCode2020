import time
from collections import deque


class Deck:
    def __init__(self, input_str, copy_data=None):
        if copy_data:
            self.player = copy_data["player"]
            self.deck = copy_data["deck"]
        else:
            lines = input_str.split("\n")
            self.player = int(lines[0].split(" ")[-1][:-1])
            self.deck = deque([int(x) for x in lines[1:] if x.strip() != ""])
        self.original_deck = self.deck.copy()
        self.has_won = False

    def play_card(self):
        return self.deck.popleft()

    def add_card_to_bottom(self, card):
        self.deck.append(card)

    def reset(self):
        self.deck = self.original_deck.copy()

    def __hash__(self):
        return hash((self.player, sum(self.deck)))

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

    def __eq__(self, other):
        return self.player == other.player and self.deck == other.deck

    def count(self):
        return len(self.deck)

    def copy(self, next_cards=None):
        cards_copy = self.deck.copy()
        if next_cards is None:
            return Deck("", copy_data={"player": self.player, "deck": cards_copy})
        num_cards_to_pop = len(self.deck) - next_cards
        while num_cards_to_pop > 0:
            cards_copy.pop()
            num_cards_to_pop -= 1
        return Deck("", copy_data={"player": self.player, "deck": cards_copy})


class GameEngine:
    def __init__(self, player_decks):
        self.decks = player_decks
        self.round = 1

    def reset(self):
        for deck in self.decks:
            deck.reset()
        self.round = 1

    def play_round(self, debug=False):
        self._round_stats(debug)
        # Each player plays a card
        cards = self._play_cards(debug)
        # determine winner of round
        self._non_recurse_win(cards, debug)
        self.round += 1

    def _round_stats(self, debug):
        if debug:
            print(f"-- Round {self.round} --")
            for deck in self.decks:
                print(deck)

    def _play_cards(self, debug):
        cards = [deck.play_card() for deck in self.decks]
        if debug:
            for card, deck in zip(cards, self.decks):
                print(f"Player {deck.player} plays: {card}")
        return cards

    def _non_recurse_win(self, cards, debug):
        top_card = -1
        top_deck = None
        for card, deck in zip(cards, self.decks):
            if card > top_card:
                top_card = card
                top_deck = deck
        if debug:
            self._print_non_recurse_win(top_deck)
        top_deck.add_card_to_bottom(top_card)
        for card in cards:
            if card != top_card:
                top_deck.add_card_to_bottom(card)

    def _print_non_recurse_win(self, deck):
        return print(f"Player {deck.player} wins the round!")

    @property
    def is_game_over(self):
        return any(deck.is_empty for deck in self.decks)

    def get_score(self, debug=False):
        if debug:
            print("== Post-game results ==")
            for deck in self.decks:
                print(deck)
        return max(deck.score for deck in self.decks)


class RecursiveGameEngine(GameEngine):
    def __init__(self, player_decks, game_number):
        super().__init__(player_decks)
        self.states = set()
        self.game = game_number
        self.subgames_so_far = 0

    def reset(self):
        super().reset()
        self.states = set()
        self.subgames_so_far = 0

    def play_round(self, debug=False):
        self._round_stats(debug)
        result = self._check_for_state_win(debug)
        if result:
            return

        cards = self._play_cards(debug)

        # Check if we need to recurse
        values = [deck.count() for deck in self.decks]
        for card, value in zip(cards, values):
            if value < card:
                self._non_recurse_win(cards, debug)
                break
        else:
            self._recurse(cards, debug)

        self.round += 1

    def _round_stats(self, debug):
        if debug:
            if not self.states:
                print(f"=== Game {self.game} ===")
            print(f"-- Round {self.round} (Game {self.game}) --")
            for deck in self.decks:
                print(deck)

    def _check_for_state_win(self, debug):
        state = tuple(deck.copy() for deck in self.decks)
        # Check if we have seen this state before
        for previous_state in self.states:
            if previous_state == state:
                if debug:
                    print(f"Player 1 by state before {previous_state} == {state}")

                winner = [deck for deck in self.decks if deck.player == 1][0]
                winner.has_won = True
                return True
        # Add this state to previous states
        self.states.add(state)
        return False

    def _recurse(self, cards, debug):
        recurse_decks = [deck.copy(card) for deck, card in zip(self.decks, cards)]
        self.subgames_so_far += 1
        new_game_engine = RecursiveGameEngine(
            recurse_decks, self.game + self.subgames_so_far
        )
        if debug:
            print("Playing a sub-game to determine the winner...")
        while not new_game_engine.is_game_over:
            new_game_engine.play_round()
        winning_deck = new_game_engine.get_winning_deck(debug=debug)
        self.subgames_so_far += new_game_engine.subgames_so_far

        if debug:
            print("")
            print(f"...anyway, back to game {self.game}.")
            p = winning_deck.player
            print(f"Player {p} wins round {self.round} of game {self.game}!")

        card_order_to_add = deque()
        non_copy_winner = None
        for card, deck in zip(cards, self.decks):
            if deck.player == winning_deck.player:
                card_order_to_add.appendleft(card)
                non_copy_winner = deck
            else:
                card_order_to_add.append(card)
        for card in card_order_to_add:
            non_copy_winner.add_card_to_bottom(card)

    def _print_non_recurse_win(self, deck):
        return print(
            f"Player {deck.player} wins round {self.round} of game {self.game}!"
        )

    @property
    def is_game_over(self):
        return any(deck.is_empty or deck.has_won for deck in self.decks)

    def get_winning_deck(self, debug=False):
        for deck in self.decks:
            if not deck.is_empty or deck.has_won:
                if debug:
                    print(f"The winner of game {self.game} is player {deck.player}!")
                return deck


def part1(decks, debug=False):
    engine = GameEngine(decks)
    while not engine.is_game_over:
        engine.play_round(debug=debug)
    return engine.get_score(debug=debug)


def part2(decks, debug=False):
    engine = RecursiveGameEngine(decks, 1)
    while not engine.is_game_over:
        engine.play_round(debug=debug)
    # Get the winning deck just for debug messages
    engine.get_winning_deck(debug=debug)
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
    p1decks = [deck.copy() for deck in decks]
    p2decks = [deck.copy() for deck in decks]
    start = time.perf_counter()
    print("Part1:", part1(p1decks))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
    print("\n")

    start = time.perf_counter()
    print("Part2:", part2(p2decks))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
