from dataclasses import dataclass
from typing import Type, List
from tabulate import tabulate


class SymbolTableEntry:
    def __init__(self, row: int, lexeme, type: Type) -> None:
        # if not isinstance(lexeme, type):
        #     raise TypeError(
        #         f"Invalid type for the given lexeme. Expected {type}"
        #     )
        
        self.row = row
        self.lexeme = lexeme
        self.type = type

    def to_tuple(self) -> tuple:
        return (self.row, self.lexeme, self.type)
    
class SymbolTable:
    def __init__(self, type: Type) -> None:
        self.entries: List[SymbolTableEntry] = []
        self.type = type

    def __str__(self) -> str:
        return tabulate(
            [entry.to_tuple() for entry in self.entries],
            headers=["Entry #", "Lexeme", "Type"],
            tablefmt="fancy_grid",
        )
    
    def add_entry(self, lexeme: type) -> int:
        """
        Returns the index of the inserted entry
        """
        for i, entry in enumerate(self.entries):
            # Search for an entry with the same lexeme
            if entry.lexeme == lexeme:
                return i

        new_entry = SymbolTableEntry(
            row=len(self.entries), 
            lexeme=lexeme, 
            type=self.type
        )
        self.entries.append(new_entry)

        # Return the index of the new entry
        return len(self.entries) - 1

