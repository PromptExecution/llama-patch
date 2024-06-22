
# let's revise this so it uses a base ubuntu image and then installs rust.
FROM ubuntu:latest

# housekeeping ubuntu packages
RUN apt-get update && apt-get install -y build-essential curl


# 🦀 Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# 🐍 Install Python and Node.js
RUN apt-get install -y python3 python3-pip python3.12-venv nodejs npm

# Install necessary Python and Node.js packages
# Set up a virtual environment for Python packages
RUN python3 -m venv /usr/src/llama_patch/venv
RUN /usr/src/llama_patch/venv/bin/pip install --upgrade pip
RUN /usr/src/llama_patch/venv/bin/pip install redbaron

# Install TypeScript
RUN npm install -g typescript

# Set the working directory
WORKDIR /usr/src/llama_patch
# Copy the current directory contents into the container at /usr/src/llama_patch
COPY . .
RUN cargo build


# Run the binary as the entry point
CMD ["./target/release/llama_patch"]
