# Relational Models
The relational model defines a database abstraction based on relations to avoid maintenance overhead

__Data Independence__
- Physical Data Independence
- Logical Data Independence

__Key Features__
- Store database in simple data structure
- Physical storage left up to the DBMS implementation
- Access data through high-level language
- DBMS figures out best execution strategy

__Properties__
- Structure: The definition of the database's relations and their contents
- Integrity: Ensure the database's contents satisfy constraint
- Maniputation: Programming interface for accessing and modifying the contents of a database

__Relation__ is unordered set that contains the relationship of attributes that represents entity

__Tuple__: another word for a row in a table
- A table map to multiple rows (tuples)
- Each row (tuple) is composed of attributes, which correspond to the columns of the table.

__Atomic Data Value__:
- Each attribute (column) in a table should hold atomic values → indivisible, not a set or list.
- Example (bad): `PhoneNumbers = {123, 456} `inside one cell.
- Example (good): split into separate rows, each with one phone number.

__Primary Key:__ uniquely identifies a single tuple

__Candidate Key:__ a bunch of cancidates that can be chosen to be primary key

__Foreign Key__: specify the an attribute from one relation maps to tuple in another relation
    - one foreign key map to another table's primary key

__Schemas__: Blueprint of the database, it defins:
- What tables exist.
- What attributes (columns) each table has.
- What data types are allowed.
- What relationships exist between tables (primary key, foreign key, constraints).

__Constraints__:
- user-defined conditions that must hold for any instance of the database (database integrity)
    - can validate data within a single tuple or accross entire relation(s)
    - prevets modifation that violates any contstraints
- `Uniqe key` constraint and `foreign key(referral)` constrinat are most common
- SQL:92 support `gobal asserts` but these are rarely used
    - `CHECKS` can be defined on one or more table

## Data Manipulation Language (DMLS)
Methods to store tand retrive information from a database

__Procedural__
- The query sepcifies the (high-level) strategy to find the desired results based on set/bags
- The user tells the database HOW to get the data.
- You specify the sequence of operations (loops, joins, selections, etc.).
- More like a step-by-step “recipe.”
- Example: Relational Algebra, older query languages.

__Non-Procedural__
- The query specifies only what data is wanted and not wanted (SQL)
- The DBMS figures out the best execution strategy (query optimizer).

__Relational Algebra__
- Relational Algebra = a formal query language for relational databases.
- It uses operators to retrieve and manipulate tuples (rows) from relations (tables).
- It’s the theory behind SQL.
- Fundamental operations to retrive and manipulate tuples in a relation
    - Based on set algebra (unordered list with no duplicates)
- Each opearator takes one or more relations as its input and putputs a new relation (closure property)
    - We can "chain" operators together to create more complex operations
    e.g.:
    ```sql
     π Name (σ Age > 20 ∧ Major = 'CS' (Students))
    ```

__Relational Algebra: Slection__
- Choose a subset of the tuples from a relation that satisfies s selection predicates
    - predicates acts as a filter to retain only tuples that fulfill its qualifiying requirements
    - can combine multiple predicates using conjunctions / disjunctions
- Notation:
```sql
σ condition (Relation)
σ = selection operator; condition = predicate (filter); Relation = input table

Predicates: Conjunction (AND) → ∧ ; Disjunction (OR) → ∨; Negation (NOT) → ¬

Example:
| ID | Name  | Age | Major   |
| -- | ----- | --- | ------- |
| 1  | Alice | 20  | CS      |
| 2  | Bob   | 21  | Math    |
| 3  | Carol | 22  | Physics |
| 4  | David | 20  | CS      |

σ Age > 20 (Students)
Result:
(2, Bob, 21, Math)
(3, Carol, 22, Physics)

σ Age > 20 ∧ Major = 'CS' (Students)
Result: none (since no CS major is over 20).

σ Age = 20 ∨ Major = 'Math' (Students)
Result: Alice, David, and Bob.
(1, Alice, 20, CS)
(2, Bob, 21, Math)
(4, David, 20, CS)
```

__Relational Algebra: Projection__
- Generates a relation with tuples that contains only the specific attributes
    - rearrange attributes ordering
    - remove unwanted attributes
    - manipulate values to create derived attributes
- Projection creates relation with only the specified attributes(columns)
- It remove duplicates(since RA is set-based)
- Keeps all rows, but only with selected attributes
- Notation:
```sql
π attribute_list (Relation)
π = projection operator; attribute_list = list of attributes to keep

Example:
| ID | Name  | Age | Major   |
| -- | ----- | --- | ------- |
| 1  | Alice | 20  | CS      |
| 2  | Bob   | 21  | Math    |
| 3  | Carol | 22  | Physics |
| 4  | David | 20  | CS      |

π Name (Students)
Result:
| Name  |
| ----- |
| Alice |
| Bob   |
| Carol |
| David |

π Major, Age (Students)
Result:
| Major   | Age |
| ------- | --- |
| CS      | 20  |
| Math    | 21  |
| Physics | 22  |

π Name, Age+1 (Students)
Result:
| Name  | Age+1 |
| ----- | ----- |
| Alice | 21    |
| Bob   | 22    |
| Carol | 23    |
| David | 21    |
```

__Relational Algebra: Union__
- Generate a relation that contais all tuples that appear in either only one or both input relations
- Schemas neeed to be compatible: The position and the type of the attributes should match.
- Combinesd tuples from two relations into a single relation
- The result contains all tuplesd that appear in either relation(or both)
- Sice RA is set-based -> dulplicates are eliminated
- Compatibility Requirement (Union-Compatible)
    - Two relations `R` and `S` can be unioned if:
        1. They have the same number of attributes
        2. The corresponding attributes have the same domains(types)
- Notation:
```sql
R ∪ S

R(a, b)
| a | b |
| - | - |
| 1 | 2 |
| 3 | 4 |

S(a, b)
| a | b |
| - | - |
| 3 | 4 |
| 5 | 6 |

Result:
| a | b |
| - | - |
| 1 | 2 |
| 3 | 4 |
| 5 | 6 |

-- SQL Equivalent
SELECT a, b FROM R
UNION
SELECT a, b FROM S;
```

__Relational Algebra: Intersection__
- Intersection produces a relation containing only the tuplesd that appear in both input relations
- It's like the logic `AND` between two sets
- Since RA is set-based, duplicates are automatically eliminated
- Compatiability Requirement:
    - Just like Union, the two relations must be the union-compatible:
        - Same number of attributes
        - Corresponding attributes must have the samwe domain(type)
- Notion:
```sql
R ∩ S

R(a, b)
| a | b |
| - | - |
| 1 | 2 |
| 3 | 4 |
| 5 | 6 |

S(a, b)
| a | b |
| - | - |
| 3 | 4 |
| 5 | 6 |
| 7 | 8 |

Result:
| a | b |
| - | - |
| 3 | 4 |
| 5 | 6 |

-- SQL Equivalent
SELECT a, b FROM R
INTERSECT
SELECT a, b FROM S;
```

__Relational Algebra: Difference__
- Returns all tuples that are in the first relation(R) but not in the second relation(S)
- Think of it like set subtractions: `R - S`
- Result contains only unique tuples(set semantics)
- Compatability Requirement
    - Just like Union and intersection, the two relations must be union-compatible:
        1. Same number of attributes
        2. Corresponding attributes must have the same domain(type)
- Notation
```sql
R − S

R(a, b)
| a | b |
| - | - |
| 1 | 2 |
| 3 | 4 |
| 5 | 6 |

S(a, b)
| a | b |
| - | - |
| 3 | 4 |
| 7 | 8 |

Result:
| a | b |
| - | - |
| 1 | 2 |
| 5 | 6 |

-- SQL Equivalent
SELECT a, b FROM R
EXCEPT
SELECT a, b FROM S;
(In some SQL dialects like Oracle, use MINUS instead of EXCEPT.)
```

__Relational Algebra: Product__
- Generate a relation that contains all possible combinations of tuples from the input relations (aka Cartesian Product)
- If `R` has `m` tuples and `S` has `n` tuples -> result has m * n tuples
- Notation:
```sql
R × S

If R(A1, A2, …, Am) and S(B1, B2, …, Bn),
then result schema is:
(A1, A2, …, Am, B1, B2, …, Bn)

If attribute names overlap, we rename them with relation names to avoid confusion:
(R.A1, …, R.Am, S.B1, …, S.Bn)

R(a, b)
| a | b |
| - | - |
| 1 | 2 |
| 3 | 4 |

S(a, b)
| c | d |
| - | - |
| x | y |

Result
| a | b | c | d |
| - | - | - | - |
| 1 | 2 | x | y |
| 3 | 4 | x | y |

-- SQL Equivalent:
SELECT *
FROM R, S;
(or explicitly: CROSS JOIN)
```

__Relational Algebra: Join__
- Join combines tuples from two relations based on a condition.
- The most common is the Natural Join: it automatically matches tuples that share the same value(s) on common attributes.
- Generate a relation that contains all tuples that are a combination of two tuples (one from each input relation) with common values(s) for one or more attributes(aka natrual join)
- Think of it as: Product (×) + Selection (σ).
- Notation:
```sql
General Join
R ⨝condition S

Natural Join
R ⨝ S

Student(ID, Name, MajorID)
| ID | Name  | MajorID |
| -- | ----- | ------- |
| 1  | Alice | 10      |
| 2  | Bob   | 20      |
| 3  | Carol | 10      |

Majors(MajorID, MajorName):
| MajorID | MajorName |
| ------- | --------- |
| 10      | CS        |
| 20      | Math      |


Natural Join: Students ⨝ Majors
| ID | Name  | MajorID | MajorName |
| -- | ----- | ------- | --------- |
| 1  | Alice | 10      | CS        |
| 2  | Bob   | 20      | Math      |
| 3  | Carol | 10      | CS        |


-- Theta-Join (⨝θ): Join with a general condition θ.
R ⨝ R.a < S.b

-- Natural join
SELECT *
FROM Students
NATURAL JOIN Majors;

-- Theta join (explicit condition)
SELECT *
FROM Students S, Majors M
WHERE S.MajorID = M.MajorID;
```

__Extra Operators__
- Rename (p)
- Assignment (R<-S)
- Duplicate Elimination(δ)
- Aggregation(γ)
- Sorting(τ)
- Division (R÷S)