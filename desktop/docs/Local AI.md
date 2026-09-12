# Setup local AI

Instructions based on https://birdslikewires.net/ollama-macpro

```bash
# Not sure this is needed with Ramalama
sudo setsebool -P container_use_devices=true

# Install Ramalama
brew install ramalama

# Download models
ramalama pull qwen2.5-coder:14b
ramalama pull ollama://library/nomic-embed-text:latest

# Serve models
ramalama serve -d --port 8080 --ctx-size 65536 hf://second-state/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M
ramalama serve -d --port 8081 ollama://library/nomic-embed-text:latest
```

Continue config

```yaml
name: Main Config
version: 1.0.0
schema: v1
models:
  - name: Remote Coding Model
    provider: openai
    model: YOUR_RAMA_MODEL_ID
    apiBase: http://hercules.jensw.eu:8080/v1
    roles:
      - chat
      - edit
      - apply

  - name: Nomic Embed
    provider: openai
    model: YOUR_EMBED_MODEL_ID
    apiBase: http://hercules.jensw.eu:8081/v1
    roles:
      - embed

```

OpenCode config

```bash
cd ~/Projects/my-project

ramalama sandbox opencode \
  --backend vulkan \
  --ctx-size 16384 \
  --ngl all \
  --env OPENCODE_ENABLE_EXA=1 \
  -w . \
  hf://Qwen/Qwen2.5-Coder-14B-Instruct-GGUF/qwen2.5-coder-14b-instruct-q4_k_m.gguf
```
