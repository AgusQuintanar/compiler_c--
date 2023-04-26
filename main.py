from utils.transition_table import TransitionTable
class TransitionTableScanner:
    def __init__(self, transition_table: TransitionTable) -> None:
        self.transition_table = transition_table
        self.text = "hola como"
        self._last_index = 0

    def _process(self, start_ch_index: int) -> None:
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
        state = self.transition_table.get_initial_state()
        n = len(self.text)
        ch_index = start_ch_index
        print(f"Started with {self.text[ch_index]}")
        while ch_index < n and not (state.is_accepting or state.is_error):
            ch = self.text[ch_index]
            new_state_id = state.get_next_node_index(ch)
            new_state = self.transition_table.get_state(new_state_id)
            if state.can_advance(): # TODO investigate this
                ch_index += 1
            state = new_state

        if state.is_accepting:
            print("Record token")
            print(state.output)
            print(self.text[start_ch_index:ch_index])
        else:
            print("error")
        
        self._last_index = ch_index

    
    def process(self) -> None:
        self._last_index = 0
        while self._last_index < len(self.text):
            self._process(start_ch_index=self._last_index)
        print("done")


if __name__ == "__main__":
    transion_table = TransitionTable.from_excel("transition_table.xlsx")
    scanner = TransitionTableScanner(transion_table)
    scanner.process()
