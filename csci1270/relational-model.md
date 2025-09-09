# Relational Models
- Structure
- Integrity
- Maniputation

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
- Notions:
```sql
σ condition (Relation)
σ = selection operator; condition = predicate (filter); Relation = input table

Predicates: Conjunction (AND) → ∧ ; Disjunction (OR) → ∨; Negation (NOT) → ¬

Example:
σ Age > 20 ∧ Major = 'CS' (Students)
σ Age = 20 ∨ Major = 'Math' (Students)
```

__Relational Algebra: Projection__
- Generates a relation with tuples that contains only the specific attributes
    - rearrange attributes ordering
    - remove unwanted attributes
    - manipulate values to create derived attributes

__Relational Algebra: Union__
- Generate a relation that contais all tuples that appear in either only one or both input relations
- Schemas neeed to be compatible: The position and the type of the attributes should match.

__Relational Algebra: Intersection__

__Relational Algebra: Difference__

__Relational Algebra: Product__
- Generate a relation that contains all possible combinations of tuples from the input relations (aka Cartesian Product)
- Syntax: (R * S)

__Relational Algebra: Join__
- Generate a relation that contains all tuples that are a combination of two tuples (one from each input relation) with common values(s) for one or more attributes(aka natrual join)

__Extra Operators__
- Rename (p)
- Assignment (R<-S)
- Duplicate Elimination(δ)
- Aggregation(γ)
- Sorting(τ)
- Division (R÷S)