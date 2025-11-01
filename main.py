import random
content=list()
list_of_commands = ['print', 'math', 'list', 'random_number', 'append_in_list']
math_list = ['+',"-","*","/"]
letters = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z']
list1, list2, list3 = list(), list(), list()
def RANDG_1(command):
    if command.startswith('print'):
        if command.startswith('print "') and command.endswith('"'):
            try:
                print(command[7:-1])
            except:
                print(''.join(random.choices(letters, k=random.randint(3, 16))))
        else:
            print(''.join(random.choices(letters, k=random.randint(3, 16))))
    elif command.startswith('math'):
        if command.startswith('math (') and command.endswith(')'):
            try:
                result = eval(command[6:-1])
                print(f'{command[6:-1]} = {result}')
            except Exception:
                print(f'Error calculating: {Exception}')
        else:
            randg_num1=random.randint(-999, 999)
            randg_num2=random.randint(-999, 999)
            if random.choice(math_list) == '+':
                print(f'{randg_num1} + {randg_num2} = {randg_num1+randg_num2}')
            elif random.choice(math_list) == '-':
                print(f'{randg_num1} - {randg_num2} = {randg_num1-randg_num2}')
            elif random.choice(math_list) == '*':
                print(f'{randg_num1} * {randg_num2} = {randg_num1*randg_num2}')
            elif random.choice(math_list):
                try:
                    print(f'{randg_num1} / {randg_num2} = {randg_num1/randg_num2}')
                except ZeroDivisionError:
                    print('ZeroDivisionError')
    elif command == 'list':
        if random.randint(1, 3) == 1:
            print(f'List1: {list1}')
        elif random.randint(1, 3) == 2:
            print(f'List2: {list2}')
        elif random.randint(1, 3) == 3:
            print(f'List3: {list3}')
        else:
            print("List id ")
    elif command == 'random_number':
        number_generated_randomly=random.randint(-999, 999)
        print(number_generated_randomly)
    elif command == 'append_in_list':
        if random.randint(1, 2) == 1:
            if random.randint(1, 3) == 1:
                list1.append(random.randint(-999, 999))
            elif random.randint(1, 3) == 2:
                list2.append(random.randint(-999, 999))
            elif random.randint(1, 3) == 3:
                list3.append(random.randint(-999, 999))
        elif random.randint(1, 2) == 2:
            if random.randint(1, 3) == 1:
                list1.append(''.join(random.choices(letters, k=random.randint(3, 16))))
            elif random.randint(1, 3) == 2:
                list2.append(''.join(random.choices(letters, k=random.randint(3, 16))))
            elif random.randint(1, 3) == 3:
                list3.append(''.join(random.choices(letters, k=random.randint(3, 16))))

def READ_RANDG(filename):
    with open(filename, 'r') as file:
        commands = file.readlines()
    return [command_1.strip() for command_1 in commands]

def EXEC_RANDG(filename):
    commands = READ_RANDG(filename)
    for command in commands:
            if command in list_of_commands or command.startswith('print') or command.startswith('math'):
                RANDG_1(command)
            elif command.startswith('RANDG(') and command.endswith(')'):
                try:
                    num_commands = int(command[6:-1])
                    RANDG(num_commands)
                except ValueError:
                    print(f"ValueError: {command}")
            else:
                print(f'Unkown command: {command}')

def RANDG(code_lines):
    try:
        for i in range(code_lines):
            current_command=random.choice(list_of_commands)
            content.append(current_command)
            RANDG_1(current_command)
    except:
        print(f"Error creating loop for: {code_lines}")

EXEC_RANDG("test.randg") # Replace test.randg with your file path
