# DeepSeek CLI

A beautiful command-line interface for DeepSeek AI models powered by Rich.

![CLI Demo](https://via.placeholder.com/800x400.png?text=DeepSeek+CLI+Demo)

## Features

- ✨ Rich terminal formatting with Markdown support
- 💬 Interactive chat interface
- 🚀 Streaming responses with progress indicators
- 🔐 Secure API key configuration
- 📦 Multiple model support
- 🎨 Syntax highlighting for code blocks

## Installation

```bash
pip install deepseek-cli
```

## Getting Started

1. Configure your API key:
```bash
deepseek configure
```

2. Start interactive chat:
```bash
deepseek chat
```

3. Generate content from a prompt:
```bash
deepseek generate "Explain quantum computing in simple terms" --temperature 0.5
```

4. List available models:
```bash
deepseek models
```

## Advanced Usage

### Streaming Mode
```bash
deepseek chat --prompt "Write a poem about AI" --stream --markdown
```

### Code Generation
```bash
deepseek generate "Write a Python function to calculate Fibonacci sequence" --model deepseek-coder
```

### Disable Markdown
```bash
deepseek chat --no-markdown
```

## Development
```bash
git clone https://github.com/Pro-Sifat-Hasan/deepseek-cli.git
cd deepseek-cli
pip install -e .
```

## License
MIT License - See [LICENSE](LICENSE) for details