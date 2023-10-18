import time
from pysat.solvers import Glucose3
from pprint import pprint

# bin 0=>var-1   bin 1=>var1

# example 03b:
# unoptimized:
# duplicates: 7290
# clauses: 15331
#
# skip row and column clause if number from import:
# duplicates: 4419
# clauses: 12019
#
# skip square clause if number from import:
# duplicates: 3690
# clauses: 11191
# time: 0.17943358421325684
#
# example 04a:
# duplicates: 25808
# clauses: 71042
# time: 2.9506070613861084
#
# example 05a:
# duplicates: 114900
# clauses: 377275
# time: 44.6932110786438

# import os
# cwd = os.getcwd()
# print(cwd)
import_str = "./py-satsolver/sudokus/puzzle03a.sudoku"
print(import_str.split('/')[-1])


def is_valid_sudoku(board, k):
    def has_duplicates(arr):
        seen = set()
        return any(num != 0 and (num in seen or seen.add(num)) for num in arr)

    for i in range(k*k):
        row = [board[(i, j)] for j in range(k*k)]
        column = [board[(j, i)] for j in range(k*k)]
        if has_duplicates(row) or has_duplicates(column):
            return False
    for i in range(0, k*k, k):
        for j in range(0, k*k, k):
            box = [board[(i + x, j + y)] for x in range(k) for y in range(k)]
            if has_duplicates(box):
                return False
    return True


def model_to_board(model, n):
    board = dict()
    for index in range(0, len(model), n.bit_length()):
        number_str = ''
        for bit_pos in range(0, n.bit_length()):
            if model[index+bit_pos] > 0:
                number_str += '0'
            else:
                number_str += '1'
        number = int(number_str, 2)
        board[int(index/n.bit_length()/n),
              int(index/n.bit_length() % n)] = number
    return board


def index_value_to_bool_representation(index, value, n):
    number_of_bits_for_all_numbers = n.bit_length()
    offset = number_of_bits_for_all_numbers*index + 1
    bits = []
    value_bits = bin(value)[2:].zfill(number_of_bits_for_all_numbers)
    for row in range(0, number_of_bits_for_all_numbers):
        bit = offset+row
        if value_bits[row] == '0':
            bits.append(bit * -1)
        else:
            bits.append(bit)
    return bits


def pos_to_index(tuple):
    return tuple[0]*n+tuple[1]


def prettyprint(board, k):
    maxlen = len(str(k*k))+1
    minus_multiplicator = int(3)
    for row in range(0, k*k):
        if row % k == 0:
            print("-"*(k*k*minus_multiplicator))
        temp = '|'
        for column in range(0, k*k):
            temp += ' ' * \
                (maxlen - len(str(board[(row, column)]))
                 ) + str(board[(row, column)])
            if column % k == k-1:
                temp += '|'
        print(str(temp))
    print("-"*(k*k*minus_multiplicator))


print('')
start_time = time.time()
with open(import_str, "r") as file:
    content = file.read().split()
if content is None:
    exit()
k, content = int(content[0]), content[1:]
n = k*k
board = dict()
for row in range(0, n):
    for column in range(0, n):
        board[(row, column)] = int(content[pos_to_index((row, column))])

prettyprint(board, k)

clauses = []
# unallowed numbers
numbers_over_n = ((1 << n.bit_length()))-n
for row in range(0, n*n):
    for column in range(1, numbers_over_n):
        variables = index_value_to_bool_representation(row, n+column, n)
        clauses.append(variables)
    variables = index_value_to_bool_representation(row, 0, n)
    clauses.append(variables)

for row in range(0, n):
    for column in range(0, n):
        # already known numbers
        if board[(row, column)] != 0:
            for possible_number in range(1, n+1):
                if possible_number != board[(row, column)]:
                    clauses.append(index_value_to_bool_representation(
                        pos_to_index((row, column)), possible_number, n))
        else:
            # rows and columns
            for other in range(0, n):
                for possible_number in range(1, n+1):
                    # rows
                    if other != column:
                        clause = index_value_to_bool_representation(
                            pos_to_index((row, column)), possible_number, n)
                        clause += index_value_to_bool_representation(
                            pos_to_index((row, other)), possible_number, n)
                        clauses.append(clause)
                    # columns
                    if other != row:
                        clause = index_value_to_bool_representation(
                            pos_to_index((row, column)), possible_number, n)
                        clause += index_value_to_bool_representation(
                            pos_to_index((other, column)), possible_number, n)
                        clauses.append(clause)
            # squares
            square_corner = (int(row/k)*k, int(column/k)*k)
            for other_row in range(square_corner[0], square_corner[0]+k):
                for other_column in range(square_corner[1], square_corner[1]+k):
                    for possible_number in range(1, n+1):
                        if other_row != row and other_column != column:
                            clause = index_value_to_bool_representation(
                                pos_to_index((row, column)), possible_number, n)
                            clause += index_value_to_bool_representation(
                                pos_to_index((other_row, other_column)), possible_number, n)
                            clauses.append(clause)

deduplicate, duplicates = set(), 0
for clause in clauses:
    clause.sort()
    clause2 = tuple(clause)
    if clause2 not in deduplicate:
        deduplicate.add(clause2)
    else:
        duplicates += 1
print("removed " + str(duplicates) + " duplicate clauses")

g = Glucose3()
for clause in deduplicate:
    g.add_clause(clause)
print("used "+str(len(deduplicate))+" clauses")
solved = g.solve()
if not solved:
    print("Failure!!!!!!!!")
    exit()
model = g.get_model()
board_solved = model_to_board(model, n)

prettyprint(board_solved, k)

print("Is this Board valid?: "+str(is_valid_sudoku(board_solved, k)))
end_time = time.time()
print(f"Elapsed time: {end_time-start_time} seconds")
