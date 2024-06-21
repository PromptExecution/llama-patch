#![allow(unused_imports)]

use std::fs;
use std::process::Command;
use syn::{File, Item, ItemFn, ItemStruct, parse_file};
use quote::ToTokens;
use proc_macro2::TokenStream;
use serde::{Deserialize, Serialize};
use tempfile::NamedTempFile;

#[derive(Deserialize)]
struct Patch {
    file: String,
    r#type: String, // Use raw identifier to avoid keyword conflict
    name: String,
    code: Option<String>, // Option to handle removal
}

fn apply_patch(file_path: &str, item_type: &str, item_name: &str, new_code: Option<&str>) {
    let original_code = fs::read_to_string(file_path).expect("Failed to read the file");
    let mut syntax_tree: File = parse_file(&original_code).expect("Failed to parse the file");

    match item_type {
        "fn" => {
            let new_item: Option<Item> = match new_code {
                Some(code) => Some(Item::Fn(syn::parse_str(code).expect("Failed to parse the new function code"))),
                None => None,
            };
            modify_items(&mut syntax_tree.items, item_name, new_item);
        }
        "struct" => {
            let new_item: Option<Item> = match new_code {
                Some(code) => Some(Item::Struct(syn::parse_str(code).expect("Failed to parse the new struct code"))),
                None => None,
            };
            modify_items(&mut syntax_tree.items, item_name, new_item);
        }
        _ => panic!("Unsupported item type"),
    }

    let modified_code: TokenStream = syntax_tree.into_token_stream();
    let temp_file = NamedTempFile::new().expect("Failed to create a temporary file");
    fs::write(temp_file.path(), modified_code.to_string()).expect("Failed to write to the temporary file");

    generate_diff(file_path, temp_file.path().to_str().expect("Invalid temporary file path"));
}

fn modify_items(items: &mut Vec<Item>, item_name: &str, new_item: Option<Item>) {
    let mut found = false;
    items.retain_mut(|item| {
        if let Some(existing_item) = match_item(item, item_name) {
            found = true;
            if let Some(ref new_item) = new_item {
                *existing_item = new_item.clone();
                true
            } else {
                false
            }
        } else {
            true
        }
    });

    if !found {
        if let Some(new_item) = new_item {
            items.push(new_item);
        }
    }
}

fn match_item<'a>(item: &'a mut Item, item_name: &str) -> Option<&'a mut Item> {
    match item {
        Item::Fn(ref mut func) if func.sig.ident == item_name => Some(item),
        Item::Struct(ref mut struct_item) if struct_item.ident == item_name => Some(item),
        _ => None,
    }
}

fn generate_diff(original_file: &str, modified_file: &str) {
    let output = Command::new("diff")
        .arg("-u")
        .arg(original_file)
        .arg(modified_file)
        .output()
        .expect("Failed to execute diff command");

    if !output.stdout.is_empty() {
        println!("{}", String::from_utf8_lossy(&output.stdout));
    } else {
        println!("No changes detected.");
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <patch_file>", args[0]);
        std::process::exit(1);
    }

    let patch_file = &args[1];
    let patch_json = fs::read_to_string(patch_file).expect("Failed to read the patch file");
    let patch: Patch = serde_json::from_str(&patch_json).expect("Failed to parse the patch JSON");

    apply_patch(&patch.file, &patch.r#type, &patch.name, patch.code.as_deref());
}
