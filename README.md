![Work in Progress](https://img.shields.io/badge/status-WIP-yellow)

# llama-patch  WIP

A polyglot cli-tool + prompts for Extract-Transform LLM generated code into valid git patch hunks (with line numbers) by parsing the language specific AST (abstract syntax tree) code structure.

<img width=150 align=right src="llama-parse-logo.webp" alt="LLMs 💖 GNU Patch"/>

Llama Patching streamlines the process of CRUD (create, read, update, delete) source text files with LLM-generated changes by extracting line number positions & creating valid gnu unified diff files suitable for `git patch apply` the intention is to support as many languages as possible in a single container despite the need for separate native syntax/AST libraries and capabilities.   This will be possible because most modern language should be able provide interfaces to their libraries via WASM (Web Assembler) and then called from any other languuage.

| Language | Support  | Notes |
|----------|----------| ----- |
| Python   | Yes      | uses redbaron to parse AST |
| Rust     | Planned v1     | |
| JavaScript | Future    | |
| TypeScript | Future    |
| Bash     | Future      |
| Other    | TBD | please create issue + send PR to README file with link to issue |

🙏🏻 Dear community - I personally use LLM agents to author code in Rust, Python, Typescript/Javascript, Bash, Terraform/HCL, YAML/K8s CRDs and a few others and welcome contributors and maintainers of others.  My goal is for llama-patch (like gnu diff/patch) to be language agnostic.  The LLM context footprint of llama-patch instructions will be more laconic without a unique syntacial dialect for each language.   It would be better to version llama-patch generationally (ex: a "next" version for each language that converges with releases of llama-patch on major version numbers.  For this reason contributions from champions of other languages are planned/welcome and a versioning system for enhanced language specific functionality will be introduced later.  Llama-parse as an agentic tool will eventually include a variety of guard-rails to catch + output prompt friendly remediation instructions for a wide variety of LLM errors.  If you've got an idea please open an issue! 

## Summary

Llama Patching is a prompt+code (container cli) tool for LLM REPL automated code generation using git. This tool addresses the inherent limitations of large language models (LLMs), such as transformers, which struggle to count or keep track of line numbers in source code—a prerequisite for generating git unified diff GNU patches. Instead of wasting tokens, time, and money trying to zero-shot entire files, Llama Patching provides a scalable and efficient solution for managing code changes.

LLMs are powerful tools for generating code, but broadly their transformer based architecture has insurmountable limitations when it comes to tracking line numbers and generating accurate patches. This leads to several issues:

* Inefficiency: Repetitively zero-shotting entire files and is error prone + not scalable for even moderately complex projects.
* Wasteful: LLMs waste valuable tokens attempting to manage context and line numbers, which can be better utilized for generating precise code changes. 
* Context Pollution: Methods that instruct the base LLM to count and track line numbers (such as using bat) pollute the context and degrade the accuracy of the generated code.

This tool is mostly for agent pair-programming tools like AutoCoder, BabyAGI, to participate in agentic system pipelines (ex: autogen, crew.ai) and each pipeline is unique so you need to consider how you will perform the setup & usage instructions below. 
Agentic systems work best building software incrementally with specific task objectives rather than taking a ridiculously complex multi-objective prompt and outputting the entire finished project with zero errors in a single shot.   
Using systems like AutoGen, Crew.Ai it is straightforward to orchestrate teams (or crews) of agents who collaboratively implement projects through iterative development, however the maximum complexity these systems can currently attain is significantly constrained to small mostly academic exercises which demo well but don't translate into a legion of LLM agents being able to maintain (or refactor) a large sprawling legacy codebase.   While RAG's and FineTuning can improve the accuracy, each time the source code is changed incrementally those systems need to be updated, which is fine for RAG but impractical for FineTuning, however the RAG strategy for updating chunks of vectors can introduce other complications.   Generally it is best to have the LLM looking at the most recent copy of the relevant source code file(s) and ONLY outputting the changes to those files for review - unfortunately (for historical reasons) generating valid patch hunks is nearly impossible due to its dependency on counting (a task which transformers are notoriously ill equipped). llama-patch addresses these shorcomings by introducing instructions (prompt samples) + container executable tool as an intermediate step in the agentic pipeline that transmogrifies LLM outpuut into a valid gnu unified diff (patch) format which is suitable for `git apply` and creating a observable + auditable change history in the repo for agentic contributions.   It is assuumed this tool will (soon, future) be integrated into a more complete set of github actions to fire on a tagged issue and the era and job market for well paid human programmers will collapse shortly thereafter. 

## HowTo Setup & Usage
- Integrate llama-patch prompts instructing the model how to output "Llama Patch" (this will probably increase output efficiency and performance)

- THEN Continue to cut and paste code from chat into a file (ex `> llm-output.txt`), OR take off the training wheels and use a shell integrated tool such as [OpenInterpreter/open-interpreter] to directly pipe auto-extract+load LLM output into llama-patch
- OPTIONAL: include details about the iteration, prompt, model, etc. for inclusion in a llama-patch.yaml for attribution in git history (hint: use an agentic pipeline to generate this file)
- From your repo root use llama-patch to generate a patch file `cat llm-output.txt | docker run llama-patch -v ($pwd):. -- | cat > llama_patch.diff` 
  - OPTIONAL: have one or more agents review the proposed patch
- THEN `git apply llama_patch.diff`
  - ON patch fail, !!TODO: example how to check the output of the patch, and create instructions + dump source file
  - ON patch success THEN execute your tests (ex: LLM agent equivalent of the REPL)
    - any failure output should be captured and sent to the llm context that generated the llm-output.txt, **future llama-patch will have CLI parameters to prepare a dump of source files and/or tests
    - 

An intermediate step "Llama Patching" leverages a combination of prompts and containerized tools to generate code changes that are compatible with git, without requiring LLMs to handle line numbers. This approach ensures accuracy and efficiency by focusing on the logical structure of the code rather than its physical layout. 

## Suggested Install
integrate one or more of the example prompts from the [examples] directory into yoru workflow. 
```bash
docker pull github.io/llama-patch
# output llm 
docker run llama-patch 
```

## Suggested Usage

## Prompt Features
* File Identification: Specify the target file.
* Item Specification: Define the type (fn, struct, class, etc.) and name of the item to be modified.
* New Code Integration: Provide the new implementation or an empty string for removal.
* Git Patch Output: Generate patches in git patch format for easy application and rollback.
