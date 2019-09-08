#!python3

'''
'''

import sys, json

animals = []

def StartUp():
    return Question("Does it live in the sea?", Animal("Dolphin"), Animal("Lion"))

class Node():
    def __init__(self):
        pass

class Question(Node):
    def __init__(self, question, yesNode, noNode):
        self.question = question
        self.yes = yesNode
        self.no = noNode

class Animal(Node):
    def __init__(self, animalName):
        self.animal = animalName

def UserSaidYes(text):
    while True:
        response = input(text + " (y/n) ")
        if response in ["Y", "y"]:
            return True
        elif response in ["N", "n"]:
            return False
        else:
            print("Sorry, didn't get that")

def Article(noun):
    if noun[:1].lower() in ["a", "e", "i", "o", "u"]:
        return "an"
    else:
        return "a"

def Ask(node):
    global animals
    if type(node) == Question: # branch node
        if UserSaidYes(node.question):
            result = Ask(node.yes)
            if type(result) is Question:
                node.yes = result
                return False
            else:
                return result
        else:
            result = Ask(node.no)
            if type(result) is Question:
                node.no = result
                return False
            else:
                return result

    else: # it's an animal - leaf node
        if UserSaidYes("Is the animal you thought " + Article(node.animal) + " " + node.animal):
            print("I knew it! I win!\r\n")
            return True
        else:
            print("Oh, you win!\r\n")
            newAnimal = input("What was the animal you thought? ")
            newQuestion = input("Can you tell me a question to differenciate between " \
                + Article(newAnimal) + " " + newAnimal \
                + " and " + Article(node.animal) + " " + node.animal + "? ")
            if UserSaidYes("For " + Article(newAnimal) + " " + newAnimal \
                + " what would you reply to that question?"):
                return Question(newQuestion, Animal(newAnimal), Animal(node.animal))
            else:
                return Question(newQuestion, Animal(node.animal), Animal(newAnimal))

# Try to load previous dataset value from file:
try:
	with open('animals.json') as f:
		animals = json.load(f)
except IOError:
	animals = StartUp()
except:
	animals = StartUp()

def main():
    global animals
    print("PyAnimals: choose an animal and don't tell me, I'll try to guess it.\r\n")
    while True:
        Ask(animals)
        if UserSaidYes("\r\nWant to play again?"):
            continue
        else:
            break

if __name__ == '__main__':
	main()
	

