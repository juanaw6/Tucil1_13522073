import random

def isAlphanumeric(token):
    alfanum = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if len(token) != 2 :
        return False
    if token[0] in alfanum and token[1] in alfanum :
        return True
    return False

def input_valid_int(msg, min):
    while True :
        try :
            integer = int(input(f"\n{msg}"))
            if integer < min :
                print(f"\nInvalid, input must be integer greater than {min - 1}.")
            else :
                return integer
        except :
            print(f"\nInvalid, input must be integer greater than {min - 1}.")

def input_valid_an(msg):
    while True :
        try :
            token = input(f"\n{msg}").upper()
            if not isAlphanumeric(token):
                print("\nInvalid, input must be alphanumeric.")
            else :
                return token
        except :
            print("\nInvalid, input must be alphanumeric.")

def generate_matrix(matrix_size, tokens):
    matrix = [[0 for _ in range(matrix_size[0])] for _ in range(matrix_size[1])]
    for i in range(matrix_size[1]):
        for j in range(matrix_size[0]):
            matrix[i][j] = random.choice(tokens)
    return matrix

def generate_sequences(num, max_length, tokens):
    sequences = []
    list_of_seq = []
    for _ in range(num):
        length = random.randint(2, max_length)
        while True:
            seq = " ".join([random.choice(tokens) for _ in range(length)])
            if seq not in list_of_seq :
                list_of_seq.append(seq)
                break
        reward = random.randint(0, 50)
        sequences.append([seq, reward])
    return sequences


def user_input():
    n_unique_token = input_valid_int("Number of unique tokens: ", 1)
    tokens = []
    for i in range(n_unique_token) :
        token = input_valid_an(f"Input alphanumeric token no.{i + 1} (A1, 3E, etc.): ")
        tokens.append(token)
    buffer_length = input_valid_int("Input buffer length: ", 1)
    matrix_col = input_valid_int("Input matrix column size: ", 1)
    matrix_row = input_valid_int("Input matrix row size: ", 2)
    matrix_size = (matrix_col, matrix_row)
    matrix = generate_matrix(matrix_size, tokens)
    num_sequence = input_valid_int("Input number of sequences: ", 1)
    max_sequence_length = input_valid_int("Input maximum sequence's length: ", 2)
    sequences = generate_sequences(num_sequence, max_sequence_length, tokens)

    return buffer_length, matrix_size, matrix, num_sequence, sequences

def read_file():
    while True :
        filename = input("\nInput .txt filename (no need for extension): ")
        file_path = f"../test/input/{filename}.txt"
        try :
            with open(file_path, 'r') as file:
                lines = file.readlines()

                buffer_length = int(lines[0].strip())
                matrix_size = tuple(map(int, lines[1].strip().split()))
                matrix = []
                
                for i in range(2, 2 + matrix_size[1]):
                    row = lines[i].strip().split()
                    matrix.append(row)
                
                num_sequence = int(lines[2 + matrix_size[1]])
                
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
        except :
            print("\nFile not found.")
    
def save_file(reward_info):
    filename = input("\nInput filename (no need for extension): ")
    file_path = f"../test/output/{filename}.txt"

    output_str = ""
    output_str += str(reward_info['max_reward']) + '\n'
    output_str += reward_info['max_reward_seq'] + '\n'
    for cdn in reward_info['seq_coordinate']:
        output_str += f"{cdn[0]}, {cdn[1]}\n"
    output_str = output_str[:-1]

    with open(file_path, 'w') as file:
        file.write(output_str)
    
    print(f"\nOutput has been saved to test/output/{filename}.txt!")