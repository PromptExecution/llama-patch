from redbaron import RedBaron
import sys
import json
import os

def replace_code_in_file(file_path, item_type, item_name, new_code):
    with open(file_path, 'r') as file:
        original_code = file.read()
    
    red = RedBaron(original_code)
    
    if item_type == "fn":
        target_node = red.find("def", name=item_name)
    elif item_type == "class":
        target_node = red.find("class", name=item_name)
    else:
        raise ValueError(f"Unsupported item type: {item_type}")
    
    if target_node:
        new_node = RedBaron(new_code).find(item_type)
        target_node.replace(new_node)
    
        with open(file_path, 'w') as file:
            file.write(red.dumps())
    else:
        raise ValueError(f"Item {item_name} not found in {file_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python llama_patch.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    file_path = data["FILE"]
    item_type = data["ITEM_TYPE"]
    item_name = data["ITEM_NAME"]
    new_code = data["NEW_CODE"]
    
    replace_code_in_file(file_path, item_type, item_name, new_code)
    
    os.system(f"git diff {file_path} > llama_patch.diff")

if __name__ == "__main__":
    main()

