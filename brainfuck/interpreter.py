import sys
import brainfuck.getch as getch


def evaluate(code):
    code = cleanup(list(code))
    bracemap = buildbracemap(code)
    cells, codeptr, cellptr = [0], 0, 0

    stored_input = []
    stored_output = []

    while codeptr < len(code):
        command = code[codeptr]

        if command == ">":
            cellptr += 1
            if cellptr == len(cells):
                cells.append(0)

        if command == "<":
            cellptr = 0 if cellptr <= 0 else cellptr - 1

        if command == "+":
            cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

        if command == "-":
            cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

        if command == "[" and cells[cellptr] == 0:
            codeptr = bracemap[codeptr]
        if command == "]" and cells[cellptr] != 0:
            codeptr = bracemap[codeptr]
        if command == ".":
            char = chr(cells[cellptr])
            stored_output.append(char)
        if command == ",":
            input_char = getch.getch()  # Get a single character of input
            cells[cellptr] = ord(input_char)
            stored_input.append(input_char)

        codeptr += 1

    return {"input": "".join(stored_input), "output": "".join(stored_output)}


def cleanup(code):
    return "".join(
        filter(lambda x: x in [".", ",", "[", "]", "<", ">", "+", "-"], code)
    )


def buildbracemap(code):
    temp_bracestack, bracemap = [], {}

    for position, command in enumerate(code):
        if command == "[":
            temp_bracestack.append(position)
        if command == "]":
            start = temp_bracestack.pop()
            bracemap[start] = position
            bracemap[position] = start
    return bracemap
