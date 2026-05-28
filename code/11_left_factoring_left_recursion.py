def print_grammar(title, grammar):
    print(title)
    for nonterminal, productions in grammar.items():
        parts = [" ".join(production) for production in productions]
        print(f"{nonterminal} -> {' | '.join(parts)}")
    print()

def eliminate_left_recursion(grammar):
    updated = {}
    for nonterminal, productions in grammar.items():
        recursive = []
        non_recursive = []
        for production in productions:
            if production and production[0] == nonterminal:
                recursive.append(production[1:])
            else:
                non_recursive.append(production)
        if recursive:
            new_nonterminal = nonterminal + "'"
            updated[nonterminal] = []
            for production in non_recursive:
                updated[nonterminal].append(production + [new_nonterminal])
            updated[new_nonterminal] = []
            for production in recursive:
                updated[new_nonterminal].append(production + [new_nonterminal])
            updated[new_nonterminal].append(["epsilon"])
        else:
            updated[nonterminal] = [list(production) for production in productions]
    return updated

def left_factor(grammar):
    updated = {}
    counter = 1
    for nonterminal, productions in grammar.items():
        grouped = {}
        for production in productions:
            prefix = production[0] if production else "epsilon"
            grouped.setdefault(prefix, []).append(production)
        updated[nonterminal] = []
        changed = False
        for prefix, group in grouped.items():
            if len(group) == 1:
                updated[nonterminal].append(group[0])
                continue
            common_prefix = list(group[0])
            for production in group[1:]:
                limit = min(len(common_prefix), len(production))
                index = 0
                while index < limit and common_prefix[index] == production[index]:
                    index += 1
                common_prefix = common_prefix[:index]
            if not common_prefix:
                updated[nonterminal].extend(group)
                continue
            changed = True
            new_nonterminal = f"{nonterminal}{counter}"
            counter += 1
            updated[nonterminal].append(common_prefix + [new_nonterminal])
            updated[new_nonterminal] = []
            for production in group:
                suffix = production[len(common_prefix):]
                if not suffix:
                    suffix = ["epsilon"]
                updated[new_nonterminal].append(suffix)
        if not changed:
            updated[nonterminal] = [list(production) for production in productions]
    return updated

def main():
    recursion_grammar = {
        "E": [["E", "+", "T"], ["T"]],
        "T": [["T", "*", "F"], ["F"]],
        "F": [["(", "E", ")"], ["id"]],
    }
    factoring_grammar = {
        "S": [["i", "E", "t", "S"], ["i", "E", "t", "S", "e", "S"], ["a"]],
    }

    print("Left Recursion")
    print_grammar("Input Grammar", recursion_grammar)
    eliminated = eliminate_left_recursion(recursion_grammar)
    print_grammar("After Removing Left Recursion", eliminated)

    print("Left Factoring")
    print_grammar("Input Grammar", factoring_grammar)
    factored = left_factor(factoring_grammar)
    print_grammar("After Left Factoring", factored)

if __name__ == "__main__":
    main()