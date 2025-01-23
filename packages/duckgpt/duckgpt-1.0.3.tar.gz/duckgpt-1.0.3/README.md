# 🦆 DuckGPT

**DuckGPT** is a Python client for interacting with the DuckGPT model, providing seamless integration and easy-to-use functionalities.

## 🚀 Features

- **Easy Installation**: Quickly set up DuckGPT with a single command.
- **Simple API**: Intuitive methods to interact with the model.
- **Flexible**: Supports various models, including `gpt-4o-mini`.
- **Supports multiple languages**: Now you can receive responses in languages other than english `gpt-4o-mini`.

## 📦 Installation

Install DuckGPT using `pip`:

```bash
pip3 install duckgpt
```

## 💡 Usage
Here's a quick example to get you started:
    
```python
from duckgpt import DuckGPT

# Initialize the client with the desired model
client = DuckGPT(model="gpt-4o-mini")

# Fetch available models
models = client.Models()

# Interact with the model
response = client.Chat("Hello, world! 你好世界！ ", [])
print(response)
```
