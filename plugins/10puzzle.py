# -*- coding: utf-8 -*-
import itertools, re, random
import math

TARGET = 'REPLY'

def ten_puzzle(inputs):
	action = ['+', '-', '*', '/']
	function = ['', 'math.sqrt']

	i = 0
	found = 0
	result = []
	for inp in list(itertools.permutations(inputs)):
		for x in action:
			for y in action:
				for z in action:
					for f1 in function:
						for f2 in function:
							for f3 in function:
								for f4 in function:
									expression = '%s( float(%s) ) %s %s( float(%s) ) %s %s( float(%s) ) %s %s( float(%s) )' % (f1, inp[0], x, f2, inp[1], y, f3, inp[2], z, f4, inp[3])
									try:
										evaled = eval(expression)
										i += 1
									except (ValueError, ZeroDivisionError):
										continue
									if evaled == 10:
										expression = re.sub('float\((\d+)?\)', r'\1', expression)
										expression = re.sub('math.sqrt\( (\d+)? \)', ur'√\1', expression)
										expression = expression.replace('( ', '')
										expression = expression.replace(' )', '')
										result.append(expression)
										found += 1
	text = u'total %s ways (found %s patterns)' % (i, found)
	if len(result) > 0:
		text = text + '\nFor example: %s, %s, %s' % (random.choice(result), random.choice(result), random.choice(result))
	else:
		text = text + '\nThere is no pattern.'
	return text

def do(stream):
	if '10puzzle' in stream['text']:
		inputs = stream['text'].split(' ')[2:]
		text = u'@%s %s' % (stream['user']['screen_name'], ten_puzzle(inputs))
		result = {"text": text, "in_reply_to": stream['id']}
		return result
