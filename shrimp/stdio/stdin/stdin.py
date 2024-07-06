class Text:
    """Class for handling text input."""

    def __str__(self):
        return self.value

    def __repr__self(self):
        return self.value

    def txtin(self, prompt) -> str:
        """Prompt for text input."""
        stdin = input(prompt)
        self.value = stdin
        return self.value

    @staticmethod
    def isalpha(stdin) -> bool:
        """Check if input is alphabetic."""
        return stdin.isalpha()

    def alphain(self, prompt) -> str:
        """Prompt for alphabetic input. (no numbers or symbols and no spaces)"""
        stdin = input(prompt)
        self.value = stdin if stdin.isalpha() else self.alphain(prompt)
        return self.value

    @staticmethod
    def is_alpha_and_spaces(stdin) -> bool:
        """Check if input is alphabetic with spaces or with no spaces."""
        if " " in stdin:
            return "".join(stdin.split()).isalpha()
        return stdin.isalpha()

    def alpha_and_spaces_in(self, prompt) -> str:
        """Prompt for alphabetic input. (with spaces or with no spaces but no numbers or symbols)"""
        stdin = input(prompt)
        self.value = (
            stdin
            if Text.is_alpha_and_spaces(stdin)
            else self.alpha_and_spaces_in(prompt)
        )
        return self.value

    @staticmethod
    def isname(stdin) -> bool:
        """Check if input is a name."""
        if " " in stdin:
            return "".join(stdin.split(" ")).isalpha()
        return stdin.isalpha()

    def namein(self, prompt) -> str:
        """Prompt for alphabetic input. (no numbers or symbols)"""
        stdin = input(prompt)
        self.value = stdin if self.isname(stdin) else self.namein(prompt)
        return self.value


class Symbol:
    """Class for handling symbol input."""

    @staticmethod
    def issymbol(stdin) -> bool:
        """Check if input is a symbol."""
        if not (
            stdin.isalpha()
            or stdin.isnumeric()
            or stdin.isspace()
            or stdin == ""
            or ("".join(stdin.split()).isalpha() and " " in stdin)
        ):
            return True
        return False

    def symbolin(self, prompt) -> str:
        """Prompt for symbols input. (no numbers or alphabetic)"""
        stdin = input(prompt)
        self.value = stdin if Symbol.issymbol(stdin) else self.symbolin(prompt)
        return self.value


class Number:
    """Class for handling number input."""

    @staticmethod
    def isnum(stdin) -> bool:
        """Check if input is a number."""
        if "".join(stdin.split(".")).isnumeric() and "." in stdin:
            return True
        return False

    def numin(self, prompt) -> int | float:
        """Prompt for numeric input. (int or float)"""
        stdin = input(prompt)
        self.value = (
            float(stdin)
            if (Number.isfloat(stdin))
            else (int(stdin) if Number.isint(stdin) else self.numin(prompt))
        )
        return self.value

    @staticmethod
    def isint(stdin) -> bool:
        """Check if input is an integer."""
        try:
            int(stdin)
            return True
        except ValueError:
            return False

    def intin(self, prompt) -> int:
        """Prompt for integer input."""
        stdin = input(prompt)
        self.value = int(stdin) if stdin.isnumeric() else self.intin(prompt)
        return self.value

    @staticmethod
    def isfloat(stdin) -> bool:
        """Check if input is a float."""
        try:
            float(stdin)
            return True
        except ValueError:
            return False

    def floatin(self, prompt) -> float:
        """Prompt for float input."""
        stdin = input(prompt)
        self.value = float(stdin) if Number.isfloat(stdin) else self.floatin(prompt)
        return self.value


class Char:
    """Class for handling character input."""

    def __int__(self):
        if Number.isint(self.value):
            self.value = int(self.value)
            return self.value
        else:
            raise ValueError("Invalid input, input is not of type int")

    @staticmethod
    def again(prompt: str, valid: list[str], nore: list[str]) -> bool:
        play_again = Char()
        play_again.validin(prompt, valid)
        if play_again in nore:
            return False
        return True

    @staticmethod
    def ischar(stdin: str) -> bool:
        """Check if input is alphabetic."""
        if type(stdin) != type(str):
            print("Warning! : Invalid input, input is not of type str")
            return False
        elif len(stdin) == 1 or stdin == " " or stdin == "":
            return True
        else:
            return False

    def __eq__(self, other):
        return self.value == other

    def charin(self, prompt) -> str:
        """Prompt for character input."""
        stdin = input(prompt)
        self.value = stdin if Char.ischar(stdin) else self.charin(prompt)
        return self.value

    @staticmethod
    def isint(stdin) -> bool:
        """Check if input is an integer."""
        try:
            int(stdin)
            return True
        except ValueError:
            return False

    def intin(self, prompt) -> int:
        """Prompt for integer input."""
        stdin = input(prompt)
        self.value = int(stdin) if Char.isint(stdin) else self.intin(prompt)
        return self.value

    @staticmethod
    def isvalid(valid: list[str], stdin) -> bool:
        return stdin in valid

    def validin(self, prompt: str, valid: list[str]) -> str | int:
        """Prompt for valid input. (valid is a list of characters)"""
        stdin = input(prompt)
        if Char.isvalid(valid, stdin):
            self.value = stdin
            return self.value
        self.value = Char.validin(self, prompt, valid)
        return self.value


def __doc__():
    """
    This module contains classes to get input from the user.
    The classes and their methods are:

    TextInput:
        - txtin(prompt) -> str
        - isapha(stdin) -> bool
        - alphain(prompt) -> str
        - is_alpha_and_spaces(stdin) -> bool
        - alpha_and_spaces_in(prompt) -> str
        - isname(stdin) -> bool
        - namein(prompt) -> str

    SymbolInput:
        - issymbol(stdin) -> bool
        - symbolin(prompt) -> str

    NumberInput:
        - isnum(stdin) -> bool
        - numin(prompt) -> int | float
        - isint(stdin) -> bool
        - intin(prompt) -> int
        - isfloat(stdin) -> bool
        - floatin(prompt) -> float

    These classes and methods are used to get input from the user.
    They return the input as a string, integer, or float.
    """
    return __doc__
