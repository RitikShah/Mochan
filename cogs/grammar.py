import random
import json
import re

def create(filename: str, raw: str):
	grammar = {}

	spaces = re.compile('\\s+')
	bars = re.compile('\\|')

	# Ensure every line has ':=='
	for line in [ele.split('::=') for ele in raw.split('\n')]:
		assert(len(line) == 2)
		assert(line[0] not in grammar)

		grammar[line[0]] = [spaces.split(ele) for ele in bars.split(line[1].strip())]

	return grammar

def generate(sym, grammar):
	def _gen(symbol):
		if symbol not in grammar:
			return symbol
		else:
			output = [_gen(symb) for symb in random.choice(grammar[symbol])]
			return ' '.join(output)

	return _gen(sym)

# main testing method
if __name__ == '__main__':
	stuff = ''
	filename = input('Filename: ')
	with open('grammar/' + filename + '.txt', 'r') as file:
		grammar = create(filename, file.read())

		with open(filename + '.json', 'w') as outfile:
			json.dump(grammar, outfile)

		print(generate('<s>', grammar))
	