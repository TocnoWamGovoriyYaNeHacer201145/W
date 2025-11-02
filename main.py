import random
import re

class RANDGInterpreter:
    def __init__(self):
        self.content = []
        self.list_of_commands = ['print', 'math', 'list', 'random_number', 'append_in_list', 'if', 'var', 'funct', 'return']
        self.math_list = ['+', "-", "*", "/"]
        self.letters = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z']
        self.list1, self.list2, self.list3 = [], [], []
        self.variables = {}
        self.functions = {}
        self.current_function = None
        self.function_stack = []
        self.return_value = None
    
    def EVAL_CONDITION(self, condition):
        try:
            for var_name, var_value in self.variables.items():
                condition = condition.replace(var_name, str(var_value))
            return eval(condition, {'__builtins__': {}}, {})
        except:
            return False
    
    def EVAL_EXPRESSION(self, expression):
        try:
            for var_name, var_value in self.variables.items():
                expression = expression.replace(var_name, str(var_value))
            return eval(expression, {'__builtins__': {}}, {})
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {e}")
    
    def EXEC_BLOCK(self, commands):
        for cmd in commands:
            if self.return_value is not None:
                return
            if cmd in self.list_of_commands or cmd.startswith('print') or cmd.startswith('math') or cmd.startswith('if') or cmd.startswith('var') or cmd.startswith('func') or cmd.startswith('return') or '(' in cmd:
                self.RANDG_1(cmd)
            elif cmd.startswith('RANDG(') and cmd.endswith(')'):
                try:
                    num_commands = int(cmd[6:-1])
                    self.RANDG(num_commands)
                except ValueError:
                    print(f"ValueError: {cmd}")
    
    def PROCESS_VARIABLE(self, command):
        if command.startswith('var '):
            parts = command[4:].split('=', 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                var_value = parts[1].strip()
                if var_value.startswith('"') and var_value.endswith('"'):
                    self.variables[var_name] = var_value[1:-1]
                else:
                    try:
                        self.variables[var_name] = self.EVAL_EXPRESSION(var_value)
                    except:
                        self.variables[var_name] = var_value
                return True
        return False
    
    def PROCESS_FUNCTION_DEF(self, command):
        if command.startswith('funct '):
            if ')' in command and '{' in command:
                funct_start = 5
                param_start, param_end = command.find('('), command.find(')')
                funct_name = command[funct_start:param_start].strip()
                params_str = command[param_start+1:param_end].strip()
                params = [p.strip() for p in params_str.split(',')] if params_str else []
                self.functions[funct_name] = {
                    'params': params,
                    'body': command
                }
                return True
        return False
    
    def CALL_FUNCTION(self, command):
        if '(' in command and command.endswith(')'):
            funct_name = command.split('(')[0].strip()
            if funct_name in self.functions:
                args_str = command[command.find('(')+1:-1].strip()
                args = [arg.strip() for arg in args_str.split(',')] if args_str else []
                old_variables = self.variables.copy()
                self.function_stack.append({
                    'variables': old_variables,
                    'return_value': self.return_value
                })
                funct_data = self.functions[funct_name]
                for i, param in enumerate(funct_data['params']):
                    if i < len(args):
                        arg_value = args[i]
                        if arg_value.startswith('"') and arg_value.endswith('"'):
                            self.variables[param] = arg_value[1:-1]
                        else:
                            try:
                                self.variables[param] = self.EVAL_EXPRESSION(arg_value)
                            except:
                                self.variables[param] = arg_value
                self.return_value = None
                funct_body = funct_data['body']
                body_start = funct_body.find('{') + 1
                body_end = funct_body.rfind('}')
                body_commands = [cmd.strip() for cmd in funct_body[body_start:body_end].split('\n') if cmd.strip() and cmd.strip() != '}']
                for cmd in body_commands:
                    if self.return_value is not None:
                        break
                    self.RANDG_1(cmd)
                stack_data = self.function_stack.pop()
                self.variables = stack_data['variables']
                result = self.return_value
                self.return_value = stack_data['return_value']
                
                return result
            
            else:
                print(f"Unknown function: {funct_name}")
        
        return None
    
    def PROCESS_RETURN(self, command):
        if command.startswith('return'):
            return_expr = command[6:].strip()
            if return_expr:
                try:
                    self.return_value = self.EVAL_EXPRESSION(return_expr)
                except:
                    self.return_value = return_expr
            else:
                self.return_value = None
            return True
        return False
    
    def SUBSTITUTE_VARIABLES(self, text):
        for var_name, var_value in self.variables.items():
            text = text.replace(var_name, str(var_value))
        return text
    
    def RANDG_1(self, command):
        if command.startswith('print'):
            if command.startswith('print "') and command.endswith('"'):
                try:
                    text = command[7:-1]
                    text = self.SUBSTITUTE_VARIABLES(text)
                    print(text)
                except:
                    print(''.join(random.choices(self.letters, k=random.randint(3, 16))))
            else:
                var_name = command[5:].strip()
                if var_name in self.variables:
                    print(self.variables[var_name])
                else:
                    print(''.join(random.choices(self.letters, k=random.randint(3, 16))))
        
        elif command.startswith('math'):
            if command.startswith('math (') and command.endswith(')'):
                try:
                    expression = command[6:-1]
                    expression = self.SUBSTITUTE_VARIABLES(expression)
                    result = eval(expression, {'__builtins__': {}}, {})
                    print(f'{expression} = {result}')
                except Exception as e:
                    print(f'Error calculating: {e}')
            else:
                randg_num1 = random.randint(-999, 999)
                randg_num2 = random.randint(-999, 999)
                operation = random.choice(self.math_list)
                if operation == '+':
                    print(f'{randg_num1} + {randg_num2} = {randg_num1 + randg_num2}')
                elif operation == '-':
                    print(f'{randg_num1} - {randg_num2} = {randg_num1 - randg_num2}')
                elif operation == '*':
                    print(f'{randg_num1} * {randg_num2} = {randg_num1 * randg_num2}')
                elif operation == '/':
                    try:
                        print(f'{randg_num1} / {randg_num2} = {randg_num1 / randg_num2}')
                    except ZeroDivisionError:
                        print('ZeroDivisionError')
        
        elif command.startswith('var '):
            self.PROCESS_VARIABLE(command)
        
        elif command.startswith('funct '):
            self.PROCESS_FUNCTION_DEF(command)
        
        elif command.startswith('return'):
            self.PROCESS_RETURN(command)
        
        elif '(' in command and command.endswith(')'):
            self.CALL_FUNCTION(command)
        
        elif command == 'list':
            if random.randint(1, 3) == 1:
                print(f'List1: {self.list1}')
            elif random.randint(1, 3) == 2:
                print(f'List2: {self.list2}')
            elif random.randint(1, 3) == 3:
                print(f'List3: {self.list3}')
            else:
                print("List id")
        
        elif command == 'random_number':
            number_generated_randomly = random.randint(-999, 999)
            print(number_generated_randomly)
        
        elif command == 'append_in_list':
            if random.randint(1, 2) == 1:
                if random.randint(1, 3) == 1:
                    self.list1.append(random.randint(-999, 999))
                elif random.randint(1, 3) == 2:
                    self.list2.append(random.randint(-999, 999))
                elif random.randint(1, 3) == 3:
                    self.list3.append(random.randint(-999, 999))
            elif random.randint(1, 2) == 2:
                if random.randint(1, 3) == 1:
                    self.list1.append(''.join(random.choices(self.letters, k=random.randint(3, 16))))
                elif random.randint(1, 3) == 2:
                    self.list2.append(''.join(random.choices(self.letters, k=random.randint(3, 16))))
                elif random.randint(1, 3) == 3:
                    self.list3.append(''.join(random.choices(self.letters, k=random.randint(3, 16))))
    
    def READ_RANDG(self, filename): # Reads .randg file
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        commands = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            if (line.startswith('if (') or line.startswith('funct ')) and '{' in line:
                block = [line]
                if '}' not in line:
                    i += 1
                    while i < len(lines) and '}' not in lines[i]:
                        cleaned_line = lines[i].strip()
                        if cleaned_line:
                            block.append(cleaned_line)
                        i += 1
                    if i < len(lines):
                        block.append(lines[i].strip())
                commands.append('\n'.join(block))
            else:
                commands.append(line)
            i += 1
        return commands
    
    def EXEC_RANDG(self, filename): # Executes .randg file
        commands = self.READ_RANDG(filename)
        i = 0
        while i < len(commands):
            command = commands[i]
            if command.startswith('if'):
                lines = command.split('\n')
                first_line = lines[0].strip()
                if first_line.startswith('if (') and ') {' in first_line:
                    condition_start = 4
                    condition_end = first_line.find(') {')
                    condition = first_line[condition_start:condition_end]
                    block_commands = []
                    for line in lines[1:]:
                        line = line.strip()
                        if line == '}' or not line:
                            continue
                        block_commands.append(line)
                    if self.EVAL_CONDITION(condition):
                        self.EXEC_BLOCK(block_commands)
        
            elif command.startswith('RANDG(') and command.endswith(')'):
                try:
                    num_commands = int(command[6:-1])
                    self.RANDG(num_commands)
                except ValueError:
                    print(f"ValueError: {command}")
        
            elif command.startswith('funct '):
                self.RANDG_1(command)  # Function creation
        
            elif command in self.list_of_commands or command.startswith('print') or command.startswith('math') or command.startswith('var') or command.startswith('return') or '(' in command:
                self.RANDG_1(command)
        
            else:
                print(f'Unknown command: {command}')
        
            i += 1
    
    def RANDG(self, code_lines):
        try:
            for i in range(code_lines):
                current_command = random.choice(self.list_of_commands)
                self.content.append(current_command)
                self.RANDG_1(current_command)
        except Exception as e:
            print(f"Error creating loop for line: {code_lines}, error: {e}")

# Usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: <your python version, python3 as exmaple> main.py <your .randg version>")
        sys.exit(1)
    filename = sys.argv[1]
    interpreter = RANDGInterpreter()
    interpreter.EXEC_RANDG(filename) # Or replace filename with you file path
