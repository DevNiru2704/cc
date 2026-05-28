**Concept**: Remove left recursion and perform left factoring
**Logic**:
- Use one grammar to demonstrate left recursion elimination
- Use another grammar to demonstrate left factoring
- Print the original grammar and the transformed grammar
**Sample Input**:
Grammars used in the program:
```text
E -> E + T | T
T -> T * F | F
F -> ( E ) | id

S -> i E t S | i E t S e S | a
```
**Sample Output**:
```
Left Recursion
Input Grammar
E -> E + T | T
T -> T * F | F
F -> ( E ) | id

After Removing Left Recursion
E -> T E'
E' -> + T E' | epsilon
T -> F T'
T' -> * F T' | epsilon
F -> ( E ) | id

Left Factoring
Input Grammar
S -> i E t S | i E t S e S | a

After Left Factoring
S -> i E t S S1 | a
S1 -> epsilon | e S
```
**Run**:
```bash
python3 code/11_left_factoring_left_recursion.py
```
