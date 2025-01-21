def load_file(dll_file):
    variables = {}
    with open(dll_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split('==')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    variables[key] = value
    return '\n'.join([f"{key}: {value}" for key, value in variables.items()])
