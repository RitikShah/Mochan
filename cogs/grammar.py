import random
import re

class Grammar:
	def __init__(self, raw: str):
		self.grammar = {}

		spaces = re.compile('\\s+')
		bars = re.compile('\\|')

		# Ensure every line has ':=='
		for line in [ele.split('::=') for ele in raw.split('\n')]:
			assert(len(line) == 2)
			assert(line[0] not in self.grammar)

			self.grammar[line[0]] = [spaces.split(ele) for ele in bars.split(line[1].strip())]

	def generate(self, symbol, times=None):
		if times is not None:
			assert(times > 0 and symbol in self.grammar)
			return [self.generate(symbol) for i in range(times)]

		else:
			if symbol not in self.grammar:
				return symbol
			else:
				output = [self.generate(symb) for symb in random.choice(self.grammar[symbol])]
				return ' '.join(output)

# main testing method
if __name__ == '__main__':
	stuff = ''

	with open('grammar/' + input('Filename: ') + '.txt', 'r') as file:
		print(Grammar(file.read()).generate('<s>', int(input('How many times: '))))
	