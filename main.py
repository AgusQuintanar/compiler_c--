from utils.transition_table import TransitionTable, StateBase
from utils.symbol_table import SymbolTable
from utils.constants import IDENTIFIER

class TransitionTableScanner:
    def __init__(self, transition_table: TransitionTable, file_path: str) -> None:
        self.transition_table = transition_table
        with open(file_path, "r") as file:
            self.text = file.read()+"\0"

        self.scanner_output = []
        self.symbol_tables = [
            SymbolTable(int),
            SymbolTable(float),
            SymbolTable(str),
            SymbolTable(IDENTIFIER)
        ]

    def transition(self, state: StateBase, ch: str) -> StateBase:
        new_state_id = state.get_next_node_index(ch)
        return self.transition_table.get_state(new_state_id)
    
    def record_token(self, token: str, token_type: str) -> None:
        ...

    def process(self, start_ch_index: int = 0) -> None:
        """
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
            print("DONE")
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
            print("Record token")
            print(state.output)
            if state.output in ["INT", "FLOAT", "IDENTIFIER", "<", ">", "=", "/"]: 
                ch_index -= 1
            print(f'"{self.text[start_ch_index:ch_index]}"')
        else:
            raise Exception(f"Error: {state.output}")
        
        
        print("-"*10)
        self.process(start_ch_index=ch_index)



if __name__ == "__main__":
    transion_table = TransitionTable.from_excel("transition_table.xlsx")
    scanner = TransitionTableScanner(transion_table, file_path="tests/test2.c--")
    scanner.process()
