from backend.app.harness.ollama_qwen import OllamaQwenHarness
def test_harness(): 
    h=OllamaQwenHarness("http://localhost:11434","qwen2.5:7b");assert h.url.endswith("/api/chat")
