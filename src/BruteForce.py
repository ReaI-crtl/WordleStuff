import os
import cmd
import json

import random

from WordleFunctions import compareWords

# dictionaryPath = "unsorted-dictionary.json"
# cachedHintsPath = "cached-hints"

dictionaryPath = "wordle-dictionary.json"
cachedHintsPath = "temp/cached-hints-1"

dictionary = None
currentDictionary = None

firstHints = [
    '20000',
    '01020',
    '20000',
    '00001',
    '02200',
    '20001',
    '00010',
    '11111',
]
dictionaryScores = {}

commonStarting = ["raise", "adieu", "gamer", "crane", 'audio']

testedHints = ["00000", "22222"]

hardcodedHints = [
    '20000',
    '20010',

    '01020',
    '10220',
    '00222',
    '02222',

    '20000',
    '00200',
    '21220',
    '20222',

    '00001',
    '01000',
    '00001',
    '10000',
    '00100',
    '01022',

    '02200',
    '01000',
    '22201',

    '20001',
    '11000',
    '12200',

    '11111',

    '00010',
    '11000',
    '10101',
    '21001',
    '21100',
]

class Cracker(cmd.Cmd):
    intro = 'Have you tried horse?\n'
    prompt = '> '

    def do_show(self, args):
        """Show all potential words"""
        amount = len(currentDictionary)
        if amount <= 300:
            print(currentDictionary)
        print(amount)
    
    def do_random(self, args):
        """Random set"""
        global currentDictionary

        scores = {}
        totalScore = 0

        for word in currentDictionary:
            scores[word] = 0

        for _ in range(100):
            testWord = random.choice(dictionary)
            for word in currentDictionary:
                hint = formatHint(compareWords(testWord, word))
                if word == "ready ":
                    print(testWord, hint)
                if hint in testedHints:
                    scores[word] += 1
        
        # print(scores)

        for score in scores:
            totalScore += scores[score]
        
        bufferDictionary = currentDictionary.copy()
        threshold = int((totalScore/len(currentDictionary)) * 0.5)

        print(threshold)
        for word in scores:
            score = scores[word]
            if score <= threshold:
                bufferDictionary.remove(word)
        
        currentDictionary = bufferDictionary

    def do_compare(self, args):
            """"Compare two words based on wordle rules"""
            args = args.split(" ")
            print(compareWords(args[0], args[1]))
            print(formatHint(compareWords(args[0], args[1])))

    def do_reset(self, args):
            """"Reset dictionary"""
            global currentDictionary
            global dictionary
            currentDictionary = dictionary.copy()
            print("Dictionary resetted")

    def do_scoring(self, args):
        """"Reset dictionary"""
        Scoring().cmdloop()

    def do_deduction(self, args):
        """"Reset dictionary"""
        Deduction().cmdloop()

    def do_quit(self, args):
        """Exits the dice roller."""
        print("It was probably horse")
        return True

class Deduction(cmd.Cmd):
    intro = 'Deduction mode enabled\n'
    prompt = '> '

    def do_step(self, args):
        """Show all the input hints"""
        hint = args

        if hint is None:
            print("Enter a valid hint")
            return

        # Check if hint is reused
        if hint in testedHints:
            print("Hint already tested")
            return
        testedHints.append(hint)

        global currentDictionary

        bufferDictionary = currentDictionary.copy()
        validWords = []
        invalidWords = []
        
        count = 0
        
        for testWord in currentDictionary:
            with open(f"{cachedHintsPath}/{testWord}.json", 'r') as file:
                data = json.load(file)
                valid = True
                
                if data.get(hint) == None:

                    if testWord == "noisy":
                        print(f"Test failed:{testWord} on hint {hint}")
                    invalidWords.append(testWord)
                    bufferDictionary.remove(testWord)
                    valid = False

                if valid:
                    # print(f"Valid word: {testWord}")
                    validWords.append(testWord)
            
            count += 1
            if count % 100 == 0:
                print(f"Processed {count}/{len(dictionary)} words")
        
        print(f"Valid words: {len(validWords)}")
        print(f"Invalid words: {len(invalidWords)}")
        print(f"Reduced dictionary size from {len(dictionary)} to {len(bufferDictionary)}")
        dictionary = bufferDictionary

    def do_start(self, args):
        """Show all the input hints"""
        hints = []

        # Filter hints to prevent duplicates
        for hint in hardcodedHints:
            if hint in hints:
                continue
            hints.append(hint)
        testedHints.append(hint)

        global currentDictionary

        bufferDictionary = dictionary.copy()
        validWords = []
        invalidWords = []
        
        count = 0
        
        for testWord in dictionary:
            with open(f"{cachedHintsPath}/{testWord}.json", 'r') as file:
                data = json.load(file)
                valid = True

                for hint in hints:
                    if data.get(hint) == None:
                        invalidWords.append(testWord)
                        bufferDictionary.remove(testWord)
                        valid = False
                        break
                
                if not valid:
                    validWords.append(testWord)

            
            count += 1
            if count % 100 == 0:
                print(f"Processed {count}/{len(dictionary)} words")
        
        print(f"Valid words: {len(validWords)}")
        print(f"Invalid words: {len(invalidWords)}")
        print(f"Reduced dictionary size from {len(currentDictionary)} to {len(bufferDictionary)}")
        currentDictionary = bufferDictionary
    
    def do_quit(self, args):
        """Exits the dice roller."""
        print("Stopping..")
        return True

class Scoring(cmd.Cmd):
    intro = 'Scoring mode enabled\n'
    prompt = '> '

    def do_score(self, args):
        """Show all the input hints"""
        global currentDictionary
        global dictionaryScores
        global firstHints
        
        for word in currentDictionary:
            dictionaryScores[word] = 0

        for word in currentDictionary:
            for common in commonStarting:
                resultHint = formatHint(compareWords(common, word))
                comparison = resultHint in firstHints
                print(resultHint)
                
                if comparison:
                    print(f"{word}: {common}")
                    dictionaryScores[word] += 1
        
        print(dictionaryScores)

        sortedScores = {}
        for word in dictionaryScores:
            score = dictionaryScores[word]
            scores = sortedScores.get(score)
            if scores == None:
                sortedScores[score] = []
            sortedScores[score].append(word)

        for score in sorted(sortedScores, reverse=True):
            print(score, sortedScores[score])
    
    def do_frequency(self, args):
        """Show all the input hints"""
        global currentDictionary
        scores = [{}, {}, {}, {}, {}]

        for word in currentDictionary:
            for i in range(5):
                letter = word[i]
                score = scores[i]

                letterScore = score.get(letter)
                if letterScore == None:
                    score[letter] = 0
                score[letter] += 1
        
        # Sort
        for i in range(5):
            score = scores[i]
            print(f"Position {i+1}")
            for letter in sorted(score, key=lambda x : score[x], reverse=True):
                print(letter, score[letter])
        

    def do_add(self, args):
        """Add hint into firstHints"""
        global firstHints

        firstHints.append(args)
    
    def do_quit(self, args):
        """Exits the dice roller."""
        print("Stopping..")
        return True


def formatHint(hint):
    return "".join(map(str, hint))

def init():
    global dictionary

    # Load the dictionary
    with open(dictionaryPath, 'r') as file:
        dictionary = json.load(file)
    dictionary = dictionary["words"]

    size = len(dictionary)
    print(f"Total words in selected dictionary: {size}")

    for word in dictionary:
        stored = {}
        for other in dictionary:
            hint = formatHint(compareWords(other, word))
            if stored.get(hint):
                stored[hint].append(other)
            else:
                stored[hint] = [other]
        with open(f"{cachedHintsPath}/{word}.json", "w+") as file:
            json.dump(stored, file, indent=4)
    
def load():
    global dictionary
    global currentDictionary

    # Load the dictionary
    with open(dictionaryPath, 'r') as file:
        dictionary = json.load(file)
    dictionary = dictionary["words"]

    size = len(dictionary)
    print(f"Total words in selected dictionary: {size}")

    currentDictionary = dictionary.copy()

def main():
    Cracker().cmdloop()
    pass

if __name__ == "__main__":
    # init()
    load()
    main()