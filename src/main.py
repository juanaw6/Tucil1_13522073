import time
from utils import read_file, user_input, save_file

def search_path(matrix, row, col, path, path_coordinate, n, visited, can_horizontal, sequences , reward_info):
    if n < 0:
        return
    if visited[row][col]:
        return

    visited[row][col] = True
    path.append(matrix[row][col])
    path_coordinate.append([col + 1, row + 1])

    if n > 0:
        if can_horizontal:
            new_col = col - 1
            while new_col >= 0 and not visited[row][new_col]:
                search_path(matrix, row, new_col, path, path_coordinate, n - 1, visited, False, sequences, reward_info)
                new_col -= 1

            new_col = col + 1
            while new_col < len(matrix[0]) and not visited[row][new_col]:
                search_path(matrix, row, new_col, path, path_coordinate, n - 1, visited, False, sequences, reward_info) 
                new_col += 1
        else:
            new_row = row - 1
            while new_row >= 0 and not visited[new_row][col]:
                search_path(matrix, new_row, col, path, path_coordinate, n - 1, visited, True, sequences, reward_info)
                new_row -= 1

            new_row = row + 1
            while new_row < len(matrix) and not visited[new_row][col]:
                search_path(matrix, new_row, col, path, path_coordinate, n - 1, visited, True, sequences, reward_info)
                new_row += 1

    current_path_str = " ".join(path)
    reward = sum(seq[1] for seq in sequences if seq[0] in current_path_str)
    
    if reward > reward_info['max_reward']:
        reward_info['max_reward'] = reward
        reward_info['max_reward_seq'] = current_path_str
        reward_info['seq_coordinate'] = path_coordinate.copy()

    visited[row][col] = False
    path.pop()
    path_coordinate.pop()

def find_sequences(matrix, n, sequences):
    visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    reward_info = {'max_reward': 0, 'max_reward_seq': matrix[0][0], 'seq_coordinate': [[1, 1]]}

    for col in range(len(matrix[0])):
        search_path(matrix, 0, col, [], [], n, visited, False, sequences, reward_info)
    
    return reward_info


while True :
    choice = input("Input from file? (y/n): ").lower()
    if choice != 'y' and choice != 'n' :
        print("\nInvalid choice.\n")
    else :
        if choice == 'y' :
            buffer_length, matrix_size, matrix, num_sequence, sequences = read_file()
        else :
            buffer_length, matrix_size, matrix, num_sequence, sequences = user_input()
        break

print(f"\nMatrix Size: {matrix_size[0]}x{matrix_size[1]}")
print("Matrix:")
for row in matrix:
    print(" ".join(row))
print("\nBuffer Length:", buffer_length)
print("\nNumber of Sequences:", num_sequence)
x = 1
for row in sequences :
    print(f"Sequence {x} : {row[0]} (Reward: {row[1]})")
    x += 1

print("\nMax Reward Solution ")
# process
start = time.time()
result = find_sequences(matrix, buffer_length - 1, sequences)
duration = round((time.time() - start) * 1000)
print(f"Reward: {result['max_reward']}")
print(f"Buffer: {result['max_reward_seq']}")
print(f"Buffer's Token Coordinate: ")
for cdn in result['seq_coordinate']:
    print(f"{cdn[0]}, {cdn[1]}")
print(f"\n{duration} ms\n")

while True :
    choice = input("Do you want to save solution (y/n): ").lower()
    if choice != 'y' and choice != 'n' :
        print("Invalid choice.")
    else :
        save_file(result)
        break
