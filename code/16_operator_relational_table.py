def build_grammar():
    return {
        "E":[["E","+","E"],["E","*","E"],["(","E",")"],["id"]]
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

                first = p[0]

                if first not in grammar:

                    if first not in result[nt]:
                        result[nt].add(first)
                        changed = True

                else:

                    if len(p) > 1:

                        second = p[1]

                        if second not in grammar:

                            if second not in result[nt]:
                                result[nt].add(second)
                                changed = True

                    for x in result[first]:

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

                last = p[-1]

                if last not in grammar:

                    if last not in result[nt]:
                        result[nt].add(last)
                        changed = True

                else:

                    if len(p) > 1:

                        before = p[-2]

                        if before not in grammar:

                            if before not in result[nt]:
                                result[nt].add(before)
                                changed = True

                    for x in result[last]:

                        if x not in result[nt]:
                            result[nt].add(x)
                            changed = True

    return result

def make_table(terminals):

    return {
        row:{col:"" for col in terminals}
        for row in terminals
    }

def set_relation(table, a, b, rel):

    current = table[a][b]

    if current == "":
        table[a][b] = rel

    elif rel not in current:
        table[a][b] += rel

def build_relations(grammar, first_vt, last_vt, terminals):

    table = make_table(terminals)

    for productions in grammar.values():

        for p in productions:

            for i in range(len(p)-1):

                left = p[i]
                right = p[i+1]

                if left not in grammar and right not in grammar:
                    set_relation(table,left,right,"=")

                if left not in grammar and right in grammar:

                    for x in first_vt[right]:
                        set_relation(table,left,x,"<")

                if left in grammar and right not in grammar:

                    for x in last_vt[left]:
                        set_relation(table,x,right,">")

                if i+2 < len(p):

                    middle = p[i+1]
                    last = p[i+2]

                    if left not in grammar and middle in grammar and last not in grammar:
                        set_relation(table,left,last,"=")

    start = next(iter(grammar))

    for x in first_vt[start]:
        set_relation(table,"$",x,"<")

    for x in last_vt[start]:
        set_relation(table,x,"$",">")

    set_relation(table,"$","$","=")

    return table

def print_table(table, terminals):

    print("\nOperator Precedence Relation Table\n")

    print("\t", end="")

    for t in terminals:
        print(t, end="\t")

    print()

    for row in terminals:

        print(row, end="\t")

        for col in terminals:

            value = table[row][col]

            if value == "":
                value = "-"

            print(value, end="\t")

        print()

def main():

    grammar = build_grammar()

    if not is_operator_grammar(grammar):

        print("Given grammar is not an Operator Grammar")
        return

    first_vt = firstvt(grammar)
    last_vt = lastvt(grammar)

    print("FIRSTVT")

    for nt, values in first_vt.items():
        print(nt, "=", sorted(values))

    print("\nLASTVT")

    for nt, values in last_vt.items():
        print(nt, "=", sorted(values))

    _, terminals = terminals_and_nonterminals(grammar)

    table = build_relations(
        grammar,
        first_vt,
        last_vt,
        terminals
    )

    print_table(table, terminals)

if __name__ == "__main__":
    main()