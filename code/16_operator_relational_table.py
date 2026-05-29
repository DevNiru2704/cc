def build_grammar():
    return {
        "E":[["E","+","T"],["T"]],
        "T":[["T","*","F"],["F"]],
        "F":[["(","E",")"],["id"]]
    }

def is_operator_grammar(grammar):
    for productions in grammar.values():
        for production in productions:

            if production == ["e"] or production == ["ε"]:
                return False

            for i in range(len(production)-1):
                if production[i] in grammar and production[i+1] in grammar:
                    return False

    return True

def terminals_and_nonterminals(grammar):
    nonterminals = list(grammar.keys())
    terminals = []

    for productions in grammar.values():
        for production in productions:
            for symbol in production:
                if symbol not in grammar and symbol not in terminals:
                    terminals.append(symbol)

    terminals.append("$")
    return nonterminals, terminals

def firstvt(grammar):
    result = {nt:set() for nt in grammar}

    changed = True
    while changed:
        changed = False

        for nt, productions in grammar.items():
            for p in productions:

                if p[0] not in grammar:
                    if p[0] not in result[nt]:
                        result[nt].add(p[0])
                        changed = True

                else:
                    if len(p) > 1 and p[1] not in grammar:
                        if p[1] not in result[nt]:
                            result[nt].add(p[1])
                            changed = True

                    for x in result[p[0]]:
                        if x not in result[nt]:
                            result[nt].add(x)
                            changed = True

    return result

def lastvt(grammar):
    result = {nt:set() for nt in grammar}

    changed = True
    while changed:
        changed = False

        for nt, productions in grammar.items():
            for p in productions:

                if p[-1] not in grammar:
                    if p[-1] not in result[nt]:
                        result[nt].add(p[-1])
                        changed = True

                else:
                    if len(p) > 1 and p[-2] not in grammar:
                        if p[-2] not in result[nt]:
                            result[nt].add(p[-2])
                            changed = True

                    for x in result[p[-1]]:
                        if x not in result[nt]:
                            result[nt].add(x)
                            changed = True

    return result

def make_table(terminals):
    return {r:{c:"" for c in terminals} for r in terminals}

def set_relation(table,a,b,rel):

    if table[a][b] == "":
        table[a][b] = rel

    elif table[a][b] != rel:
        table[a][b] = "CONFLICT"

def build_relations(grammar, first_vt, last_vt, terminals):

    table = make_table(terminals)

    for productions in grammar.values():
        for p in productions:

            for i in range(len(p)-1):

                a = p[i]
                b = p[i+1]

                if a not in grammar and b not in grammar:
                    set_relation(table,a,b,"=")

                if a not in grammar and b in grammar:
                    for x in first_vt[b]:
                        set_relation(table,a,x,"<")

                if a in grammar and b not in grammar:
                    for x in last_vt[a]:
                        set_relation(table,x,b,">")

                if i+2 < len(p):
                    c = p[i+2]

                    if a not in grammar and b in grammar and c not in grammar:
                        set_relation(table,a,c,"=")

    start = next(iter(grammar))

    for x in first_vt[start]:
        set_relation(table,"$",x,"<")

    for x in last_vt[start]:
        set_relation(table,x,"$",">")

    set_relation(table,"$","$","=")

    return table

def has_conflict(table):

    for r in table:
        for c in table[r]:
            if table[r][c] == "CONFLICT":
                return True

    return False

def print_table(table, terminals):

    print("\nOperator Precedence Relation Table\n")

    print("\t", end="")
    for t in terminals:
        print(t, end="\t")
    print()

    for r in terminals:

        print(r, end="\t")

        for c in terminals:

            x = table[r][c]

            if x == "":
                x = "-"

            print(x, end="\t")

        print()

grammar = build_grammar()

if not is_operator_grammar(grammar):
    print("Given grammar is not an Operator Grammar")

else:

    first_vt = firstvt(grammar)
    last_vt = lastvt(grammar)

    print("FIRSTVT")
    for k,v in first_vt.items():
        print(k,"=",v)

    print("\nLASTVT")
    for k,v in last_vt.items():
        print(k,"=",v)

    _, terminals = terminals_and_nonterminals(grammar)

    table = build_relations(
        grammar,
        first_vt,
        last_vt,
        terminals
    )

    if has_conflict(table):
        print("\nGrammar is ambiguous")
        print("Operator Precedence Table cannot be constructed")

    else:
        print_table(table, terminals)