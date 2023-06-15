"""
1. program → declaration_list void IDENTIFIER (void) {local_declarations statement_list return ;}
2. declaration_list → declaration declaration_list | Ɛ
3. declaration → var_specifier ID var_declaration' | fun_specifier ID ( params ) { local_declarations statement_list }
4. var_declaration' → ; | [ INT ] ;
5. var_specifier → int | float | string
6. fun_specifier → var_specifier | void
7 params → var_specifier ID param' param_list' | void
8. param_list' → , var_specifier ID param' param_list' | Ɛ
9. param' → Ɛ | [ ]
10. local_declarations → var_specifier ID var_declaration' local_declarations | Ɛ
11. statement_list → statement statement_list | Ɛ
12. statement →  ID statement'
| { local_declarations statement_list }
| if (  factor term' arithmetic_expression'  expression' ) statement selection_stmt' 
| while (  factor term' arithmetic_expression'  expression' ) statement
| return return_stmt' 
| read  ID var' ;
| write  factor term' arithmetic_expression'  expression' ;

13. statement' → var' = assignment_stmt' | ID ( args ) ;
14. assignment_stmt' → factor term' arithmetic_expression' expression' ; | STRING ;
15. selection_stmt' → Ɛ | else statement
16. return_stmt' → ; | factor term' arithmetic_expression' expression' ;
17. output_stmt'  →  factor term' arithmetic_expression'  expression'  ; | STRING ; 
18. var' → Ɛ | [ factor term' arithmetic_expression' ]
19. expression' → relop factor term' arithmetic_expression' | Ɛ
20. relop → <= | < | > | >= | == | !=
21. arithmetic_expression' → addop factor term' arithmetic_expression' | Ɛ
22. addop → + | -
23. factor → ( factor term' arithmetic_expression' ) | ID factor' | INT | FLOAT
24. factor' → var' | ID ( args ) ;
25. term' → mulop factor term' | Ɛ
26. mulop → * | /
27. args → factor term' arithmetic_expression' args_list' | Ɛ
28. args_list' = , factor term' arithmetic_expression' args_list' | Ɛ
"""

from enum import Enum

def match_terminal(terminal):
    ...

def match_type(type):
    ...

class TokenType(Enum):
    IDENTIFIER = 1
    INT = 2
    FLOAT = 3
    STRING = 4


current_token = "a"

def get_next_token():
    global current_token
    return current_token



def is_type(token, type: TokenType):
    if token.type == type:
        return True
    return False



def program():
    declaration_list()
    match_terminal("void")
    match_type(TokenType.IDENTIFIER)
    match_terminal("(")
    match_terminal("void")
    match_terminal(")")
    match_terminal("{")
    local_declarations()
    statement_list()
    match_terminal("return")
    match_terminal(";")
    match_terminal("}")

def declaration_list():
    declaration()
    declaration_list()

def error(e):
    print(e)

def declaration():
    if current_token == 'void':
        match_terminal("void")
        match_type(TokenType.IDENTIFIER)
        match_terminal("(")
        params()
        match_terminal(")")
        match_terminal("{")
        local_declarations()
        statement_list()
        match_terminal("}")
    else:
        var_specifier()
        match_type(TokenType.IDENTIFIER)
        if current_token == "(":
            match_terminal("(")
            params()
            match_terminal(")")
            match_terminal("{")
            local_declarations()
            statement_list()
            match_terminal("}")
        else:
             var_declaration_prime()

def var_declaration_prime():
    if current_token == ";":
        match_terminal(";")
    elif current_token == "[":
        match_terminal("[")
        match_terminal("int")
        match_terminal("]")
        match_terminal(";")
    else:
        error("Error in var_declaration_prime")

def var_specifier():
    if current_token == "int":
        match_terminal("int")
    elif current_token == "float":
        match_terminal("float")
    elif current_token == "string":
        match_terminal("string")
    else:
        error("Error in var_specifier")
        
def fun_specifier():
    if current_token == "void":
        match_terminal("void")
    else:
        var_specifier()

def params():
    if current_token == "void":
        match_terminal("void")
    else:
        var_specifier()
        match_type(TokenType.IDENTIFIER)
        param_prime()
        param_list_prime()

def param_list_prime():
    if current_token == ",":
        match_terminal(",")
        var_specifier()
        match_type(TokenType.IDENTIFIER)
        param_prime()
        param_list_prime()
    else:
        error("Error in param_list_prime")

def param_prime():
    if current_token == "[":
        match_terminal("[")
        match_terminal("]")
    else:
        error("Error in param_prime")

def local_declarations():
    var_specifier()
    match_type(TokenType.IDENTIFIER)
    var_declaration_prime()
    local_declarations()

def statement_list():
    statement()
    statement_list()

def statement():
    if current_token == "ID":
        match_type(TokenType.IDENTIFIER)
        statement_prime()
    elif current_token == "{":
        match_terminal("{")
        local_declarations()
        statement_list()
        match_terminal("}")
    elif current_token == "if":
        match_terminal("if")
        match_terminal("(")
        factor()
        term_prime()
        arithmetic_expression_prime()
        expression_prime()
        match_terminal(")")
        statement()
        selection_stmt_prime()
    elif current_token == "while":
        match_terminal("while")
        match_terminal("(")
        factor()
        term_prime()
        arithmetic_expression_prime()
        expression_prime()
        match_terminal(")")
        statement()
    elif current_token == "return":
        match_terminal("return")
        return_stmt_prime()
    elif current_token == "read":
        match_terminal("read")
        match_type(TokenType.IDENTIFIER)
        var_prime()
        match_terminal(";")
    elif current_token == "write":
        match_terminal("write")
        factor()
        term_prime()
        arithmetic_expression_prime()
        expression_prime()
        match_terminal(";")
    else:
        error("Error in statement")

def statement_prime():
    if is_type(current_token, TokenType.IDENTIFIER):
        match_type(TokenType.IDENTIFIER)
        match_terminal("(")
        args()
        match_terminal(")")
        match_terminal(";")
    else:
        var_prime()
        match_terminal("=")
        assignment_stmt_prime()

def assignment_stmt_prime():
    if is_type(current_token, TokenType.STRING):
        match_type(TokenType.STRING)
        match_terminal(";")
    else:
        factor()
        term_prime()
        arithmetic_expression_prime()
        expression_prime()
        match_terminal(";")

def selection_stmt_prime():
    if current_token == "else":
        match_terminal("else")
        statement()
    else:
        error("Error in selection_stmt_prime")

def return_stmt_prime():
    if current_token == ";":
        match_terminal(";")
    else:
        factor()
        term_prime()
        arithmetic_expression_prime()
        expression_prime()
        match_terminal(";")

def output_stmt_prime():
    if is_type(current_token, TokenType.STRING):
        match_type(TokenType.STRING)
        match_terminal(";")
    else:
        factor()
        term_prime()
        arithmetic_expression_prime()
        expression_prime()
        match_terminal(";")

def var_prime():
    if current_token == "[":
        match_terminal("[")
        factor()
        term_prime()
        arithmetic_expression_prime()
        expression_prime()
        match_terminal("]")
    else:
        error("Error in var_prime")

def expression_prime():
    relop()
    factor()
    term_prime()
    arithmetic_expression_prime()

def relop():
    if current_token == "<":
        match_terminal("<")
    elif current_token == "<=":
        match_terminal("<=")
    elif current_token == ">":
        match_terminal(">")
    elif current_token == ">=":
        match_terminal(">=")
    elif current_token == "==":
        match_terminal("==")
    elif current_token == "!=":
        match_terminal("!=")
    else:
        error("Error in relop")

def arithmetic_expression_prime():
    addop()
    factor()
    term_prime()
    arithmetic_expression_prime()

def addop():
    if current_token == "+":
        match_terminal("+")
    elif current_token == "-":
        match_terminal("-")
    else:
        error("Error in addop")

def factor():
    if current_token == "(":
        match_terminal("(")
        factor()
        term_prime()
        arithmetic_expression_prime()
        match_terminal(")")
    elif is_type(current_token, TokenType.IDENTIFIER):
        match_type(TokenType.IDENTIFIER)
        factor_prime()
    elif is_type(current_token, TokenType.INT):
        match_type(TokenType.INT)
    elif is_type(current_token, TokenType.FLOAT):
        match_type(TokenType.FLOAT)
    else:
        error("Error in factor")
    
def factor_prime():
    if is_type(current_token, TokenType.IDENTIFIER):
        match_type(TokenType.IDENTIFIER)
        match_terminal("(")
        args()
        match_terminal(")")
        match_terminal(";")
    else:
        var_prime()
    
def term_prime():
    mulop()
    factor()
    term_prime()


def mulop():
    if current_token == "*":
        match_terminal("*")
    elif current_token == "/":
        match_terminal("/")
    else:
        error("Error in mulop")

def args():
    factor()
    term_prime()
    arithmetic_expression_prime()
    args_list_prime()

def args_list_prime():
    if current_token == ",":
        match_terminal(",")
        factor()
        term_prime()
        arithmetic_expression_prime()
        args_list_prime()
    else:
        error("Error in args_list_prime")