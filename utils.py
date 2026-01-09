from enum import Enum
import time
import shutil
import inspect

class text_style(Enum):
    REGULAR = 1
    TYPED = 2

class Color(Enum):
  BLACK = 30
  RED = 31
  GREEN = 32
  YELLOW = 33
  BLUE = 34
  MAGENTA = 35
  CYAN = 36
  WHITE = 37

  BRIGHT_BLACK = 90
  BRIGHT_RED = 91
  BRIGHT_GREEN = 92
  BRIGHT_YELLOW = 93
  BRIGHT_BLUE = 94
  BRIGHT_MAGENTA = 95
  BRIGHT_CYAN = 96
  BRIGHT_WHITE = 97
   


class cmd: #wrapper incase other things are added 
  class frontend:
    current_color = Color.BRIGHT_WHITE
    current_phrase = []
    current_style = text_style.REGULAR
    cached_phrases = []

    
    def center(self, text : str) -> str:
      return text.center(shutil.get_terminal_size().columns) 
      # gets the x center of the terminal  and centers the text
    
    
    def printEx(self, text: str, centered: bool = False, end: str = "\n"):
      output = self.center(text) if centered else text

      if self.current_style == text_style.REGULAR:
          print(output, end=end, flush=True)
          return

      if self.current_style == text_style.TYPED:
          for char in output:
              print(char, end="", flush=True)
              time.sleep(0.05)
          print(end=end, flush=True)

    def pause(self):
      input("")
      
    def SetPrintStyle(self, current_style):
      type(self).current_style = current_style

    
    def SetForeColor(self, current_color):
      type(self).current_color = current_color

      print(f"\033[{self.current_color.value}m") #console cmd to change foreground color
      
    def send(self, current_phrase: list[str], centered : bool = False, end : str = "\n"):
      type(self).current_phrase = current_phrase
    #sets the type of the current phrase 
      for phrase in self.current_phrase: #prints all the values(strings) in the vector 
          self.printEx(phrase, centered, end)

    def get_inputs(self, text) -> str:
      # -> str defines this function as returning a string value 
      lines = []
      while True:
          line = input(text)
          if line.strip() == "":
              break
          lines.append(line)
      return "\n".join(lines) 
    
    def collect_cache(self, current_phrase: str, end_line : bool = True):
      type(self).cached_phrases.append(current_phrase)
      #added current phrase to the pool(vector) value
  
    def trash_cache(self):
       type(self).cached_phrases.clear() #clears the vector / list 
      
    def send_cache(self, dump : bool = True):
      for phrase in self.cached_phrases:
        self.printEx(phrase)
      if(dump):
        self.trash_cache() #example of memory optimization 


    def cls(self, reset_col : bool = False, reset_style : bool = False):
      print("\033c", end="") #cleats screen
      if reset_col == 0:
        self.SetForeColor(self.current_color) #puts back on the orginial color 
      if reset_style == 0:
        self.SetPrintStyle(self.current_style) #puts back on the current print style used 


    def normalize_user_args(self, target, user_text: str): 
        sig = inspect.signature(target)
        params = list(sig.parameters.values()) #getting params

        #get rid of self 
        if params and params[0].name == "self":
            params = params[1:]

        # No parameters expected
        if not params:
            return ()

        first = params[0]

        # send(self, list[str])
        # if list
        """
      please note I have not added the ability to send mulitple arguments
      this only lets you send a list of strings
        """
        if first.annotation in (list[str], list):
            return (user_text.splitlines(),)

        # printEx(self, str, ...)
        if first.annotation is str:
            return (user_text,)

        # else just send the text
        return (user_text,)
 
  

        
    
  
 

  