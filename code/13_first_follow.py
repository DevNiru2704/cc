def build_grammar():
    return {
        "E": [["T", "E'"]],
        "E'": [["+", "T", "E'"], ["epsilon"]],
        "T": [["F", "T'"]],
        "T'": [["*", "F", "T'"], ["epsilon"]],
        "F": [["(", "E", ")"], ["id"]],
    }

def is_nonterminal(symbol, grammar):
    return symbol in grammar

def first_of_sequence(sequence, grammar, first):
    result = set()
    if sequence == ["epsilon"]:
        result.add("epsilon")
        return result
    for symbol in sequence:
        if not is_nonterminal(symbol, grammar):
            result.add(symbol)
            return result
        result.update(first[symbol] - {"epsilon"})
        if "epsilon" not in first[symbol]:
            return result
    result.add("epsilon")
    return result

def compute_first(grammar):
    first = {nonterminal: set() for nonterminal in grammar}
    changed = True
    while changed:
        changed = False
        for nonterminal, productions in grammar.items():
            for production in productions:
                values = first_of_sequence(production, grammar, first)
                before = len(first[nonterminal])
                first[nonterminal].update(values)
                if len(first[nonterminal]) != before:
                    changed = True
    return first

def compute_follow(grammar, first, start_symbol):
    follow = {nonterminal: set() for nonterminal in grammar}
    follow[start_symbol].add("$")
    changed = True
    while changed:
        changed = False
        for lhs, productions in grammar.items():
            for production in productions:
                for index, symbol in enumerate(production):
                    if not is_nonterminal(symbol, grammar):
                        continue
                    beta = production[index + 1:]
                    if beta:
                        first_beta = first_of_sequence(beta, grammar, first)
                        before = len(follow[symbol])
                        follow[symbol].update(first_beta - {"epsilon"})
                        if len(follow[symbol]) != before:
                            changed = True
                        if "epsilon" in first_beta:
                            before = len(follow[symbol])
                            follow[symbol].update(follow[lhs])
                            if len(follow[symbol]) != before:
                                changed = True
                    else:
                        before = len(follow[symbol])
                        follow[symbol].update(follow[lhs])
                        if len(follow[symbol]) != before:
                            changed = True
    return follow

def print_set_map(title, values):
    print(title)
    for nonterminal in values:
        print(f"{nonterminal}: {sorted(values[nonterminal])}")
    print()

def main():
    grammar = build_grammar()
    start_symbol = next(iter(grammar))
    first = compute_first(grammar)
    follow = compute_follow(grammar, first, start_symbol)
    print("Grammar")
    for lhs, productions in grammar.items():
        for production in productions:
            print(f"{lhs} -> {' '.join(production)}")
    print()
    print_set_map("FIRST", first)
    print_set_map("FOLLOW", follow)

if __name__ == "__main__":
    main()