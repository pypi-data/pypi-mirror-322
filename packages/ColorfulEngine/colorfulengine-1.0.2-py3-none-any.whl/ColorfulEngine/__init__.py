try:
    from msvcrt import get_osfhandle
except ImportError:
    raise OSError("This library requires Windows. If you wish to uninstall, you can also remove Colorama if not needed.")


import colorama
from colorama import Fore, Back, Style
from typing import Literal

colorama.init() # autoreset=True

class FontError(Exception):
    def __init__(self, message: str = "Font Error raised. Check configurations in 'Font' objects."):
        super().__init__(message)
        self.message = message
    def __str__(self):
        return self.message
    
class ColorfulError(Exception):
    def __init__(self, message: str = "Colorful Error raised. Check configurations in 'Colorful' objects."):
        super().__init__(message)
        self.message = message
    def __str__(self):
        return self.message

class Font:
    def __init__(self, foreground: str = 'WHITE', background: str = 'BLACK', styling: str = 'NORMAL'):
        """
        Foreground and Background options:
        'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE', 'LIGHTBLACK', 'LIGHTRED', 'LIGHTGREEN', 'LIGHTYELLOW', 'LIGHTBLUE', 'LIGHTMAGENTA', 'LIGHTCYAN', 'LIGHTWHITE'
        
        Styling options:
        'DIM', 'NORMAL', 'BRIGHT'

        Important Info: paramters NOT case-sensetive :)
        """
        self.fabs = ['BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE', 'LIGHTBLACK', 'LIGHTRED', 'LIGHTGREEN', 'LIGHTYELLOW', 'LIGHTBLUE', 'LIGHTMAGENTA', 'LIGHTCYAN', 'LIGHTWHITE']
        self.styles = ['DIM', 'NORMAL', 'BRIGHT']
        nf = foreground.upper()
        nb = background.upper()
        ns = styling.upper()

        if not ((nf in self.fabs) and (nb in self.fabs) and (ns in self.styles)):
            raise FontError("One of foreground, background or styling values is having a wrong type.")
        else:
            self.fore = nf
            self.back = nb
            self.style = ns
    def changeFore(self, foreground: Literal['BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE', 'LIGHTBLACK', 'LIGHTRED', 'LIGHTGREEN', 'LIGHTYELLOW', 'LIGHTBLUE', 'LIGHTMAGENTA', 'LIGHTCYAN', 'LIGHTWHITE']):
        nf = foreground.upper()
        if not (nf in self.fabs):
            raise FontError("Foreground cannot be changed. Selected foreground doesn't exist.")
        else:
            self.fore = nf
        return self
    def changeBack(self, background: Literal['BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE', 'LIGHTBLACK', 'LIGHTRED', 'LIGHTGREEN', 'LIGHTYELLOW', 'LIGHTBLUE', 'LIGHTMAGENTA', 'LIGHTCYAN', 'LIGHTWHITE']):
        nf = background.upper()
        if not (nf in self.fabs):
            raise FontError("Background cannot be changed. Selected background doesn't exist.")
        else:
            self.back = nf
        return self
    def restyle(self, style: Literal["DIM", "NORMAL", "BRIGHT"]):
        nf = style.upper()
        if not (nf in self.styles):
            raise FontError("Style cannot be changed. Selected style doesn't exist.")
        else:
            self.style = nf
        return self
    def __str__(self):
        return f"{self.style.capitalize()} {self.fore.capitalize()} text in {self.back.capitalize()} background."


class Colorful:
    def __init__(self, autoreset: Literal["t", "b", "s", "a", "tb", "ts", "bs"] | Literal[False] = False):
        """
        autoreset parameters:\n
        "t" for autoresetting text colors\n
        "b" for autoresetting background colors\n
        "s" for autoresetting text styles\n
        Combine the above for custom resets.
        "a" for autoresetting everything\n
        False boolean for disable autoresetting
        """
        self.mode = {
            "t": '"t" for autoresetting text colors',
            "b": '"b" for autoresetting background colors',
            "s": '"s" for autoresetting text styles',
            "a": '"a" for autoresetting everything',
            "tb": '"tb" for autoresetting text and background colors',
            "ts": '"ts" for autoresetting text colors and styles',
            "bs": '"bs" for autoresetting background colors and styles',
            "False": 'False boolean for disable autoresetting'
        }
        if type(autoreset) is bool:
            if not autoreset:
                self.resets = [False, "n"]
            else:
                raise ColorfulError("autoreset parameter should not be a 'True' boolean value.")
        elif type(autoreset) is str:
            if autoreset in ["t", "b", "s", "a", "tb", "ts", "bs"]:
                self.resets = [True, autoreset]
            else:
                raise ColorfulError("autoreset parameter should be one of 't', 'b', 's', 'tb', 'ts', 'bs', or 'a'.")
    def log(self, text: str = "Hello, world.", font: Font = Font()):
        'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE', 'LIGHTBLACK', 'LIGHTRED', 'LIGHTGREEN', 'LIGHTYELLOW', 'LIGHTBLUE', 'LIGHTMAGENTA', 'LIGHTCYAN', 'LIGHTWHITE'
        fore = font.fore.upper()
        back = font.back.upper()
        style = font.style.upper()
        referenceF = {
            'BLACK': Fore.BLACK,
            'RED': Fore.RED,
            'GREEN': Fore.GREEN,
            'YELLOW': Fore.YELLOW,
            'MAGENTA': Fore.MAGENTA,
            'CYAN': Fore.CYAN,
            'WHITE': Fore.WHITE,
            'BLUE': Fore.BLUE,
            'LIGHTBLACK': Fore.LIGHTBLACK_EX,
            'LIGHTRED': Fore.LIGHTRED_EX,
            'LIGHTGREEN': Fore.LIGHTGREEN_EX,
            'LIGHTYELLOW': Fore.LIGHTYELLOW_EX,
            'LIGHTMAGENTA': Fore.LIGHTMAGENTA_EX,
            'LIGHTCYAN': Fore.LIGHTCYAN_EX,
            'LIGHTWHITE': Fore.LIGHTWHITE_EX,
            'LIGHTBLUE': Fore.LIGHTBLUE_EX,
        }
        referenceB = {
            'BLACK': Back.BLACK,
            'RED': Back.RED,
            'GREEN': Back.GREEN,
            'YELLOW': Back.YELLOW,
            'MAGENTA': Back.MAGENTA,
            'CYAN': Back.CYAN,
            'WHITE': Back.WHITE,
            'BLUE': Back.BLUE,
            'LIGHTBLACK': Back.LIGHTBLACK_EX,
            'LIGHTRED': Back.LIGHTRED_EX,
            'LIGHTGREEN': Back.LIGHTGREEN_EX,
            'LIGHTYELLOW': Back.LIGHTYELLOW_EX,
            'LIGHTMAGENTA': Back.LIGHTMAGENTA_EX,
            'LIGHTCYAN': Back.LIGHTCYAN_EX,
            'LIGHTWHITE': Back.LIGHTWHITE_EX,
            'LIGHTBLUE': Back.LIGHTBLUE_EX,
        }
        referenceS = {
            'DIM': Style.DIM,
            'NORMAL': Style.NORMAL,
            'BRIGHT': Style.BRIGHT
        }
        print(f"{referenceF[fore]}{referenceB[back]}{referenceS[style]}{text}")
        if (type(self.resets[0]) is bool and self.resets[0]):
            referenceR = {
                "t": Fore.RESET,
                "b": Back.RESET,
                "s": Style.NORMAL,
                "a": Style.RESET_ALL,
                "tb": Fore.RESET + Back.RESET, 
                "ts": Fore.RESET + Style.NORMAL, 
                "bs": Back.RESET + Style.NORMAL
            }
            constant = self.resets[1]
            if constant == "a":
                font.changeBack("BLACK")
                font.changeFore("WHITE")
                font.restyle("NORMAL")
            elif constant == "t":
                font.changeFore("WHITE")
            elif constant == "b":
                font.changeBack("BLACK")
            elif constant == "s":
                font.restyle("NORMAL")
            elif constant == "tb":
                font.changeBack("BLACK")
                font.changeFore("WHITE")
            elif constant == "ts":
                font.changeFore("WHITE")
                font.restyle("NORMAL")
            elif constant == "bs":
                font.changeBack("BLACK")
                font.restyle("NORMAL")
            print(referenceR[self.resets[1]], end="")
        return text
    def reset(self, param: Literal["t", "b", "s", "a", "tb", "ts", "bs"]):
        """
        RESETS THE TERMINAL ONLY.
        """
        if param in ["t", "b", "s", "a", "tb", "ts", "bs"]:
            referenceR = {
                "t": Fore.RESET,
                "b": Back.RESET,
                "s": Style.NORMAL,
                "a": Style.RESET_ALL,
                "tb": Fore.RESET + Back.RESET, 
                "ts": Fore.RESET + Style.NORMAL, 
                "bs": Back.RESET + Style.NORMAL
            }
            print(referenceR[param], end="")
        else:
            raise Colorful("Cannot reset manually. Reset mode not specified correctly.")
        return self
    def __str__(self):
        if (type(self.resets[0]) is bool and self.resets[0]):
            return f"Text Engine with autoreset mode {self.mode[self.resets[1]]}."
        else:
            return f"Text Engine with autoreset mode {self.mode[str(False)]}."
