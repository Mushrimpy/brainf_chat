from brainfuck.converter import TextBrainfuckConverter
import brainfuck.interpreter as interpreter


converter = TextBrainfuckConverter()


def brainfuck_io(input_string):
    # Pass data through the Brainfuck converter and interpreter.
    bf_code = converter.string_to_bf(input_string)
    result = interpreter.evaluate(bf_code)
    return result["output"]
