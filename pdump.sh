#!/bin/bash

# Set the default project path to the current directory if not provided
project_path="${1:-.}"


# Function to dump file content with filename notation
dump_file() {
    echo "📂 File: $1"
    cat "$1"
    echo "" # New line for separation
}

# Check if the project path exists
if [ ! -d "$project_path" ]; then
    echo "Project path does not exist: $project_path"
    exit 1
fi

# Change to the project directory
cd "$project_path" || exit

# Dump README.md if it exists
if [ -f "README.md" ]; then
    dump_file "README.md"
fi

echo "👋🏻 project files in $(pwd)"
rg --files | tree --fromfile

# dump any docs file
if [ -d "docs" ]; then
    for md_file in docs/*.md; do
        dump_file "$md_file"
    done
fi

if [ -f "Dockerfile" ] ; then
    dump_file "Dockerfile"
fi


if [ -f "requirements.txt" ]; then
    # Python project
    dump_file "requirements.txt"

    for py_file in $(find . -type f -name "*.py" | grep -v "venv"); do
        dump_file "$py_file"
    done
elif [ -f "pyproject.toml" ] ; then
    # Python poetry project
    dump_file "pyproject.toml"

    # Dump all .py files in src directory
    if [ -d "src" ]; then
        # dump src
        for py_file in $(find src -type f -name "*.py"); do
            dump_file "$py_file"
        done
    else
        ## other project (this)
        for py_file in $(find . -type f -name "*.py" | grep -v "venv"); do
            dump_file "$py_file"
        done
    fi
fi


if [ -f "Cargo.toml" ]; then
    # Rust project
    dump_file "Cargo.toml"

    # Dump all .rs files in src directory
    if [ -d "src" ]; then
        # Changed context: dump Rust files
        for rs_file in $(find src -type f -name "*.rs"); do
            dump_file "$rs_file"
        done
    fi

    # Run cargo build and dump the output
    echo "Output of 'cargo build':"
    cargo build
    echo "" # New line for separation

fi

# Dump any YAML file
# Look in local directory for any yaml files
for yaml_file in ./*.yaml; do
    dump_file "$yaml_file"
done
if [ -d "config" ]; then
    for yaml_file in config/*.yaml; do
        dump_file "$yaml_file"
    done
fi




# End of script

