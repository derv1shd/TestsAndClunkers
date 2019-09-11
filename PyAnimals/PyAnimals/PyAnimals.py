#!python3

'''
This is a guess the animal game, where the
conputer asks questions trying to guess at an
animal the user thought of. If the computer
does not know an animal, it asks the user to
provide a question to differentiate from
already known animals and so learn more.
It's implemented by using a binary tree where
the branches are the questions and the leaves
are animals, and it's traversed recursively.
It saves what it learns in a text file.
'''

class Node():
	def __init__(self):
		pass
	def Save(self, file):
		pass
	def Load(self, file):
		line = file.readline()
		line = line.replace("\n", "")\
							 .replace("\r", "")
		if line[:1] == "Q":
			return Question(line[3:], \
											Node.Load(self, file), \
											Node.Load(self, file))
		elif line[:1] == "A":
			return Animal(line[3:])

class Question(Node):
	def __init__(self, question, yesNode, noNode):
		self.question = question
		self.yes = yesNode
		self.no = noNode
	def Save(self, file):
		file.write("Q: " + self.question + "\n")
		self.yes.Save(file)
		self.no.Save(file)
		
class Animal(Node):
	def __init__(self, animalName):
		self.animal = animalName
	def Save(self, file):
		file.write("A: " + self.animal + "\n")
				
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
			if newQuestion[-1:] != "?":
				newQuestion += "?"
			if UserSaidYes("For " + Article(newAnimal) + " " + newAnimal \
			+ " what would you reply to that question?"):
				return Question(newQuestion, Animal(newAnimal), Animal(node.animal))
			else:
				return Question(newQuestion, Animal(node.animal), Animal(newAnimal))
				
def SampleData():
	return Question("Does it live in the sea?", Animal("Dolphin"), Animal("Lion"))
	
def Load():
	# Try to load previous dataset value from file:
	try:
		with open('animals.txt') as f:
			return Node().Load(f)
	except IOError:
		return SampleData()
	except:
		return SampleData()
		
def Save(data):
	# Save the new dataset value to a file:
	with open('animals.txt', 'w') as f:
		data.Save(f)
		
def main():
	animals = Load()
	me = you = 0
	print("PyAnimals!\r\n")
	while True:
		print("Choose an animal and I'll try to guess it.\r\n")
		if Ask(animals):
			me += 1
		else:
			Save(animals)
			you += 1
		print("You: " + str(you) + " Me: " + str(me))
		if UserSaidYes("\r\nWant to play again?"):
			continue
		else:
			break
			
if __name__ == '__main__':
	main()

