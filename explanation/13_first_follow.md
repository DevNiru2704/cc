**Concept**: Compute FIRST and FOLLOW sets for a grammar
**Logic**:
- Store the grammar inside the program
- Compute FIRST sets until they stop changing
- Compute FOLLOW sets using FIRST information and the start symbol
**Sample Input**:
Grammar used in the program:
```text
E -> T E'
E' -> + T E' | epsilon
T -> F T'
T' -> * F T' | epsilon
F -> ( E ) | id
```
**Sample Output**:
```
Grammar
E -> T E'
E' -> + T E'
E' -> epsilon
T -> F T'
T' -> * F T'
T' -> epsilon
F -> ( E )
F -> id

FIRST
E: ['(', 'id']
E': ['+', 'epsilon']
T: ['(', 'id']
T': ['*', 'epsilon']
F: ['(', 'id']

FOLLOW
E: ['$', ')']
E': ['$', ')']
T: ['$', ')', '+']
T': ['$', ')', '+']
F: ['$', ')', '*', '+']
```
**Run**:
```bash
python3 code/13_first_follow.py
```
