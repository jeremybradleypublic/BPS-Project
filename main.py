import disassembler
import dis
import sys 
from utils import cmd, text_style, Color






frontend = cmd().frontend

compiled_code = 0
change_color = False
#loop to project the option screen until user quites the program 
while True:
    frontend().cls() #clears the previous screen for the user to be able to pick a new option
    if not change_color:
        frontend().SetForeColor(Color.BRIGHT_RED)

    ##ascii font using patorjk
    frontend().send(["""
██████╗ ██████╗ ███████╗     █████╗ ███████╗███╗   ███╗      ███████╗████████╗ █████╗ ██████╗ ████████╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔════╝████╗ ████║      ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██████╔╝██████╔╝███████╗    ███████║███████╗██╔████╔██║█████╗███████╗   ██║   ███████║██████╔╝   ██║   █████╗  ██████╔╝
██╔══██╗██╔═══╝ ╚════██║    ██╔══██║╚════██║██║╚██╔╝██║╚════╝╚════██║   ██║   ██╔══██║██╔══██╗   ██║   ██╔══╝  ██╔══██╗
██████╔╝██║     ███████║    ██║  ██║███████║██║ ╚═╝ ██║      ███████║   ██║   ██║  ██║██║  ██║   ██║   ███████╗██║  ██║
╚═════╝ ╚═╝     ╚══════╝    ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝      ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
"""])
    if not change_color:
        frontend().SetForeColor(Color.BRIGHT_WHITE)
    frontend().SetPrintStyle(text_style.TYPED)
    frontend().send(["by Jeremy Arsney and Calum "], True) # centered text
    if not change_color:
        frontend().SetForeColor(Color.RED)
    frontend().SetPrintStyle(text_style.REGULAR)

    frontend().send([
        """
[1] Run and Dissasemble Your Code   [4] Displays object and slots
[2]  Display Your Byte Code         [5] Displays vtables and jmps 
[3] Color                           [6] Call via Vtable 

                        [7 Exit]
"""
    ])
    
    disassembler.init() ##inits the fe, which is vital for all dissesmbler calls

    switch = int(input(">"))
    
    frontend().cls()

    frontend().SetPrintStyle(text_style.TYPED)
    frontend().send([f"You picked option {str(switch)}\n"])
    
    frontend().SetPrintStyle(text_style.REGULAR)

    match switch: ## switch case 
        case 1:
            frontend().send(["Enter Python code. Press ENTER on an empty line to compile.\n"])
            user_code = frontend().get_inputs(">>>")
            compiled_code = disassembler.input_into_py(user_code)
            dis.dis(compiled_code) #returns code in a psuedocode manner
           
        

        case 2:
            if compiled_code: 
                byte_values = list(disassembler.code_to_bytes(compiled_code))
                frontend().send(["\n--- BYTECODE (hex) ---"])
                frontend().send([str(" ".join(f"0x{b:02x}" for b in byte_values))])
            else:
                print("please run and dissasemble your code first")
            frontend().pause()
            

        case 3:
            ##Todo , make a whole nother page / menu for this
            # letting user change more than just color
            ## prolly change to letter instead number
            frontend().send(["This lets you change the color of the ForeGround text\n",
            "please enter the number of the color you want\n", 
            """
               RESSET_TO_DEFAULT = 0 
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
            """])
            change_color = True
            color_id = int(input(">"))
            if color_id == 0:
                change_color = False
            else: 
                current_color = Color(color_id)
                frontend().SetForeColor(current_color)
            

        case 4:
            disassembler.dump_object(frontend)
            disassembler.dump_slots(frontend)
            

        case 5:
            disassembler.dump_virtual_and_jump_table(frontend)
            frontend().pause()
           

        case 6:
            frontend().send(["Please enter the name of the function you want to call",
            """
            class text_style(Enum):
                REGULAR = 1
                TYPED = 2
               ## BLINK = 3
                ENCRYPTED = 3
                DECRYPTED = 4
                CACHED = 5
                BUFFER = 6

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
              
            cmd: # todo enter the input varaibles needed
                frontend:
                    def center
                    def printEx
                    def pause
                    def SetPrintStyle
                    def SetForeColor
                    def send
                    def collect_cache
                    def cls
                    def send_cache
                    def trash_cache
                    
            """])
            func_str = str(input(" "))
            frontend().send([f"\n Found {func_str} at @ 0x{id(disassembler.get_via_vtable(func_str)):x}"])
            frontend().send(["Please enter each input"]) 
            inputs = (frontend().get_inputs(">>>"))
            disassembler.send_call(frontend,func_str, inputs)   
            frontend().pause()
           

        case 7:
            sys.exit(0)
        case _:
            frontend().send(["\nplease pick a valid option "])
    

