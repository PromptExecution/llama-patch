# Just a command runner
# https://github.com/casey/just

build:
	docker build -t llama_patch .

build-rust:


example:
	docker run -v $(pwd):/usr/src/patch_tool llama_patch example.rs target_function "fn target_function(x: i32) -> i32 { x * 2 }"

parse INPUTFILE:
	cat {{INPUTFILE}} | docker run -v $(pwd):. llama_patch

