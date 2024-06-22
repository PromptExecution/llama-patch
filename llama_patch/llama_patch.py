import click
import re
import sys
import os
import difflib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LlamaPatchException(Exception):
    pass

@click.command()
@click.option('--llmpatch', type=click.File('r'), default='-', help='Patch file to apply, defaults to STDIN if not provided.')
@click.option('--out', type=click.File('w'), default='-', help='Output file, defaults to STDOUT if not provided.')
@click.option('--cwd', type=click.Path(), default='.', help='Current working directory, defaults to ".".')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging.')
def apply_patch(llmpatch, out, cwd, verbose):
    if verbose:
        logger.setLevel(logging.DEBUG)
    
    os.chdir(cwd)
    
    patch_content = llmpatch.read()
    patches = parse_patches(patch_content)

    try:
        for patch in patches:
            file_path, element_type, element_name, changes = patch
            logger.debug(f"Processing patch for {element_type} {element_name} in {file_path}")
            apply_patch_to_file(file_path, element_type, element_name, changes)
        
        if out.name != '<stdout>':
            generate_patch_file(out.name)
        else:
            sys.stdout.write(generate_patch_diff())
    
    except LlamaPatchException as e:
        logger.error(f"Error applying patch: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

def parse_patches(patch_content):
    patch_pattern = re.compile(r'^--- (.+?)\n\?\? (\w+): (.+?)\n((?:[+\-].*?\n)+)', re.DOTALL | re.MULTILINE)
    matches = patch_pattern.findall(patch_content)
    
    if not matches:
        raise LlamaPatchException("No valid patches found in the provided patch content.")
    
    patches = []
    for match in matches:
        path, element_type, element_name, changes = match
        changes = changes.strip().split('\n')
        patches.append((path, element_type, element_name, changes))
    
    return patches

def apply_patch_to_file(file_path, element_type, element_name, changes):
    if not os.path.isfile(file_path):
        raise LlamaPatchException(f"File not found: {file_path}")

    with open(file_path, 'r') as file:
        original_code = file.read()

    if element_type in ["function", "def"]:
        updated_code = apply_function_patch(original_code, element_name, changes)
    elif element_type == "class":
        updated_code = apply_class_patch(original_code, element_name, changes)
    elif element_type == "struct":
        updated_code = apply_struct_patch(original_code, element_name, changes)
    elif element_type == "<<":
        updated_code = prepend_code(original_code, changes)
    elif element_type == ">>":
        updated_code = append_code(original_code, changes)
    else:
        raise LlamaPatchException(f"Unsupported element type: {element_type}")

    with open(file_path, 'w') as file:
        file.write(updated_code)

def apply_function_patch(original_code, function_name, changes):
    function_pattern = re.compile(rf'def {function_name}\(.*?\):\n((?:\s+.*?\n)*)', re.DOTALL)
    match = function_pattern.search(original_code)
    if not match:
        raise LlamaPatchException(f"Function {function_name} not found")

    start, end = match.span()
    context_code = match.group(1)

    new_code = generate_new_code(context_code, changes)
    updated_code = original_code[:start] + f'def {function_name}(\n{new_code}' + original_code[end:]
    return updated_code

def apply_class_patch(original_code, class_name, changes):
    class_pattern = re.compile(rf'class {class_name}:\n((?:\s+.*?\n)*)', re.DOTALL)
    match = class_pattern.search(original_code)
    if not match:
        raise LlamaPatchException(f"Class {class_name} not found")

    start, end = match.span()
    context_code = match.group(1)

    new_code = generate_new_code(context_code, changes)
    updated_code = original_code[:start] + f'class {class_name}:\n{new_code}' + original_code[end:]
    return updated_code

def apply_struct_patch(original_code, struct_name, changes):
    struct_pattern = re.compile(rf'struct {struct_name} {{\n((?:\s+.*?\n)*)}}', re.DOTALL)
    match = struct_pattern.search(original_code)
    if not match:
        raise LlamaPatchException(f"Struct {struct_name} not found")

    start, end = match.span()
    context_code = match.group(1)

    new_code = generate_new_code(context_code, changes)
    updated_code = original_code[:start] + f'struct {struct_name} {{\n{new_code}}}' + original_code[end:]
    return updated_code

def prepend_code(original_code, changes):
    new_code = "\n".join(line[1:] for line in changes if line.startswith('+'))
    updated_code = new_code + "\n" + original_code
    return updated_code

def append_code(original_code, changes):
    new_code = "\n".join(line[1:] for line in changes if line.startswith('+'))
    updated_code = original_code + "\n" + new_code
    return updated_code

def generate_new_code(context_code, changes):
    context_lines = context_code.strip().split('\n')
    new_code = []

    for line in changes:
        if line.startswith('-'):
            context_lines.remove(line[1:].strip())
        elif line.startswith('+'):
            new_code.append(line[1:])
        else:
            new_code.append(line)

    return "\n".join(new_code)

def generate_patch_file(output_file):
    diff = generate_patch_diff()
    with open(output_file, 'w') as file:
        file.write(diff)

def generate_patch_diff():
    file_list = [f for f in os.listdir('.') if os.path.isfile(f)]
    diff = []
    
    for file_name in file_list:
        with open(file_name, 'r') as file:
            new_code = file.readlines()
        with open(f'{file_name}.orig', 'r') as file:
            old_code = file.readlines()
        file_diff = difflib.unified_diff(old_code, new_code, fromfile=f'{file_name}.orig', tofile=file_name)
        diff.extend(file_diff)
    
    return ''.join(diff)

if __name__ == "__main__":
    apply_patch()

