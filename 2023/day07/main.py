import heapq
import os


def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    def get_hand_type(hand: str) -> int:
        """
        This function is used to get the hand type for a particular hand.
        The function returns an integer, from 1 (High card) up to 7 (Five of
        a kind).
        """

        # `cards` is a dict where each key corresponds to a card in the hand, and
        # each value is the numbeer of times that that card appears in the hand
        cards: dict[str, int] = {}

        for card in hand:
            cards[card] = cards.get(card, 0) + 1

        # `values` is a list corresponding to the frequency of the cards in the hand,
        # with the highest value first
        values = sorted(cards.values(), reverse=True)

        # Five of a kind - [5]
        if values[0] == 5:
            return 7

        # Four of a kind - [4, 1]
        if values[0] == 4:
            return 6

        if values[0] == 3:
            # Full house - [3, 2]
            if values[1] == 2:
                return 5

            # Three of a kind - [3, 1, 1]
            return 4

        if values[0] == 2:
            # Two pair - [2, 2, 1]
            if len(values) == 3:
                return 3

            # One pair - [2, 1, 1, 1]
            return 2

        # High card - [1, 1, 1, 1, 1]
        return 1

    def get_hand_strength(hand: str) -> str:
        """
        This function replaces the non-numerical cards in the hand with new letters, so that
        ASCII ordering can be used when directly comparing strings. e.g.:

                   ('V') ('W') ('X') ('Y') ('Z')

        ... < '9' < 'T' < 'J' < 'Q' < 'K' < 'A'
        """

        return (
            hand.replace("T", "V")
            .replace("J", "W")
            .replace("Q", "X")
            .replace("K", "Y")
            .replace("A", "Z")
        )

    # We use a heap to order the hands. The hands are first ordered by their type from the
    # get_hand_type() function. If the types are equal, they will then be ordered by their
    # strength after being transformed by the get_hand_strength() function. This function
    # allows the hands to be compared directly as strings. The bid is also added to the heap.
    # This is not used for sorting, but to help in calculating the total winnings later.
    heap: list[tuple[int, str, int]] = []

    for line in array:
        hand, bid = line.split(" ")
        hand_type = get_hand_type(hand)
        hand_strength = get_hand_strength(hand)

        # Push the tuple onto the heap
        heapq.heappush(heap, (hand_type, hand_strength, int(bid)))

    result = 0

    rank = 1

    # Loop until the heap is empty
    while heap:
        # Popping an item off the heap gives us the smallest (weakest) hand
        # We only need the bid value
        bid = heapq.heappop(heap)[2]
        result += rank * bid

        # Increment the rank
        rank += 1

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    def get_hand_type(hand: str) -> int:
        """
        This function is similar to Part 1, with added logic for the joker cards.
        We calculate which card (other than 'J') appears the most often, and we
        change all 'J' cards to that card.

        If there are no joker cards, or there are only joker cards ('JJJJJ'), then
        cards do not need to be changed, and the logic is identical to Part 1.
        """

        cards: dict[str, int] = {}

        for card in hand:
            cards[card] = cards.get(card, 0) + 1

        # We only need to change cards if there is at least one joker, but not
        # Five of a kind ('JJJJJ')
        if "J" in cards and cards["J"] != 5:
            # `top` will be the card that appears the most number of times
            # exluding 'J'
            top = None

            # `maximum` will be the number of times that the top card appears
            maximum = 0

            for card, count in cards.items():
                # Exclude counting 'J' cards
                if card != "J" and count > maximum:
                    top = card
                    maximum = count

            # At this point, `top` should never be `None`, however it has been added
            # to fix typing errors
            assert top is not None

            # Add the count of jokers to the count of the top card
            cards[top] += cards["J"]

            # Delete the jokers from the hand, as they are now the top card
            del cards["J"]

        values = sorted(cards.values(), reverse=True)

        if values[0] == 5:
            return 7
        if values[0] == 4:
            return 6
        if values[0] == 3:
            if values[1] == 2:
                return 5
            return 4
        if values[0] == 2:
            if len(values) == 3:
                return 3
            return 2
        return 1

    def get_hand_strength(hand: str) -> str:
        """
        This function is the same as in Part 1, however the value of 'J' is now
        '1', to accommodate the new ordering. e.g.:

        ('1')                         ('V')

         'J' < '2' < '3' < ... < '9' < 'T' < ...
        """

        return (
            hand.replace("T", "V")
            .replace("J", "1")
            .replace("Q", "X")
            .replace("K", "Y")
            .replace("A", "Z")
        )

    heap: list[tuple[int, str, int]] = []

    for line in array:
        hand, bid = line.split(" ")
        hand_type = get_hand_type(hand)
        hand_strength = get_hand_strength(hand)

        heapq.heappush(heap, (hand_type, hand_strength, int(bid)))

    result = 0

    rank = 1

    while heap:
        bid = heapq.heappop(heap)[2]
        result += rank * bid
        rank += 1

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
