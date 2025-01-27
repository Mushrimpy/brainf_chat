class TextBrainfuckConverter:
    def __init__(self):
        pass

    def _char_to_bf(self, char):
        # Uses current cell as a counter for a loop that increments the next cell 10 times
        # Loop runs for ASCII code divided by 10, remainder handled by additional increments
        buffer = "[-]>[-]<"
        for i in range(ord(char) // 10):
            buffer += "+"
        buffer += "[>++++++++++<-]>"
        for i in range(ord(char) % 10):
            buffer += "+"
        buffer += ".<"
        return buffer

    def _delta_to_bf(self, delta):
        # Converts ASCII value differences to optimized Brainfuck code
        buffer = ""
        for i in range(abs(delta) // 10):
            buffer += "+"

        if delta > 0:
            buffer += "[>++++++++++<-]>"
        else:
            buffer += "[>----------<-]>"

        for i in range(abs(delta) % 10):
            buffer += "+" if delta > 0 else "-"
        buffer += ".<"
        return buffer

    def string_to_bf(self, string, commented=False):
        buffer = ""
        if not string:
            return buffer

        for i, char in enumerate(string):
            if i == 0:
                buffer += self._char_to_bf(char)
            else:
                delta = ord(string[i]) - ord(string[i - 1])
                buffer += self._delta_to_bf(delta)
            if commented:
                buffer += " " + char + "\n"
        return buffer
