def partOne(input: str):
    """
    A, X - Rock
    B, Y - Paper
    C, Z - Scissors
    """

    # This dict contains the outcome for each possible scenario
    outcomes = {
        'A': {
            'X': 'draw',
            'Y': 'win',
            'Z': 'loss'
        },
        'B': {
            'X': 'loss',
            'Y': 'draw',
            'Z': 'win'
        },
        'C': {
            'X': 'win',
            'Y': 'loss',
            'Z': 'draw'
        }
    }

    # This dict contains the scores for each game result, as well as each shape selected
    scores = {
        'loss': 0,
        'draw': 3,
        'win': 6,
        'X': 1,
        'Y': 2,
        'Z': 3
    }

    array = input.splitlines()

    final_score = 0

    for item in array:
        you, me = item.split(' ')

        result = outcomes[you][me]

        # The total score consists of the score for the result, as well as
        # the score of the shape played
        score = scores[result] + scores[me]

        final_score += score

    print(final_score)


def partTwo(input: str):
    """
    A - Rock
    B - Paper
    C - Scissors
    X - Loss
    Y - Draw
    Z - Win
    """

    # This dict contains which shape to play for each scenario
    outcomes = {
        'A': {
            'X': 'C',
            'Y': 'A',
            'Z': 'B'
        },
        'B': {
            'X': 'A',
            'Y': 'B',
            'Z': 'C'
        },
        'C': {
            'X': 'B',
            'Y': 'C',
            'Z': 'A'
        }
    }

    # This dict contains the scores for each game result, as well as each shape selected
    scores = {
        'X': 0,
        'Y': 3,
        'Z': 6,
        'A': 1,
        'B': 2,
        'C': 3
    }

    array = input.splitlines()

    final_score = 0

    for item in array:
        you, result = item.split(' ')

        me = outcomes[you][result]

        score = scores[result] + scores[me]

        final_score += score

    print(final_score)


with open('input.txt') as f:
    input = f.read()

partOne(input)
partTwo(input)
