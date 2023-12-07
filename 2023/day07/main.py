#!/usr/bin/env python3
import re
import sys
from collections import defaultdict


values = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2
}

class Hand:
    def __init__(self, line):
        self.cards = line[:5]
        self.bid = int(line[6:])
        self.counts = defaultdict(int)

        for card in self.cards:
            self.counts[card] += 1

    def __lt__(self, hand):
        # We have less different cards, hand will always be stronger
        if len(self.counts) < len(hand.counts):
            return False

        elif len(self.counts) > len(hand.counts):
            return True

        # When amount of different cards is the same, the one with the biggest count always wins
        elif len(self.counts) == len(hand.counts):
            similarA = max(self.counts.values())
            similarB = max(hand.counts.values())

            if similarA > similarB:
                return False

            elif similarB > similarA:
                return True

        i = 0
        while i < 5:
            if values[self.cards[i]] != values[hand.cards[i]]:
                return values[self.cards[i]] < values[hand.cards[i]]

            i += 1

        return False

    def __eq__(self, hand):
        return self.cards == hand.cards

    def __gt__(self, hand):
        return not self.__lt__(hand) and not self.__eq__(hand)


class Game:
    def __init__(self):
        self.hands = []

    def parse(self, line):
        self.hands.append(Hand(line))

    def compute(self):
        i = 1
        total = 0

        for hand in sorted(self.hands):
            print("Rank %d: %s" % (i, hand.cards))
            total += i * hand.bid
            i += 1

        print("")
        return total

    def apply_joker_rule(self):
        values["J"] = 1

        for hand in self.hands:
            if "J" in hand.counts:
                jokers = hand.counts.pop("J")

                max_count = 0
                max_card = None
                for card in hand.counts:
                    if hand.counts[card] > max_count:
                        max_count = hand.counts[card]
                        max_card = card

                hand.counts[max_card] += jokers

with open(sys.argv[1], "r") as f:
    game = Game()

    for line in f:
        game.parse(line)

    print(game.compute())
    print("")
    game.apply_joker_rule()
    print(game.compute())
