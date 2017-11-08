def add_token(out, current_token):
    current_token = current_token.strip()
    if current_token != "":
        out.append(current_token)

def lex(s):
    out = []
    current_token = ""
    i = 0
    while i < len(s):
        if s[i] == ";":
            add_token(out, current_token)
            add_token(out, ";")
            current_token = ""
            i += 1
        elif s[i] == "&" and s[i+1] == "&":
            add_token(out, current_token)
            add_token(out, "&&")
            current_token = ""
            i += 2
        elif s[i] == "|" and s[i+1] == "|":
            add_token(out, current_token)
            add_token(out, "||")
            current_token = ""
            i += 2
        elif s[i] == "(":
            add_token(out, current_token)
            add_token(out, "(")
            current_token = ""
            i += 1
        elif s[i] == ")":
            add_token(out, current_token)
            add_token(out, ")")
            current_token = ""
            i += 1
        elif s[i] == "!":
            add_token(out, current_token)
            add_token(out, "!")
            current_token = ""
            i += 1
        else:
            current_token += s[i]
            i += 1
    add_token(out, current_token)
    return out

def parse(tokens):
    out = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "(":
            closeparen = i+1 + tokens[i+1:].index(")")
            out.append(parse(tokens[i+1:closeparen]))
            i = closeparen+1
        else:
            out.append(tokens[i])
            i += 1
    return out
