from dataclasses import dataclass
from typing import Type, List
from abc import ABCMeta, abstractproperty
from tabulate import tabulate


class SymbolTableEntry:
    def __init__(self, row: int, lexeme, type: Type) -> None:
        if not isinstance(lexeme, type):
            raise TypeError(
                f"Invalid type for the given lexeme. Expected {type}"
            )
        
        self.row = row
        self.lexeme = lexeme
        self.type = type

    def to_tuple(self) -> tuple:
        return (self.row, self.lexeme, self.type)
    
class SymbolTableBase(metaclass=ABCMeta):
    @abstractproperty
    def type(self) -> Type:
        ...

    def __init__(self) -> None:
        self.entries: List[SymbolTableEntry] = []

    def __str__(self) -> str:
        return tabulate(
            [entry.to_tuple() for entry in self.entries],
            headers=["Entry #", "Lexeme", "Type"],
            tablefmt="fancy_grid",
        )
    
    def add_entry(self, lexeme: type):
        new_entry = SymbolTableEntry(
            row=len(self.entries), 
            lexeme=lexeme, 
            type=self.type
        )
        self.entries.append(new_entry)


    

class IntegerSymbolTable(SymbolTableBase):
    @property
    def type(self) -> Type:
        return int

class StringSymbolTable(SymbolTableBase):
    @property
    def type(self) -> Type:
        return str


a = IntegerSymbolTable()
a.add_entry(
    3
)
a.add_entry(45)
print(a)