from utils.transition_table import TransitionTable, StateBase
from utils.symbol_table import SymbolTable
from utils.constants import IDENTIFIER, RESERVED_KEYWORDS, COMMENT
from utils.utils import get_token_name, get_token_id
from tabulate import tabulate

class TransitionTableScanner:
    def __init__(self, transition_table: TransitionTable, file_path: str) -> None:
        self.transition_table = transition_table
        with open(file_path, "r") as file:
            self.text = file.read()+"\0"

        self.scanner_output = []
        self.symbol_tables = {
            "IDENTIFIER": SymbolTable(IDENTIFIER),
            "INT_CONSTANT": SymbolTable(int),
            "FLOAT_CONSTANT": SymbolTable(float),
            "STRING_CONSTANT": SymbolTable(str),
            "COMMENT": SymbolTable(COMMENT)
        }

    def transition(self, state: StateBase, ch: str) -> StateBase:
        """
        Performs a transition from the given state to the next state based on the given input character.
        """
        new_state_id = state.get_next_node_index(ch)
        return self.transition_table.get_state(new_state_id)

    def _get_token_output(self, token: str, token_type: str):
        """
        Returns the output of the token based on the token type.
        """
        if token_type == "IDENTIFIER":
            if token.upper() in RESERVED_KEYWORDS:
                return [get_token_id(token.upper())]

        if token_type in ["INT_CONSTANT", "STRING_CONSTANT", "COMMENT", "FLOAT_CONSTANT", "IDENTIFIER"]:
            symbol_table_id = get_token_id(token_type)
            symbol_table_entry_idx = self.symbol_tables[token_type].add_entry(
                token)
            return [symbol_table_id, symbol_table_entry_idx]

        return [get_token_id(token_type)]

    def record_token(self, token: str, token_type: str) -> None:
        """
        Records the token in the scanner output.
        """
        token = self._get_token_output(token, token_type)
        self.scanner_output.append(token)

    def process(self, start_ch_index: int = 0) -> None:
        """
        Processes the input text and generates the scanner output.

        Pseudocode:
            state = 0; /* start */
            ch = next input character;
            while (!Accept[state] && !Error[state] ) {
                newState = T[state, ch]; 
                if (Advance[state, ch])
                    ch = next input character ;
                state = newState;
            } /* end while */ 
            if (Accept[state] )
                RecordToken; 
            else
                error;
        """
        n = len(self.text)
        ch_index = start_ch_index

        if ch_index >= n:
            # End of file reached
            return

        state = self.transition_table.get_initial_state()

        while not (state.is_accepting or state.is_error):
            ch = self.text[ch_index]
            new_state = self.transition(state, ch)

            if new_state._id == 0:
                return self.process(start_ch_index=ch_index+1)

            if state.can_advance():
                ch_index += 1

            state = new_state

        if state.is_accepting:
            # If the output is in the following list, we need to go back one character, 
            # to make sure that the next token is not affected
            if state.output in ["INT_CONSTANT", "FLOAT_CONSTANT", "IDENTIFIER", "<", ">", "=", "/"]:
                ch_index -= 1

            token = self.text[start_ch_index:ch_index]
            self.record_token(token=token, token_type=state.output)
        else:
            raise Exception(f"Error: {state.output}")

        self.process(start_ch_index=ch_index)

    def _get_token_recognition(self, output_entry: list) -> str:
        if len(output_entry) == 1:
            return get_token_name(token_id=output_entry[0])
        elif len(output_entry) == 2:
            token_id, token_entry_idx = output_entry
            token_name = get_token_name(token_id)
            return self.symbol_tables[token_name].entries[token_entry_idx]
        else:
            raise Exception("Invalid output entry")

    def print_scanner_output(self):
        """
        Prints the scanner output.
        In the following format:
            <token_id, token_entry_idx>
            <token_id>
            [...]
        """
        print("Scanner Output:")
        for output_entry in self.scanner_output:
            str_entry = ", ".join(
                [str(entry) for entry in output_entry]
            )
            print(f"<{str_entry}>")

    def print_formatted_scanner_output(self):
        """
        Prints the scanner output in a formatted table.
        In the following format:
            Scanner Output              | Token Recognition
            ------------------------------------------------
            <token_id, token_entry_idx> | <token_name>
            <token_id>                  | <token_name>
            [...]
        """
        print("Formatted Scanner Output:")

        formatted_output = tabulate(
            [[output_entry, self._get_token_recognition(
                output_entry)] for output_entry in self.scanner_output],
            headers=["Scanner Output", "Token Recognition"],
            tablefmt="fancy_grid",
        )

        print(formatted_output)

    def print_symbol_tables(self):
        """
        Prints the symbol tables.
        """
        for symbol_table_name, symbol_table in self.symbol_tables.items():
            print(f"Symbol Table: {symbol_table_name}")
            print(symbol_table)
            print()
