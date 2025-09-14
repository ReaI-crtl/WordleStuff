import os
import cmd
import json

import random

from WordleFunctions import compareWords

dictionaryPath = "unsorted-dictionary.json"
cachedHintsPath = "cached-hints"
dictionary = None
currentDictionary = None

testedHints = ["00000", "22222"]

hardcodedHints = [
    '00010',
    '02210',
    '10101',
    '02101',
    '10200',
    '02000',
    '10100',
    '02100',
    '02211',
    '00011',
    '00020',
    '22220',
    '00200',
    '00120',
    '00100',
    '02020',
    '02022',
]

class Cracker(cmd.Cmd):
    intro = 'Have you tried horse?\n'
    prompt = '> '

    def do_show(self, args):
        """Show all the input hints"""
        print(currentDictionary)
        print(len(currentDictionary))

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

        global dictionary

        bufferDictionary = dictionary.copy()
        validWords = []
        invalidWords = []
        
        count = 0
        
        for testWord in dictionary:
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

    def do_quit(self, args):
        """Exits the dice roller."""
        print("It was probably horse")
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