![Work in Progress](https://img.shields.io/badge/status-WIP-yellow)

# llama-patch  WIP

👋🏻 A [polyglot](https://www.merriam-webster.com/dictionary/polyglot) [containerized](https://en.wikipedia.org/wiki/Containerization) [cli-tool](https://en.wikipedia.org/wiki/Command-line_interface) + prompt instructions for Extract-Transform LLM generated code into valid git patch hunks (with line numbers) by parsing the language specific [AST (abstract syntax tree)](https://en.wikipedia.org/wiki/Abstract_syntax_tree) rather than letting an LLM re-create & output an entire copy of an entire file _(which is both impractical and dangerous in most large codebases, especially those that have limited/incomplete test coverage)_


<img width=150 align=right src="llama-parse-logo.webp" alt="LLMs 💖 GNU Patch"/>

Llama Patching streamlines the process of CRUD (create, read, update, delete) source text files with LLM-generated using an intermediate representation that can be translated into a valid [gnu unified diff](https://www.gnu.org/software/diffutils/manual/html_node/Detailed-Unified.html) format suitable for [`git patch apply`](https://en.wikipedia.org/wiki/Patch_\(Unix\)).

### Support
| Language | Support  | Notes |
|----------|----------| ----- |
| Python   | YES      | uses redbaron to parse AST |
| Rust     | YES     | uses syn crate to parse AST |
| JavaScript | Next    | |
| TypeScript | Next    | in progress |
| Bash     | Future      |
| Go | Future |
| Java | Future |
| 💖 Other    | TBD | please create issue + send PR to README file with link to issue |


## Quickstart
To get started simply add the [example instruction prompt](examples/) to your favorite codegen LLM, then pipe it's output into llama-patch using the cli or a subprocess to get out a patch file.
See [Howto](#howto) section for a sample step by step.


## Summary Abstract

Since most people who will visit this page are data-scientists who mopstly aren't git wizards but are accustomed to scanning a paper abstract let's explain llama-patch this way:

Llama Patching is a prompt+code (container cli) tool for LLM [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop)  automated code generation using git. This tool addresses the inherent limitations of large language models (LLMs), such as transformers, which struggle to count or keep track of line numbers in source code—a prerequisite for generating git unified diff GNU patches. Instead of wasting tokens, time, and money trying to zero-shot entire files, Llama Patching provides a scalable and efficient solution for translating LLM outpuut into the gold-standard "unix patch" format used for decades to perform code changes.  Llama-patch also has the beneficial side effect of creating meaningful git history for agent/human proxy collaboration on a repository.

LLMs are powerful tools for generating code, but broadly their modern transformer based architecture has (*present day*) insurmountable limitations when it comes to tracking line numbers and generating accurate patches.  Every other approach (besides llama-patch) can be ranked & fit to these issues:

* Inefficiency: Repetitively zero-shotting entire files and is error prone + not scalable for even moderately complex projects.
* Wasteful: LLMs waste valuable tokens attempting to manage context and line numbers, which can be better utilized for generating precise code changes.
* Context Pollution: Methods that instruct the base LLM to count and track line numbers (such as using bat) pollute the context and degrade the accuracy of the generated code and generally won't work.
* Bad Alternative Practices: executing non-contextual search and replace mechanisms such as 'sed' or 'regex' based is like performing surgery with a machete rather than a scalpel and will inadvertantly introduce a variety of issues and may create cybersecurity consequences.

Llama-patch proffers a better tooling approach for your [agentic codegen](https://github.com/SamurAIGPT/Best-AI-Agents) like AutoCoder, BabyAGI, or pipeline such as [autogen](https://microsoft.github.io/autogen/) or [crew.ai](https://github.com/joaomdmoura/crewAI).  Since your pipeline is probably unique you will need to consider how to best perform the setup & usage instructions outlined below.

Agentic systems work best building software incrementally with specific task objectives rather than taking a ridiculously complex multi-objective prompt and outputting the entire finished project with zero errors in a single shot.

Using systems like AutoGen, Crew.Ai it is straightforward to orchestrate teams (or crews) of agents who collaboratively implement projects through iterative development, however the maximum complexity these systems can currently attain is significantly constrained to small mostly academic exercises which demo well but don't translate into a legion of LLM agents being able to maintain (or refactor) a large sprawling legacy codebase.   While RAG's and FineTuning can improve the accuracy, each time the source code is changed incrementally those systems need to be updated, which is fine for RAG but impractical for FineTuning, however the RAG strategy for updating chunks of vectors can introduce other complications.   Generally it is best to have the LLM looking at the most recent copy of the relevant source code file(s) and ONLY outputting the changes to those files for review - unfortunately (for historical reasons) generating valid patch hunks is nearly impossible due to its dependency on counting (a task which transformers are notoriously ill equipped). llama-patch addresses these shorcomings by introducing instructions (prompt samples) + container executable tool as an intermediate step in the agentic pipeline that transmogrifies LLM outpuut into a valid gnu unified diff (patch) format which is suitable for `git apply` and creating a observable + auditable change history in the repo for agentic contributions.   It is assuumed this tool will (soon, future) be integrated into a more complete set of github actions to fire on a tagged issue and the era and job market for well paid human programmers will collapse shortly thereafter.

## Usage
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

## 🙏🏻 Contributors Welcome!
If you've got an idea please open an issue! Language Champions needed. I can't possibly maintain all the languages (my stack is rust, python, typescript, terraform/HCL and bash so I will try and do those)
My goal is for llama-patch (like gnu diff/patch) to be language agnostic (despite its dependency on AST code parsing).
The LLM context footprint of llama-patch instructions can be laconic without a unique syntacial dialect for each language.
It would be better to version llama-patch generationally (ex: a "next" version for each language that proposes changes & periodically converges with releases of llama-patch on major version numbers)
Llama-parse as an agentic tool will eventually include a variety of guard-rails to catch + output prompt friendly remediation instructions for a wide variety of LLM errors.

# Goals and Non-Goals
The goal of llama-patch is to offer laconic performant prompts for all popular models,  while supporting as many languages as possible in a single container despite the need for translating the logic into separate native syntax/AST libraries and capabilities.  The assumption is that converge becauuse most modern languages should be able provide interfaces to their libraries via WASM (Web Assembler) and then called from any other language, and that LLM's will be used to do the heavy lifting of maintain logic synchronicity between language implementations.

This tool does not seek to replace GNU patch, rather to work collaboratively as shown in the logo.

Using semantic versioning, major versions will introduce breaking changes, minor versions will introduce new functionality per language.

