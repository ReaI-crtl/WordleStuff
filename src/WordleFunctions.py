"""Functions to apply wordle rules and other stuff"""

def compareWords(guess, answer):
    """Compares two words and returns a list of results
    0 = letter not in word
    1 = letter in word, wrong position
    2 = letter in word, right position"""
    
    result = [0, 0, 0, 0, 0]
    answerLetters = list(answer)
    guessLetters = list(guess)

    # Green
    for i in range(5):
        guessLetter = guessLetters[i]
        answerLetter = answerLetters[i]

        if guessLetter == answerLetter:
            result[i] = 2
            answerLetters[i] = None
            guessLetters[i] = None
    # print(answerLetters)
    # Yellow
    for i in range(5):
        guessLetter = guessLetters[i]

        if guessLetter is None:
            continue

        index = answerLetters.index(guessLetter) if guessLetter in answerLetters else -1
        if index != -1:
            result[i] = 1
            answerLetters[index] = None
            guessLetters[i] = None
    # print(answerLetters)

    return result