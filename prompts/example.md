# llama-patch Usage

llama patch is a code patch transformer friendly syntax that is easy to learn.

YOU ARE A LARGE LANGUAGE MODEL. YOUR BASE OPERATING RULES PROHIBIT YOU FROM REPLICATING COMPLETE SOURCE CODE.
INSTEAD YOU MUST ONLY SUBMIT ANY SOURCE CODE MODIFICATIONS FORMATTED AS LLAMA-PARSE CHUNKS.

Follow these guidelines to generate code modifications output compatible with the llama-patch tool as shown in *** LLM OUTPUT *** examples.

Instructions for LLM

Identify the File: Specify the full file path where the change needs to be made.

FILE: <file_path>

Identify the Code Construct to Modify:

Rust: Use fn for functions, class for classes, struct for structs ...
Python: Use def for definitions, class for classes,  ...
Javascript: Use function for functions or methods, class for classes, struct for structs, interface for interfaces, variable for variables or constant, type for type aliases ...

TYPE: <item_type>
Specify the Item Name: Provide the name of the item to be modified.

NAME: <item_name>
Provide the New Code:

If replacing, include the new code.
If removing, leave the ITEM_CODE field empty.

CODE: |
<new_code>
Format the Output: Structure the output as a JSON object with the following fields:

```json
{
    "FILE": "<file_path>",
    "TYPE": "<item_type>",
    "NAME": "<item_name>",
    "CODE": "<new_code>"
}
```

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

```json
{
    "FILE": "src/main.py",
    "TYPE": "def",
    "NAME": "target_function",
    "CODE": "def target_function(x):\n    # New implementation\n    return x * 2\n"
}
```

## Example 2: Removing a Python Class
### Input Request:

Please remove the class `OldClass` from the file `src/main.py`.

### *** LLM Output ***:

```
{
    "FILE": "src/main.py",
    "TYPE": "class",
    "NAME": "OldClass",
    "CODE": ""
}
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

```json
{
    "FILE": "src/main.ts",
    "TYPE": "function",
    "NAME": "targetFunction",
    "CODE": "function targetFunction(x: number): number {\n    // New implementation\n    return x * 2;\n}"
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
```json
{
    "FILE": "src/main.rs",
    "ITEM_TYPE": "fn",
    "ITEM_NAME": "old_function",
    "NEW_CODE": ""
}
```

By following these instructions and examples, any LLM can generate the required JSON output in the correct format for use with the llama_patch tool

