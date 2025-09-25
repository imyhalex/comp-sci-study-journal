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
    - Think about the blueprint for the data structured in rows, colums, table. This is how the data is organized.
- Integrity: Ensure the database's contents satisfy constraint. Making sure the data follows the rules (e.g. non-negative ages, every student must have an ID).
- Maniputation: Programming interface for accessing and modifying the contents of a database

__Relation__: is unordered set that contains the relationship of attributes that represents entity
- A formal word for a table
    - It's an unordered set of tuples (rows)
    - Each tuples is made of attributes (columns)
    - Those attributes describe an entity (like a student, book, or customer)
- Which means: 
    - Is a table made of rows and columns, where each row represents an entity and each colum represents an attributes of that entity.

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
- Rules defined by the user (or database designer) that the data must always follow.
- They protect database integrity by making sure only valid data can be stored
- They can check:
    - Values inside a single row (e.g. _age_ must be >= 0)
    - Relationship accross rows and tables (e.g., every order must belong to an existing customer).
- If an opeartion would break a constraint, the DBMS blocks it.
- `Uniqe key` constraint and `foreign key(referral)` constrinat are most common
- SQL:92 support `gobal asserts` but these are rarely used
    - `CHECKS` can be defined on one or more table

### Questions:
__Q__: Why not just use file system(store data in flat file) than DBMS?
1. Data Consistency
    - Flat File: Both update might overwrite each other unless you code your own locking system
    - DBMS: The database enforces constraints (e.g. no duplcate booking) and transaction garatee all-or-nothing
2. Efficnent Data Retrival
    - Flat File: To find “all customers who booked in September,” you’d have to scan the whole file.
    - DBMS: You create an index (like a book’s index) and jump right to the matching rows.
3. Crash Recovery
    - Flat File: If your program crashes halfway through writhing, you might end up with a corrupted file
    - DBMS: Use Write-Ahead Logging (WAL) and checkpoints so it can roll back incomplete transactions or redo finished ones.
4. Data Independence
    - Flat File: If you change the file layout (say you add a new file), every program that reads it breaks.
    - DBMS: Abstarcts the storage. Apps talk to SQL, not the physical layout. Shcema evolution is easier.
5. Concurrent Access
    - Flat File: Two process writing at once -> chaos (corrputed file, partial updates)
    - DBMS: Has concurrency control so multiple users can safely read/write at the same time.

__Q__: Describe the difference between `key`, `primary key`, and `candidate key`
1. Key (general idea):
    - A `key` is any set (can be one or more) of attributes that can uniquely identify a tuple (row) in a relation (table)
2. Candidate Key:
    - It is a minimal key - meaning you can't remove any attribute from it and still uniquely identify rows
    - A relation can have multiple candidate keys
    - Each is an equal valid choice to serve as the primary identifier.
3. Primary Key:
    - Is the chosen candidate key the databse will use as the main identifier for rows
    - It’s also the key that other tables reference (via foreign keys) to build relationships.
4. Composite Key:
    - Means the key is made up of more than one attribute
    - So:
        - If a candidate key uses one attribute -> it is a simple key
        - If a candidate key use two or more attributes -> it is a composite key
5. Foreign Key:
    - An attribute (one or set of attributes) references the primary key in another table.
    - It create relationship between two tables
    - Its job to ensure referential integrity (you can’t borrow a book from a library if the member doesn’t exist in the members table).

## Data Manipulation Language (DMLS)
Methods to store tand retrive information from a database

Relational Algebra vs. 

__Procedural__
- The query sepcifies the (high-level) strategy to find the desired results based on set/bags
- The user tells the database HOW to get the data.
- You specify the sequence of operations (loops, joins, selections, etc.).
- More like a step-by-step “recipe.”
- Example: Relational Algebra, older query languages.

__Non-Procedural__
- The query specifies only what data is wanted and not wanted (SQL)
- The DBMS figures out the best execution strategy (query optimizer).

__Procedural(Relational Algebra) vs. Non-Procedureal (Declaritive)__
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
        2. The corresponding attributes have the same domains(same data types)
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

-- SQL Equivalent (remove duplicate naturally)
SELECT a, b FROM R
UNION
SELECT a, b FROM S;

-- This contains duplicates
SELECT a, b FROM R
UNION ALL
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

S(c, d)
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

SELECT * FROM R JOIN S USING (a_id, b_id);

SELECT * FROM R JOIN S
ON R.a_id = S.a_id AND R.b_id = S.b_id;

-- Theta join (explicit condition, a cross join with predicates)
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

### Questions:
__Q__: what are differences between SQL and relational algebra
- In relational algebra(procedural)
    - A relation is always a set -> no duplicate anywhere in the final result
    - Every operation (`∪, ∩, −, π, σ, ⋈, ×`) produces a duplicate-free set
        - If duplicates appear naturally during the operation, they are collapsed (only one copy remains).
    - You must spell  out the steps (`e.g., σ condition (π attributes (R × S))`).
    - It's like writhing a receipe -> you're in control "how" to compute
- In SQL/ relational calculus (non-procedural, delcarative):
    - Tables are bags(multisets) by default -> duplicates appear unless you explicitly remove them (`DISTINCT`)
    - You state what you want, not the steps to get it
    - The DBMS query optimizer choose the execution plan (join, scans, indexs, etc..)
    - It's like ordering food at a restaurant -> you say "I want pasta" not "boil water, add salt, cook noodles..."