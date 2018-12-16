#!/usr/bin/env python3

"""
This program entails a person playing against an AI in a game of battleship.

By: ephemerallylong
"""
from random import randint
import string, time

com_array = [[0 for i in range(10)] for j in range(10)]  # 10 elements in row and 10 rows
															# 0 is empty value
comVsPlay_list = [0 for i in range(100)]	# used for know what has and hasn't been hit by com
comVsPlay_array = [[0 for i in range(10)] for j in range(10)]					

play_array = [[0 for i in range(10)] for j in range(10)]
play_name_array = [[0 for i in range(10)] for j in range(10)]
playVsCom_array = [[0 for i in range(10)] for j in range(10)]

array_row_dict = {'j': 9}
array_row_dict.update({letter: int(num) for letter, num in zip(string.ascii_lowercase[0:9], range(9))})
array_row_dict = dict(sorted(array_row_dict.items(), key=lambda x: x[1]))
		# need dict sorted numerically by value for when I use dict.items() method
array_col_dict = {0: 9}
array_col_dict.update({old_num: new_num for old_num, new_num in zip(range(1, 10), range(9))})
array_col_dict = dict(sorted(array_col_dict.items(), key=lambda x: x[1]))
		# need dict sorted numerically by value for when I use dict.items() method

def switchKeyValue(dict_):
	"""Reverses the keys and values s.t. the values become keys and vice versa"""
	return {value: key for key, value in dict_.items()}
	
array_row_dict_reverse = switchKeyValue(array_row_dict)
array_col_dict_reverse = switchKeyValue(array_col_dict)

display_dict = {1: 'S', 0: ' ', -1: 'M', 2: 'X'}
			   # ship , none  , miss   , hit
display_legend = {'M': 'miss', 'X': 'hit'}

difficulty_list = ('cakewalk', 'average', 'methodical') # difficulties of com in game
com_hit_dict = {}
target_list = []


returnValue = lambda x: x # returns itself

activate_sleep_print = False
def sleep_print(*args, end_arg='\n', time_val=.015):
	"""Used to set flow of pace. Prints each argument out iteratively, element by element."""
	if activate_sleep_print:
		for arg in args:
			arg = str(arg)
			for i in arg:
				print(i, end='')
				time.sleep(time_val)
			print(end_arg, end='')
	else:
		print(*args, end=end_arg)

def time_sleep(time_val):
	"""Used instead of sleep_print if needed. Uses time.sleep() function."""
	if not(activate_sleep_print):
		time.sleep(time_val)
	
def deletechars(orig_str, del_chars):
	"""deletes characters from original string"""
	gen = (i for i in orig_str if i not in del_chars)
	new_str = ''
	for i in gen: new_str += i
	return new_str
	
def detectShipOverlap(array, return_list=False):
	"""
	Used in chooseShipLocCom() and chooseShipLocPlay() functions.
	Returns overlap_coord or False depending on whether or not there is any overlap between ships.
	If two ships occupy the same space, the function returns overlap_coord.
	"""
	overlap_coord = []
	for i in range(len(array)):
		for j in range(len(array[0])): # length of all lists in array should be the same
			if array[i][j] == 2:
				overlap_coord.append((i, j)) 
	if overlap_coord == []:
		return False
	else:
		if return_list == True:
			return overlap_coord
		else:
			return True

def convertTupCoord(lst):
	"""Converts the tuples used in game to the coordinates displayed in game"""
	return array_row_dict_reverse[lst[0]].upper() + str(array_col_dict_reverse[lst[1]])
	
def chooseShipLocCom():
	"""
	The com will randomly select where to place its battleships
		Consists of...
			2 len, 3 len, 3 len, 4 len, 5 len
	
	Returns tuple with array of just ships and array of ship names
	"""
	com_array = [[0 for i in range(10)] for j in range(10)]
	com_name_array = [[0 for i in range(10)] for j in range(10)]
	ship_list = [2, 3, 3, 4, 5] # contains all possible ships
	# name_list = [[j for i in range(max(ship_list) + 1)] for j in range(1, len(ship_list) + 1)]
	count = 1
	while len(ship_list) > 0:
		choose_ship = ship_list.pop(randint(0, len(ship_list) - 1))
		while True:
			orientation = randint(0, 1) # 0 is horizontal, 1 is vertical
			position = randint(0, 9 - choose_ship) # dictates where starting element of ship will be
			row_col = randint(0, 9)
			store_loc = []
			if orientation == 0:
				for j in range(choose_ship):
					com_array[row_col][position + j] += 1
					store_loc.append((row_col, position + j))
			else:	# orientation == 1
				for j in range(choose_ship):
					com_array[position + j][row_col] += 1
					store_loc.append((position + j, row_col))
			if detectShipOverlap(com_array) == False:
				for tup in store_loc:
					com_name_array[tup[0]][tup[1]] = returnValue(count)
				break
			else:
				if orientation == 0:
					for j in range(choose_ship):
						com_array[row_col][position + j] -= 1
				else:	# orientation == 1
					for j in range(choose_ship):
						com_array[position + j][row_col] -= 1
		count += 1
	return com_array, com_name_array
	
def displayArray(lst, use_dict=True): #lst must be a list consisting of 10 elements, all elements being list consisting of 10 elements themselves
	"""Displays array of a given list for battleship"""
	timing = 0.005 # seconds
	col_display = list(" " + string.digits[1:] + '0')
	row_display = string.ascii_uppercase[0:10]
	for i in col_display:
		sleep_print(i, end_arg=' ', time_val=timing)
	sleep_print('\n', end_arg='')
	for i in range(len(row_display)):
		sleep_print(row_display[i], end_arg=' ', time_val=timing)
		if use_dict:
			for j in lst[i]: sleep_print(display_dict[j], end_arg=' ', time_val=timing)
		else: 
			for j in lst[i]: 
				if j > 0: sleep_print(j, end_arg=' ', time_val=timing)
				else: sleep_print(' ', end_arg=' ', time_val=timing)
		sleep_print('\n', end_arg='', time_val=timing)
		
def returnArrayInput(input_var):
	"""
	Checks whether input_var is within range (i.e. between A1 and J0).
	Returns tuple of (row, col)
	"""
	input_var = input_var.lower()
	row, col = '', '' # need predefined here or UnboundLocalError
	while len(row) != 1 or len(col) != 1:
		row, col = '', '' # empty string for now so as to be able to detect errors like multiple digits or letters in input_var
		for i in input_var:
			if i in string.ascii_lowercase[0:10]:
				row += i
			elif i in string.digits:
				col += i
		if len(row) != 1 or len(col) != 1:
			input_var = input("\nYour input was invalid. Please make sure you only have one letter and one digit within range of the board. (e.g. 'A7', 'd0')\n").lower()
	col = array_col_dict[int(col)]
	row = array_row_dict[row]
	return row, col

def chooseShipLocPlay():
	"""
	The player will select where to place their battleships
		Consists of...
			2 len, 3 len, 3 len, 4 len, 5 len
	"""
	ship_list = [2, 3, 3, 4, 5]
	count = 1
	while len(ship_list) > 0:
		sleep_print("\nHere are the ship lengths you can choose from:\n%s" % ship_list)
		chooseShip_input = input("Input the number length of the ship you want to place on the board.\n")
		while True:
			while not(isinstance(chooseShip_input, int)):
				try: 
					chooseShip_input = int(chooseShip_input)
				except ValueError:
					chooseShip_input = input("\nInput is not a number. Make your input a number within the following list:\n%s\n" % ship_list)
			if chooseShip_input in ship_list:
				break
			chooseShip_input = input("\nInput is not a valid ship length. Make sure your input is a number in the following list:\n%s\n" % ship_list)
			
		choose_ship = ship_list.pop(ship_list.index(chooseShip_input))

		while True:
			sleep_print("\nHere is what your board looks like right now:\n")
			displayArray(play_name_array, use_dict=False)
			layout_start = input("\nInput the location where you want your ship to start. (e.g. 'A7', 'd0')\n").lower()
			tup_start = returnArrayInput(layout_start)
			layout_end = input("\nInput the location where you want your ship to end. (e.g. 'A7', 'd0')\n").lower()
			tup_end = returnArrayInput(layout_end)
			store_loc = [] # stores tuple of indices, i.e. (row, col) of ship layout. If no ship overlap detected, it is used in play_name_array
			if tup_start[0] > tup_end[0] or tup_start[1] > tup_end[1]:
				buffer_start, buffer_end = returnValue(tup_start), returnValue(tup_end)
				tup_start, tup_end = buffer_end, buffer_start # switches values around so that math works out w/o having to rework the whole thing
			if tup_start[0] == tup_end[0]: # i.e. if horizontal
				if abs(tup_start[1] - tup_end[1]) + 1 != choose_ship:
					sleep_print("\nThe layout you selected occupies {} spaces. It must occupy {} spaces. Try again.\n".format(abs(tup_start[1] - tup_end[1]) + 1, choose_ship))
					time_sleep(2)
					continue
				for i in range(choose_ship):
					play_array[tup_start[0]][tup_start[1] + i] += 1
					store_loc.append((tup_start[0], tup_start[1] + i))
			elif tup_start[1] == tup_end[1]: # i.e. if vertical
				if abs(tup_start[0] - tup_end[0]) + 1 != choose_ship:
					sleep_print("\nThe layout you selected occupies {} spaces. It must occupy {} spaces. Try again.\n".format(abs(tup_start[0] - tup_end[0]) + 1, choose_ship))
					time_sleep(2)
					continue
				for i in range(choose_ship):
					play_array[tup_start[0] + i][tup_start[1]] += 1
					store_loc.append((tup_start[0] + i, tup_start[1]))
			else:
				sleep_print("\nThe start and end of the ship must either be on the same row or column. Try again.\n(In other words it must be vertical or horizontal.)\n")
				time_sleep(2)
				continue
			
			if detectShipOverlap(play_array) == True:
				sleep_print("Ship placement is invalid. An overlap was detected at these points: ", end_arg='', time_val=0.2)
				sleep_print(deletechars(str(convertTupCoord(detectShipOverlap(play_array, return_list=True))), "[]'")) # prints sequence of coords where overlap occurs
				time_sleep(3)
				if tup_start[0] == tup_end[0]: # horizontal
					for i in range(choose_ship):
						play_array[tup_start[0]][tup_start[1] + i] -= 1
				else: # vertical
					for i in range(choose_ship):
						play_array[tup_start[0] + i][tup_start[1]] -= 1
				continue
			else:
				for tup in store_loc:
					play_name_array[tup[0]][tup[1]] = returnValue(count)
				break
		count += 1
	sleep_print("\nHere is what your final board looks like:\n")
	displayArray(play_name_array, use_dict=False)
	time_sleep(3)


def checkIfWin(hit_array, compare_array):
	"""
	Returns True if all ships have been sunk.
	Returns False otherwise.
	"""
	count_hit = 0
	count_ship = 0
	for i in range(len(hit_array)):
		for j, k in zip(hit_array[i], compare_array[i]):
			if j > 0:
				count_hit += 1
			try: 
				if display_legend[display_dict[k]].lower() == 'hit' and j > 0:
					count_ship += 1
			except KeyError:
				pass
	if count_hit == count_ship:
		return True
	else:
		return False
	
def checkIfSink(hit_array, compare_array, ship_hit, is_com=False):
	"""This will check if the ship has sunk"""
	global target_list
	
	count_hit = 0
	count_ship = 0
	for i in range(len(hit_array)):
		for j, k in zip(hit_array[i], compare_array[i]):
			if j == ship_hit:
				count_hit += 1
			try:
				if display_legend[display_dict[k]].lower() == 'hit' and j == ship_hit:
					count_ship += 1
			except KeyError:
				pass
	if count_hit == count_ship:
		sleep_print("\nThe targeted ship has sunk!\n")
		time_sleep(1.5)
		if is_com:
			indices_to_del = sorted([i for i in range(len(target_list)) if target_list[i][1] == ship_hit], reverse=True)
			for i in indices_to_del:
				del target_list[i]
		checkIfWin(hit_array, compare_array)
	
def initTargets(array_index):
	"""
	This function initializes the targets in target_list for com's next turn.
	If two of the same ship is hit, it will change target_list accordingly.
	"""
	ship_id = play_name_array[array_index[0]][array_index[1]]
	com_hit_dict.update({array_index: ship_id})
	adjacency_zip = zip((1,0,-1,0), (0,1,0,-1))
	target_list.extend([((array_index[0]+i, array_index[1]+j), ship_id)\
		for i, j in adjacency_zip if all((array_index[0]+i in array_row_dict.values(), array_index[1]+j in array_col_dict.values()))]) 
			# need to wrap elems in all() in a tuple b/c only takes one arg
	# print(f"target_list before: {target_list}")
	indices_to_del = [i for i in range(len(target_list)) if target_list[i][0] in com_hit_dict.values()\
		or comVsPlay_array[target_list[i][0][0]][target_list[i][0][1]] != 0]
	indices_to_del = sorted(indices_to_del, reverse=True)
	for i in indices_to_del: # want to delete larger indices first b/c they won't get in way of other indices to del
		del target_list[i]
	ship_hit_loc = [i[0] for i in com_hit_dict.items() if i[1] == ship_id]
	# print(f"target_list after: {target_list}")
	# print(f"ship_hit_loc: {ship_hit_loc} is len {len(ship_hit_loc)}")
	if len(ship_hit_loc) >= 2:
		for tup in ship_hit_loc:
			for i in (1, -1):
				try:
					if ship_hit_loc[0][0] == ship_hit_loc[1][0]: # if orientation horizontal
						target_list.remove(((tup[0]+i,tup[1]),ship_id))
					else: #if orientation vertical
						target_list.remove(((tup[0],tup[1]+i),ship_id))
				except ValueError: 
					pass
		# print(f"B/c ship_hit_loc is len {len(ship_hit_loc)}, target_list is now:\n    {target_list}")

methodical_choice = randint(0, 1)
methodical_pref = []
for i in range(len(comVsPlay_list)): # for i in range(100)
	if i < len(comVsPlay_array) or int(list(str(i))[0]) % 2 == 0: # if i < 10
		if (methodical_choice + i) % 2 == 0:
			methodical_pref.append(i)
	else:
		if (methodical_choice + 1 + i) % 2 == 0:
			methodical_pref.append(i)
			
def comTurn(difficulty):
	"""Com tries to hit ship of player"""
	global target_list
	
	empty_spots = [i for i in range(len(comVsPlay_list)) if comVsPlay_list[i] == 0]
	max_randrange = len(empty_spots) - 1
	if difficulty == difficulty_list[0]:
		turn_index = list(str(empty_spots[randint(0, max_randrange)]))
	elif target_list != []:
		turn_index = target_list.pop(randint(0, len(target_list)-1))[0]
		# print(f"target_list after pop: {target_list}")
	elif difficulty == difficulty_list[1]: # average
		turn_index = list(str(empty_spots[randint(0, max_randrange)]))
	elif difficulty == difficulty_list[2]: # methodical
		empty_spots = [i for i in range(len(comVsPlay_list)) if comVsPlay_list[i] == 0 and i in methodical_pref]
		max_randrange = len(empty_spots) - 1
		turn_index = list(str(empty_spots[randint(0, max_randrange)]))
	else:
		raise ValueError("One of 'cakewalk', 'average', or 'methodical' must be set equal to True.")
	# print(turn_index)
	turn_index = [int(i) for i in turn_index]
	turn_index = tuple(turn_index) # a lot of things are made on the condition turn_index is a tuple
	# print(turn_index) # debug
	try: comVsPlay_list[int(str(turn_index[0])+str(turn_index[1]))] = 1
	except IndexError:
		turn_index = (0, turn_index[0])
		comVsPlay_list[int(str(turn_index[0])+str(turn_index[1]))] = 1
	target = convertTupCoord(turn_index)
	sleep_print("\nThe enemy is targeting {}.\n".format(deletechars(target, "'")))
	time_sleep(1.5)
	if play_array[turn_index[0]][turn_index[1]] == 1:	# if enemy's choice is where battleship resides
		comVsPlay_array[turn_index[0]][turn_index[1]] = 2 # 2 means it hit; 1 already means something else
		# play_array[turn_index[0]][turn_index[1]] = -2
		sleep_print("\nEnemy hit your ship!\n")
		time_sleep(1)
		displayArray(comVsPlay_array)
		sleep_print('\n' * 3, end_arg='')
		if difficulty in difficulty_list[1:3]: # if difficulty == 'average' or 'methodical'
			initTargets(turn_index)
		checkIfSink(play_name_array, comVsPlay_array, play_name_array[turn_index[0]][turn_index[1]], is_com=True)
	else:
		sleep_print("\nEnemy missed!\n")
		time_sleep(1)
		comVsPlay_array[turn_index[0]][turn_index[1]] = -1
	sleep_print("\nThe enemy's turn has ended.\n")
	time_sleep(1.5)

def playTurn():
	print_tup = ("This is the board with your ships.", "This is the board where AI has targeted your ships.", "This is the board where you have targeted the AI's ships.")
	for lst, str_elem in zip((play_name_array, comVsPlay_array, playVsCom_array), print_tup):
		sleep_print(str_elem,'\n')
		if lst == play_name_array:
			displayArray(lst, use_dict=False)
		else:
			displayArray(lst)
		if lst != play_name_array:
			sleep_print('')
			for key, value in display_legend.items():
				sleep_print(key,'=',value)
			sleep_print('')
		sleep_print('\n' * 3, end_arg='')  # end='' b/c it's easier to manipulate wanted amt of skipped lines that way
		time_sleep(1.5)
	turn_choice = input("\nInput the location you want to target.\n").lower()
	turn_row, turn_col = returnArrayInput(turn_choice)
	while playVsCom_array[turn_row][turn_col] != 0:
		turn_choice = input("\nYou have selected that spot already. Try again.\n")
		turn_row, turn_col = returnArrayInput(turn_choice)
	time_sleep(1)
	if com_array[turn_row][turn_col] == 1:
		sleep_print("\nYou hit the enemy's ship!\n")
		time_sleep(1.5)
		playVsCom_array[turn_row][turn_col] = 2 # 2 means it hit; 1 already means something else
		checkIfSink(com_name_array, playVsCom_array, com_name_array[turn_row][turn_col])
	else:
		sleep_print("\nYou missed!\n")
		time_sleep(1.5)
		playVsCom_array[turn_row][turn_col] = -1
	
	sleep_print("\nPlayer's turn has ended.\n")
	time_sleep(1.5)

start_input = input("Welcome to Battleship! Press [Enter] to start your game!\n")	

chooseShipLocPlay() # use play_array, play_name_array = chooseShipLocCom() for debugging
com_array, com_name_array = chooseShipLocCom()
sleep_print("\nThe computer has chosen their ship placements.\n")
difficulty_list = ['cakewalk', 'average', 'methodical']
cakewalk, average, methodical = difficulty_list
difficulty = input("\nWhat difficulty do you want the computer to have? [cakewalk/average/methodical]\n").lower()
while difficulty not in difficulty_list:
	difficulty = input("\nThat's not a valid difficulty. Try again. [cakewalk/average/methodical]\n").lower()
start_game_input = ("\nOnce you're ready, press [Enter] to start the game!\n(You will go first.)\n")

dashLine = "-" * 15
turn = 0
while True:
	turn += 1
	sleep_print("\n{0} Turn {1} {0}\n".format(dashLine, turn))
	time_sleep(1)
	game_turn = input("It is your turn. Press [Enter] to continue.")
	playTurn()
	if checkIfWin(com_array, playVsCom_array) == True:
		sleep_print("\nAll the ships have been sunk!\nYou have won!\n")
		time_sleep(4)
		break
	game_turn = input("It is the enemy's turn. Press [Enter] to continue.")
	comTurn(difficulty.lower())
	if checkIfWin(play_array, comVsPlay_array) == True:
		sleep_print("\nAll the ships have been sunk!\nThe enemy has won!\n")
		time_sleep(4)
		break
close_input = input("The program will end. Press [Enter] to do so.")

	
	
