#!/bin/bash

set -e

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieve models..."
# ollama pull llama3
ollama create mistral-ollama -f /Modelfile
ollama create nomic-embed -f /Modelfile.embeddings
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid
