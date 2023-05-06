from utils.transition_table import TransitionTable
from utils.scanner import TransitionTableScanner

if __name__ == "__main__":
    # Create a transition table from the excel file
    transion_table = TransitionTable.from_excel("transition_table.xlsx")

    # Create a scanner from the transition table and the input file
    scanner = TransitionTableScanner(
        transion_table, file_path="tests/test1.c--"
    )

    # Process the input file
    scanner.process()

    # Print the scanner output and the symbol tables
    scanner.print_scanner_output()
    print("\n\n")
    scanner.print_formatted_scanner_output()
    print("\n\n")
    scanner.print_symbol_tables()
