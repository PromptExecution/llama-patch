#!/bin/bash

# Create a clean environment
mkdir -p test_env
cd test_env
cp ../rust/example.rs .

# Test case 1: Replace function
echo "Applying patch_replace_function.json..."
../../target/debug/llama-patch ../rust/patch_replace_function.json > patch_replace_function.diff
echo "Resulting diff for replacing function:"
cat patch_replace_function.diff

# Check the output file
echo "Content of modified example.rs after replacing function:"
cat example.rs
cp example.rs ../rust/example_replaced.rs

# Reset example.rs for the next test
cp ../rust/example.rs .

# Test case 2: Remove struct
echo "Applying patch_remove_struct.json..."
../../target/debug/llama-patch ../rust/patch_remove_struct.json > patch_remove_struct.diff
echo "Resulting diff for removing struct:"
cat patch_remove_struct.diff

# Check the output file
echo "Content of modified example.rs after removing struct:"
cat example.rs
cp example.rs ../rust/example_removed.rs

# Reset example.rs for the next test
cp ../rust/example.rs .

# Test case 3: Add new function
echo "Applying patch_add_function.json..."
../../target/debug/llama-patch ../rust/patch_add_function.json > patch_add_function.diff
echo "Resulting diff for adding new function:"
cat patch_add_function.diff

# Check the output file
echo "Content of modified example.rs after adding new function:"
cat example.rs
cp example.rs ../rust/example_added.rs

# Clean up
cd ..
rm -rf test_env
