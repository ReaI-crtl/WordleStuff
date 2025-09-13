import os
import cmd
import json

from WordleFunctions import compareWords

wordListPath = "wordle-dictionary.json"
dictionary = None

hints = []
data = []

class Cracker(cmd.Cmd):
    intro = 'Have you tried horse?\n'
    prompt = '> '

    def do_showHints(self, args):
        """Show all the input hints"""
        for hint in hints:
            print(hint.hints)

    def do_newHints(self, args):
        """Show all the input hints"""
        newHint = Hint()
        hints.append(newHint)
        newHint.cmdloop()

    def deleteHints(self, args):
        """Show all the input hints"""
        del hints[int(args[0])]
        hints.remove(int(args[0]))

    def deleteHints(self, args):
        """Show all the input hints"""
        del hints[int(args[0])]
        hints.remove(int(args[0]))

    def do_compare(self, args):
            """"Compare two words based on wordle rules"""
            print(compareWords(args[0], args[1]))

    def do_quit(self, args):
        """Exits the dice roller."""
        print("It was probably horse")
        return True

class Hint(cmd.Cmd):
    intro = 'Hint mode enabled.\n'
    prompt = '> '
    
    def __init__(self, completekey = "tab", stdin = None, stdout = None):
        super().__init__(completekey, stdin, stdout)
        self.hints = []

    def do_show(self, args):
        """Insert hint"""
        print(self.hints)

    def do_add(self, args):
        """Insert hint"""
        self.hints.append(args.split(","))
        
    def do_pop(self, args):
        """Pops hint"""
        self.hints.pop()

    def do_exit(self, args):
        """Exits editing hint mode."""
        return True

def init():
    global dictionary
    with open(wordListPath, 'r') as file:
        dictionary = json.load(file)
    dictionary = dictionary["words"]

def main():
    Cracker().cmdloop()
    pass

if __name__ == "__main__":
    init()
    main()