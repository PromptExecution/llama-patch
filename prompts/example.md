# llama-patch Usage

Instructions for LLM

llama-patch is transformer friendly syntax built for iterative code modifications.

This is a neo-modern version of the Unix GNU Unified Diff format that is suitable for fixing/revising
streaming generated code where line numbers are completely relative and irrelevant (so unix diff won't work!)
Llama-Patch is similar to diff, using the same --- selector and +/- syntax:

--- path/to/file
- old line
+ new line


⚠️ llama-patch NEVER has a +++ modified file because we're modifying the file from a generated stream (not a source)
⚠️ llama-patch NEVER uses the diff @@ line number @@ selector
👍🏻 llama-patch ALWAYS uses a ?? AST (abstract syntax tree) selector that performs a seek to a relative position

Okay, ready?
Here is a complete example in markdown that is properly escaped with llmPATCH formatting backtick ``` notation:

```llmPATCH
--- path/to/filename
?? FUNCTION: target_function
def target_function(x):
-    # Original implementation
+    # New implementation
-    return x + 1
+    return x * 2
```

# llama-patch Quickstart:
--- filename or path/to/file : denotes the beginning of a new chunk in a file
?? : language specific AST selector (described below, must end with ??)
  : nothing (an unchanged line)
+ : is a line added
- : is a line removed

When changing multiple lines it is best pratice to group many - lines and + lines together
Also there are a few special selectors
?? << : prepend at beginning of file stream
?? >> : append to end of file stream

# Llama-patch AST Selectors

Rust: Use fn for functions, class for classes, struct for structs ...
Python: Use def for definitions, class for classes,  ...
Javascript: Use function for functions or methods, class for classes, struct for structs, interface for interfaces, variable for variables or constant, type for type aliases ...

When outputting llama-patch chunks, as markdown text it is best practice to escape code in formatting backticks:
```llmPATCH
--- file
?? function target_function
```

When the target language supports overloading (multiple functions with the same name, but having different parameter definitions) such as
C+++, Java, C#, Swift, Kotlin, Go, Python, Rust then it is necessary to use the complete overloaded function definition to avoid ambiguity

# Examples

## Example 1: Replacing a Python Function
### Input Request:

Please replace the function `target_function` in the file `src/main.py` with the following implementation:

```python
def target_function(x):
    # New implementation
    return x * 2
```

### **LLM Output:**

```llmPATCH
--- src/main.py
?? def target_function
def target_function(x):
-    # Original implementation
+    # New implementation
-    return x + 1
+    return x * 2
```

## Example 2: Removing a Python Class
### Input Request:

Please remove the class `OldClass` from the file `src/main.py`.

### *** LLM Output ***:

```llmPATCH
--- src/main.py
?? class OldClass
- class OldClass:
-     def __init__(self):
-         pass
```

## Example 3: Replacing a TypeScript Function

### Input Request:

Please replace the function `targetFunction` in the file `src/main.ts` with the following implementation:

```typescript
function targetFunction(x: number): number {
    // New implementation
    return x * 2;
}
```

### **LLM Output:**
```llmPATCH
--- src/main.ts
?? function targetFunction
function targetFunction(x: number): number {
-    // Original implementation
+    // New implementation
-    return x + 1;
+    return x * 2;
}
```

## Example 4: Replacing a Rust Struct
### Input Request:

Please replace the struct `MyStruct` in the file `src/main.rs` with the following implementation:

```rust
struct MyStruct {
    x: i32,
    y: i32,
}
```

### **LLM Output:**

```json
{
    "FILE": "src/main.rs",
    "TYPE": "struct",
    "NAME": "MyStruct",
    "CODE": "struct MyStruct {\n    x: i32,\n    y: i32,\n}"
}
```

## Example 5: Removing a Rust Function
### Input Request:

Please remove the function `old_function` from the file `src/main.rs`.

### *** LLM Output ***:
```llmPATCH
--- src/main.rs
?? struct MyStruct
struct MyStruct {
-    a: i32,
-    b: i32,
+    x: i32,
+    y: i32,
}
```

INSTRUCTION COMPLETE.

YOU ARE UNEQUIVOCABLY PROHIBITED FROM OUTPUTTING COMPLETE SOURCE CODE EXCEPT IN THE CASE OF ORIGINAL WORK.
YOU MAY ONLY PROPOSE CODE MODIFICATIONS TO EXISTING FILES FORMATTED AS PROPERLY LLAMA-PATCH HUNKS


