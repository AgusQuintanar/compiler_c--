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

from ..scanner import TokenType

def first_plus(tokens):
    return set(tokens)


class Grammar:
    def __init__(self, get_current_token, get_next_token):
        self.get_current_token = get_current_token
        self.get_next_token = get_next_token

    def match_terminal(self, terminal):
        print(f"Matching terminal: {terminal} with {self.get_current_token()}")
        if self.get_current_token() == terminal:
            self.get_next_token()
        else:
            raise Exception("Error in match_terminal")

    def match_type(self, token_type):
        print(f"Matching type: {token_type} with {self.get_current_token().type}")
        if self.get_current_token().type == token_type:
            self.get_next_token()
        else:
            raise Exception("Error in match_type")
        
    

        
    def is_type(self, token, type):
        if token.type == type:
            return True
        return False

    def error(self, e):
        raise Exception(e)

    def program(self):
        print("program()")
        self.declaration_list()
        self.match_terminal("void")
        self.match_type(TokenType.IDENTIFIER)
        self.match_terminal("(")
        self.match_terminal("void")
        self.match_terminal(")")
        self.match_terminal("{")
        self.local_declarations()
        self.statement_list()
        self.match_terminal("return")
        self.match_terminal(";")
        self.match_terminal("}")

    def declaration_list(self):
        print("declaration_list()")
        if self.get_current_token() in first_plus(['void']):
            return
        else:
            self.declaration()
            self.declaration_list()

    def declaration(self):
        print("declaration()")    
        if self.get_current_token() == 'void':
            self.match_terminal("void")
            self.match_type(TokenType.IDENTIFIER)
            self.match_terminal("(")
            self.params()
            self.match_terminal(")")
            self.match_terminal("{")
            self.local_declarations()
            self.statement_list()
            self.match_terminal("}")
        else:
            self.var_specifier()
            self.match_type(TokenType.IDENTIFIER)
            if self.get_current_token() == "(":
                self.match_terminal("(")
                self.params()
                self.match_terminal(")")
                self.match_terminal("{")
                self.local_declarations()
                self.statement_list()
                self.match_terminal("}")
            else:
                 self.var_declaration_prime()

    def var_declaration_prime(self):
        print("var_declaration_prime()")
        if self.get_current_token() == ";":
            self.match_terminal(";")
        elif self.get_current_token() == "[":
            self.match_terminal("[")
            self.match_terminal("int")
            self.match_terminal("]")
            self.match_terminal(";")
        else:
            self.error("Error in var_declaration_prime")

    def var_specifier(self):
        print("var_specifier()")
        if self.get_current_token() == "int":
            self.match_terminal("int")
        elif self.get_current_token() == "float":
            self.match_terminal("float")
        elif self.get_current_token() == "string":
            self.match_terminal("string")
        else:
            self.error("Error in var_specifier")
        
    def fun_specifier(self):
        print("fun_specifier()")
        if self.get_current_token() == "void":
            self.match_terminal("void")
        else:
            self.var_specifier()

    def params(self):
        print("params()")
        if self.get_current_token() == "void":
            self.match_terminal("void")
        else:
            self.var_specifier()
            self.match_type(TokenType.IDENTIFIER)
            self.param_prime()
            self.param_list_prime()

    def param_list_prime(self):
        print("param_list_prime()")
        if self.get_current_token() == ",":
            self.match_terminal(",")
            self.var_specifier()
            self.match_type(TokenType.IDENTIFIER)
            self.param_prime()
            self.param_list_prime()
        elif self.get_current_token() in first_plus([')']):
            return
        else:
            self.error("Error in param_list_prime")

    def param_prime(self):
        print("param_prime()")
        if self.get_current_token() == "[":
            self.match_terminal("[")
            self.match_terminal("]")
        elif self.get_current_token() in first_plus([',', ')']):
            return
        else:
            self.error("Error in param_prime")

    def local_declarations(self):
        print("local_declarations()")
        if self.get_current_token() in first_plus(['{', 'if', 'while', 'return', 'read', 'write', '}']):
            return
        elif self.get_current_token().type in first_plus(TokenType.IDENTIFIER):
            return
        self.var_specifier()
        self.match_type(TokenType.IDENTIFIER)
        self.var_declaration_prime()
        self.local_declarations()

    def statement_list(self):
        print("statement_list()")
        if self.get_current_token() in first_plus(['return', '{']):
            return
        self.statement()
        self.statement_list()

    def statement(self):
        print("statement()")
        if self.get_current_token() == "ID":
            self.match_type(TokenType.IDENTIFIER)
            self.statement_prime()
        elif self.get_current_token() == "{":
            self.match_terminal("{")
            self.local_declarations()
            self.statement_list()
            self.match_terminal("}")
        elif self.get_current_token() == "if":
            self.match_terminal("if")
            self.match_terminal("(")
            self.factor()
            self.term_prime()
            self.arithmetic_expression_prime()
            self.expression_prime()
            self.match_terminal(")")
            self.statement()
            self.selection_stmt_prime()
        elif self.get_current_token() == "while":
            self.match_terminal("while")
            self.match_terminal("(")
            self.factor()
            self.term_prime()
            self.arithmetic_expression_prime()
            self.expression_prime()
            self.match_terminal(")")
            self.statement()
        elif self.get_current_token() == "return":
            self.match_terminal("return")
            self.return_stmt_prime()
        elif self.get_current_token() == "read":
            self.match_terminal("read")
            self.match_type(TokenType.IDENTIFIER)
            self.var_prime()
            self.match_terminal(";")
        elif self.get_current_token() == "write":
            self.match_terminal("write")
            self.factor()
            self.term_prime()
            self.arithmetic_expression_prime()
            self.expression_prime()
            self.match_terminal(";")
        else:
            self.error("Error in statement")

    def statement_prime(self):
        print("statement_prime()")
        if self.is_type(self.get_current_token(), TokenType.IDENTIFIER):
            self.match_type(TokenType.IDENTIFIER)
            self.match_terminal("(")
            self.args()
            self.match_terminal(")")
            self.match_terminal(";")
        else:
            self.var_prime()
            self.match_terminal("=")
            self.assignment_stmt_prime()

    def assignment_stmt_prime(self):
        print("assignment_stmt_prime()")
        if self.is_type(self.get_current_token(), TokenType.STRING):
            self.match_type(TokenType.STRING)
            self.match_terminal(";")
        else:
            self.factor()
            self.term_prime()
            self.arithmetic_expression_prime()
            self.expression_prime()
            self.match_terminal(";")

    def selection_stmt_prime(self):
        print("selection_stmt_prime()")
        if self.get_current_token() == "else":
            self.match_terminal("else")
            self.statement()
        elif self.get_current_token() in first_plus(['{', 'if', 'while', 'return', 'read', 'write']):
            return
        elif self.get_current_token().type in first_plus(TokenType.IDENTIFIER):
            return
        else:
            self.error("Error in selection_stmt_prime")

    def return_stmt_prime(self):
        print("return_stmt_prime()")
        if self.get_current_token() == ";":
            self.match_terminal(";")
        else:
            self.factor()
            self.term_prime()
            self.arithmetic_expression_prime()
            self.expression_prime()
            self.match_terminal(";")

    def output_stmt_prime(self):
        print("output_stmt_prime()")
        if self.is_type(self.get_current_token(), TokenType.STRING):
            self.match_type(TokenType.STRING)
            self.match_terminal(";")
        else:
            self.factor()
            self.term_prime()
            self.arithmetic_expression_prime()
            self.expression_prime()
            self.match_terminal(";")

    def var_prime(self):
        print("var_prime()")
        if self.get_current_token() == "[":
            self.match_terminal("[")
            self.factor()
            self.term_prime()
            self.arithmetic_expression_prime()
            self.expression_prime()
            self.match_terminal("]")
        elif self.get_current_token() in first_plus(['=', ';', '(', ')', ',', '+', '-', '*', '/', '<', '<=', '>', '>=', '==', '!=', ']']):
            return
        elif self.get_current_token().type in first_plus(TokenType.IDENTIFIER, TokenType.INT, TokenType.FLOAT):
            return
        else:
            self.error("Error in var_prime")

    def expression_prime(self):
        print("expression_prime()")
        if self.get_current_token() in first_plus([';', ')']):
            return
        self.relop()
        self.factor()
        self.term_prime()
        self.arithmetic_expression_prime()

    def relop(self):
        print("relop()")
        if self.get_current_token() == "<":
            self.match_terminal("<")
        elif self.get_current_token() == "<=":
            self.match_terminal("<=")
        elif self.get_current_token() == ">":
            self.match_terminal(">")
        elif self.get_current_token() == ">=":
            self.match_terminal(">=")
        elif self.get_current_token() == "==":
            self.match_terminal("==")
        elif self.get_current_token() == "!=":
            self.match_terminal("!=")
        else:
            self.error("Error in relop")

    def arithmetic_expression_prime(self):
        print("arithmetic_expression_prime()")
        if self.get_current_token() in first_plus(['=', ';', '(', ')', ',', '*', '/', '<', '<=', '>', '>=', '==', '!=', ']']):
            return
        elif self.get_current_token().type in first_plus(TokenType.IDENTIFIER, TokenType.INT, TokenType.FLOAT):
            return
        
        self.addop()
        self.factor()
        self.term_prime()
        self.arithmetic_expression_prime()

    def addop(self):
        print("addop()")
        if self.get_current_token() == "+":
            self.match_terminal("+")
        elif self.get_current_token() == "-":
            self.match_terminal("-")
        else:
            self.error("Error in addop")

    def factor(self):
        print("factor()")
        if self.get_current_token() == "(":
            self.match_terminal("(")
            self.factor()
            self.term_prime()
            self.arithmetic_expression_prime()
            self.match_terminal(")")
        elif self.is_type(self.get_current_token(), TokenType.IDENTIFIER):
            self.match_type(TokenType.IDENTIFIER)
            self.factor_prime()
        elif self.is_type(self.get_current_token(), TokenType.INT):
            self.match_type(TokenType.INT)
        elif self.is_type(self.get_current_token(), TokenType.FLOAT):
            self.match_type(TokenType.FLOAT)
        else:
            self.error("Error in factor")
    
    def factor_prime(self):
        print("factor_prime()")
        if self.is_type(self.get_current_token(), TokenType.IDENTIFIER):
            self.match_type(TokenType.IDENTIFIER)
            self.match_terminal("(")
            self.args()
            self.match_terminal(")")
            self.match_terminal(";")
        else:
            self.var_prime()
    
    def term_prime(self):
        print("term_prime()")
        if self.get_current_token() in first_plus(['=', ';', '(', ')', ',', '+', '-', '<', '<=', '>', '>=', '==', '!=', ']']):
            return
        elif self.get_current_token().type in first_plus(TokenType.IDENTIFIER, TokenType.INT, TokenType.FLOAT):
            return
        self.mulop()
        self.factor()
        self.term_prime()


    def mulop(self):
        print("mulop()")
        if self.get_current_token() == "*":
            self.match_terminal("*")
        elif self.get_current_token() == "/":
            self.match_terminal("/")
        else:
            self.error("Error in mulop")

    def args(self):
        print("args()")
        if self.get_current_token() in first_plus([')']):
            return
        self.factor()
        self.term_prime()
        self.arithmetic_expression_prime()
        self.args_list_prime()

    def args_list_prime(self):
        print("args_list_prime()")
        if self.get_current_token() == ",":
            self.match_terminal(",")
            self.factor()
            self.term_prime()
            self.arithmetic_expression_prime()
            self.args_list_prime()
        elif self.get_current_token() in first_plus([')']):
            return
        else:
            self.error("Error in args_list_prime")
