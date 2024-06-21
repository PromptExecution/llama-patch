#![allow(unused_imports)]
use std::fs;
use std::path::Path;
use syn::{File, Item, ItemFn, ItemStruct, parse_file};
use quote::ToTokens;
use proc_macro2::TokenStream;
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct Patch {
    file: String,
    r#type: String, // Use raw identifier to avoid keyword conflict
    name: String,
    code: String,
}

fn replace_in_file(file_path: &str, item_type: &str, item_name: &str, new_code: &str) {
    let original_code = fs::read_to_string(file_path).expect("Failed to read the file");
    let mut syntax_tree: File = parse_file(&original_code).expect("Failed to parse the file");

    match item_type {
        "fn" => {
            let new_item: ItemFn = syn::parse_str(new_code).expect("Failed to parse the new function code");
            for item in &mut syntax_tree.items {
                if let Item::Fn(ref mut func) = item {
                    if func.sig.ident == item_name {
                        *func = new_item.clone();
                    }
                }
            }
        }
        "struct" => {
            let new_item: ItemStruct = syn::parse_str(new_code).expect("Failed to parse the new struct code");
            for item in &mut syntax_tree.items {
                if let Item::Struct(ref mut struct_item) = item {
                    if struct_item.ident == item_name {
                        *struct_item = new_item.clone();
                    }
                }
            }
        }
        _ => panic!("Unsupported item type"),
    }

    let modified_code: TokenStream = syntax_tree.into_token_stream();
    fs::write(file_path, modified_code.to_string()).expect("Failed to write to the file");
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

    replace_in_file(&patch.file, &patch.r#type, &patch.name, &patch.code);
}
