import socket 
# Format user input into protocol-compliant messages
def format_request(line):
    tokens = line.strip().split(" ", 2)
    if len(tokens) < 2:
        return None

    cmd = tokens[0]
    if cmd not in ["PUT", "GET", "READ"]:
        return None

    if cmd == "PUT":
        if len(tokens) != 3:
            return None
        key, value = tokens[1], tokens[2]
        return f"P {key} {value}"

    else:
        key = tokens[1]
        return f"P {key} {value}"
