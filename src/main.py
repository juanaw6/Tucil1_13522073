import time

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

        buffer_length = int(lines[0].strip())
        matrix_size = tuple(map(int, lines[1].strip().split()))
        matrix = []
        
        for i in range(2, 2 + matrix_size[0]):
            row = lines[i].strip().split()
            matrix.append(row)
        
        num_sequence = int(lines[2 + matrix_size[0]])
        
        start = 3 + matrix_size[0]
        sequences = []
        temp = []
        isSequence = True
        for i in range(start, start + (num_sequence * 2)):
            if isSequence :
                temp.append(" ".join(lines[i].strip().split()))
                isSequence = False
            else :
                temp.append(int(lines[i].strip()))
                sequences.append(temp)
                temp = []
                isSequence = True

        return buffer_length, matrix_size, matrix, num_sequence, sequences

def dfs(matrix, row, col, path, path_coordinate, n, visited, can_horizontal, sequences , reward_info):
    if n < 0:
        return
    if visited[row][col]:
        return

    visited[row][col] = True
    path.append(matrix[row][col])
    path_coordinate.append([row + 1, col + 1])

    if n > 0:
        if can_horizontal:
            new_col = col - 1
            while new_col >= 0 and not visited[row][new_col]:
                dfs(matrix, row, new_col, path, path_coordinate, n - 1, visited, False, sequences, reward_info)
                new_col -= 1

            new_col = col + 1
            while new_col < len(matrix[0]) and not visited[row][new_col]:
                dfs(matrix, row, new_col, path, path_coordinate, n - 1, visited, False, sequences, reward_info) 
                new_col += 1
        else:
            new_row = row - 1
            while new_row >= 0 and not visited[new_row][col]:
                dfs(matrix, new_row, col, path, path_coordinate, n - 1, visited, True, sequences, reward_info)
                new_row -= 1

            new_row = row + 1
            while new_row < len(matrix) and not visited[new_row][col]:
                dfs(matrix, new_row, col, path, path_coordinate, n - 1, visited, True, sequences, reward_info)
                new_row += 1

    current_path_str = " ".join(path)
    reward = sum(seq[1] for seq in sequences if seq[0] in current_path_str)
    
    if reward > reward_info['max_reward']:
        reward_info['max_reward'] = reward
        reward_info['max_reward_seq'] = current_path_str
        reward_info['moves'] = path_coordinate.copy()

    visited[row][col] = False
    path.pop()
    path_coordinate.pop()

def find_sequences(matrix, n, sequences):
    visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    reward_info = {'max_reward': 0, 'max_reward_seq': '', 'moves': []}

    for col in range(len(matrix[0])):
        dfs(matrix, 0, col, [], [], n, visited, False, sequences, reward_info)
    
    return reward_info

file_path = 'src/input.txt'
buffer_length, matrix_size, matrix, sequence_lengths, sequences = read_file(file_path)

print("Buffer Length:", buffer_length)
print("Matrix Size:", matrix_size)
print("Matrix:")
for row in matrix:
    print(row)
print("Sequence Lengths:", sequence_lengths)
for row in sequences :
    print(row)

start = time.time()
result = find_sequences(matrix, 6, sequences)
print(result)
duration = round((time.time() - start)*1000)

