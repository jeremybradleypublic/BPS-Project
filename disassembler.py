
from types import MappingProxyType
from typing import Protocol, Mapping, Callable, cast
from utils import cmd



class RuntimeBound(Protocol):
    __vslots__: Mapping[str, int] ##variable vtable index
    __vtable__: Mapping[int, Callable] #vtable 
    __jump__: Mapping[int, Callable] #jmp call table





def input_into_py(user_code):
    return compile(user_code, "<user_input>", "exec")

def code_to_bytes(compiled):
    return compiled.co_code


def build_slot_layout(cls):
    slots: dict[str, int] = {} # creating a map
    for base in reversed(cls.__mro__): # reversed mro (Method Resolution Order), a class hiearchy  
        for name, member in base.__dict__.items(): #iterate over memebers of the class
            if callable(member) and not name.startswith("__"): #looking for anything callable, not direct varabiles like cached_phrases
                if name not in slots:
                    slots[name] = len(slots) #cache slots 
    return MappingProxyType(slots) # makes slot read only


def build_vtable(cls, slots): #shadow / somewhat copy vtable, but more bare bones
    table: dict[int, Callable] = {}
    for base in reversed(cls.__mro__):
        for name, member in base.__dict__.items():
            if callable(member) and name in slots:
                table[slots[name]] = member
    return MappingProxyType(table) #makes vtable read only


def build_jump_table(instance, vtable):
    return MappingProxyType({ ##binds the vtable to the instance
        slot: getattr(instance, func.__name__)
        for slot, func in vtable.items()
    }) #makes read only




def bind_runtime(instance) -> RuntimeBound:
    slots = build_slot_layout(type(instance))
    vtable = build_vtable(type(instance), slots)
    jump = build_jump_table(instance, vtable)

    instance.__vslots__ = slots
    instance.__vtable__ = vtable
    instance.__jump__ = jump

    return cast(RuntimeBound, instance)

fe : RuntimeBound  
def init():
    global fe
    fe = bind_runtime(cmd.frontend())

def get_via_vtable( name):
    index = fe.__vslots__[name]
    return fe.__jump__[index]

def vcall_slot(frontend_instance, name: str, user_text: str):
    target = get_via_vtable(name)
    args = frontend_instance().normalize_user_args(target, user_text)
    return target(*args)



def dump_object(frontend_instance ):
    frontend_instance().send([f"  instance @ 0x{id(fe):x}"])
    
def dump_slots(frontend_instance):
    for name, slot in fe.__vslots__.items():
        frontend_instance().collect_cache(f"  {slot:02} -> {name}")
    frontend_instance().send_cache()

def dump_virtual_and_jump_table(frontend_instance):
   
    frontend_instance().send([f"vtable @ 0x{id(fe.__vtable__):x}"])

    for slot, func in fe.__vtable__.items():
        frontend_instance().collect_cache(
            f"[{slot:02}] +0x{(id(func) - id(fe.__vtable__)):x} {func.__name__}"
        )
    frontend_instance().send_cache()

  ## jump (dispatch targets) NOT to be confused jmps instrunctions 
    cls_name = type(fe).__name__
    frontend_instance().send(["jump table (dispatch targets)"])

    for slot, bound in fe.__jump__.items():
        target = getattr(bound, "__func__", bound)
        frontend_instance().collect_cache(
            f"{cls_name}[slot:{slot:02}] "
            f"callable @ 0x{id(bound):x} -> {target.__name__}"
        )

    frontend_instance().send_cache()



   
def send_call(frontend_instance, name : str, varaibles):
    return vcall_slot(frontend_instance, name, varaibles)
    


