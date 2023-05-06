from typing import List, Dict, Optional
from abc import ABCMeta, abstractproperty
import pandas as pd
from enum import Enum
from collections import OrderedDict
from tabulate import tabulate
from .constants import azAZ, DIGITS, EOF, BLANK_DELIMITERS

TRANSITION_VECTOR = OrderedDict(
    [
        ["LETTER", lambda x: x in azAZ],
        ["DIGIT", lambda x: x in DIGITS],
        ["+", lambda x: x == "+"],
        ["-", lambda x: x == "-"],
        ["*", lambda x: x == "*"],
        ["/", lambda x: x == "/"],
        ["=", lambda x: x == "="],
        ["!", lambda x: x == "!"],
        [";", lambda x: x == ";"],
        [",", lambda x: x == ","],
        ['"', lambda x: x == '"'],
        [".", lambda x: x == "."],
        ["(", lambda x: x == "("],
        [")", lambda x: x == ")"],
        ["[", lambda x: x == "["],
        ["]", lambda x: x == "]"],
        ["{", lambda x: x == "{"],
        ["}", lambda x: x == "}"],
        ["<", lambda x: x == "<"],
        [">", lambda x: x == ">"],
        ["BLANK", lambda x: x in BLANK_DELIMITERS],
        ["EOF", lambda x: x == EOF],
        ["RARE", lambda _x: True],
    ]
)


class InputCharVector(OrderedDict):
    def __init__(
        self, input_chars: Dict[str, Optional[int]], transion_vector: OrderedDict
    ) -> None:
        self._validate(input_chars, transion_vector)
        for key, value in input_chars.items():
            self[key] = value

        self.transition_vector = transion_vector

    def _validate(
        self, input_chars: Dict[str, Optional[int]], transion_vector: OrderedDict
    ) -> None:
        if sorted(input_chars.keys()) != sorted(transion_vector.keys()):
            raise ValueError(
                "Input chars and transition vector are not compatible")


class StateType(str, Enum):
    ACCEPTING = "ACCEPTING"
    ERROR = "ERROR"
    TRANSITION = "TRANSITION"


class StateBase(metaclass=ABCMeta):
    def __init__(
        self, _id: int, input_char_vector: InputCharVector, output=None
    ) -> None:
        self._id = _id
        self.input_char_vector = input_char_vector
        self.output = output

    @abstractproperty
    def is_accepting(self) -> bool:
        ...

    @abstractproperty
    def is_error(self) -> bool:
        ...

    @abstractproperty
    def type(self) -> StateType:
        ...

    def to_dict(self) -> OrderedDict:
        _d = OrderedDict()
        _d["_TYPE"] = self.type
        _d["_STATE_ID"] = self._id
        _d["_OUTPUT"] = self.output
        for key, value in self.input_char_vector.items():
            _d[key] = value
        return _d

    def can_advance(self) -> bool:
        return False

    def __str__(self) -> str:
        return str(self.to_dict())

    def get_next_node_index(self, char: str) -> Optional[int]:
        for (
            input_char,
            is_input_char,
        ) in self.input_char_vector.transition_vector.items():
            if is_input_char(char):
                return self.input_char_vector[input_char]


class AcceptingState(StateBase):
    @property
    def is_accepting(self) -> bool:
        return True

    @property
    def is_error(self) -> bool:
        return False

    @property
    def type(self) -> StateType:
        return StateType.ACCEPTING


class ErrorState(StateBase):
    @property
    def is_accepting(self) -> bool:
        return False

    @property
    def is_error(self) -> bool:
        return True

    @property
    def type(self) -> StateType:
        return StateType.ERROR


class TransitionState(StateBase):
    @property
    def is_accepting(self) -> bool:
        return False

    @property
    def is_error(self) -> bool:
        return False

    def can_advance(self) -> bool:
        return True

    @property
    def type(self) -> StateType:
        return StateType.TRANSITION


class TransitionTable:
    def __init__(self, states: List[StateBase]) -> None:
        self.states = states

    def generate_state(
        self,
        state_type: StateType,
        state_id: int,
        input_chars: Dict[str, Optional[int]],
        output=None,
    ) -> StateBase:
        input_char_vector = InputCharVector(input_chars, TRANSITION_VECTOR)

        if state_type == StateType.ACCEPTING:
            state = AcceptingState(state_id, input_char_vector, output)
        elif state_type == StateType.ERROR:
            state = ErrorState(state_id, input_char_vector, output)
        elif state_type == StateType.TRANSITION:
            state = TransitionState(state_id, input_char_vector, output)
        else:
            raise ValueError(f"Invalid state type: {state_type}")

        return state

    def add_state(self, state_type: StateType, state_id: int, output=None) -> None:
        state = self.generate_state(state_type, state_id, output)
        self.states.append(state)

    def get_initial_state(self) -> StateBase:
        for state in self.states:
            if state._id == 0:
                return state
        raise ValueError("No initial state found")

    def get_state(self, state_id: int) -> StateBase:
        for state in self.states:
            if state._id == state_id:
                return state
        raise ValueError(f"No state with id {state_id} found")
    
    @classmethod
    def from_dataframe(cls, dataframe: pd.DataFrame) -> "TransitionTable":
        states = []
        for _, row in dataframe.iterrows():
            state_type = row.get("_TYPE")
            state_id = row.get("_STATE_ID")
            output = row.get("_OUTPUT")
            input_chars = row.drop(["_TYPE", "_STATE_ID", "_OUTPUT"]).to_dict()

            state = cls.generate_state(
                cls, state_type, state_id, input_chars, output)
            states.append(state)
        return cls(states)

    @classmethod
    def from_csv(cls, path: str) -> "TransitionTable":
        dataframe = pd.read_csv(path)
        return cls.from_dataframe(dataframe)

    @classmethod
    def from_excel(cls, path: str) -> "TransitionTable":
        dataframe = pd.read_excel(path)
        return cls.from_dataframe(dataframe)

    def __str__(self):
        return tabulate(
            [state.to_dict() for state in self.states],
            headers="keys",
            tablefmt="fancy_grid",
        )
