# ColorfulEngine
a Python engine to print out colorful text in the terminal

## Important
This library is only compatible with windows.  
This library will install Colorama, too.  

## Quickstart
The library consists of two classes.  
One for the **log engine**, and another for **fonts**.  
  
You can also use our **ColofulError** exceptions and **FontError** exceptions to your own will.  

This library supports anything the terminal supports!  

## Colorful Class
### Initializing
**Parameters**:  
`(autoreset: Literal["t", "b", "s", "a"] | Literal[False] = False) -> Colorful`  
`autoreset` parameter -> How you want the engine to autoreset everytime after printing to console.  
  
**Options Explanation**:  
`t` -> Reset text color.  
`b` -> Reset background.  
`s` -> Reset text brightness (style).  
Combine the above for custom resets.  
E.g. `tb` -> Reset text color & background.  
`a` -> Reset everything.  
`False` (bool) -> Disable resetting.  

### Log Text
**Colorful().log()**
**Parameters**  
`(text: str = "Hello, world.", font: Font = Font()) -> str`  
`text` parameter -> The text you want to print.  
`font` parameter -> The style you want to use.  
`font` parameter requires a `Font()` class. Default is -> `new Font()`  

Returns the text you just printed.  

### Reset Console
**Colorful().reset()**  
**Parameters**  
`(param: Literal["t", "b", "s", "a", "tb", "ts", "bs"])`  
Same reset parameters as `Colorful()` class initialization. (Except for `False` option)  

### str(Colorful())
**def \_\_str\_\_()**  
returns a description of the Colorful engine:
"Text Engine with autoreset mode (your reset mode and details)."

## Font Class
### Initializing
**Parameters**:  
`(foreground: str = 'WHITE', background: str = 'BLACK', styling: str = 'NORMAL')`  
`foreground` parameter -> font text color  
`background` parameter -> font bg color  
`srtling` parameter -> font brightness  

**Options Explanation**:  
Parameters are **NOT** case-sensitive.  
For `Background` & `Foreground`:  
 - `BLACK`
 - `RED`
 - `GREEN`
 - `YELLOW`
 - `BLUE`
 - `MAGENTA`
 - `CYAN`
 - `WHITE`
 - `LIGHTBLACK`
 - `LIGHTRED`
 - `LIGHTGREEN`
 - `LIGHTYELLOW`
 - `LIGHTBLUE`
 - `LIGHTMAGENTA`
 - `LIGHTCYAN`
 - `LIGHTWHITE`

For `Styling`:  
 - `DIM`
 - `NORMAL`
 - `BRIGHT`

### Change Properties
**Font().changeFore()**
`foreground` parameter -> new foreground to change to  

returns -> new `Font()` and updates the old `Font()`  

**Font().changeBack()**
`background` parameter -> new background to change to  

**Font().restyle()**
`style` parameter -> new brightness to change to  

### str(Font())
**def \_\_str\_\_()**  
returns a description of the font:  
"(style) (foreground) text in (background) background."  

## Exceptions
### ColorfulError
-> Errors that occured in the `Coloful` class.  
When will it occur:  
 - When you initialize a `Colorful` class with autoreset `True`. Reason -> Confuses computer to not know which autoreset mode?
 - When you initiliaze a `Colorful` class with not supported autoreset types.
 - Manually resetting a `Coloful` engine console while not specifying the autoreset mode correctly.

### FontError
-> Erros that occured in the `Font` class.  
When will it occur:  
 - When you are not setting a `str` value for `Font` class initialization parameters.
 - When you are changing the *foreground*, *background*, or *brightness* (style) to an unsupported value.


## Code Example
```
from __init__ import Colorful, Font

engine = Colorful("tb") # autoreset text and background
engine.log(engine) # Text Engine with autoreset mode "tb" for autoresetting text and background colors.
font1 = Font(foreground="CYAN", styling="BRIGHT") # bright, cyan font

engine.log(text="Hello, world!", font=font1) # (cyan, bright) Hello, world!
# font1 resets text and background
font1.changeBack("BLUE") # change background to blue
font1.changeFore("WHITE") # change foreground to white
# support for Chinese, Korean, Japanese and a lot more!
engine.log(text="哇! 好酷喔!", font=font1) # (white, bright) 哇! 好酷喔! (blue)
# font1 resets text and background
font1.changeBack("MAGENTA") # change background to blue
font1.changeFore("BLACK") # change foreground to white
engine.log(text="안녕하세요", font=font1) # (black, bright) 안녕하세요 (magenta)
# font1 resets text and background
engine.log(font1) # Bright White text in Black background.

engine.reset("a") # Resets the console if you want to use print normally
print("Normal text!") # Normal text!
```
