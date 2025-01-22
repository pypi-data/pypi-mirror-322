# EnvVault

EnvVault is a Python package for encrypting and managing `.env` files, similar to Rails Credentials. It allows you to securely store sensitive information (such as API keys, database passwords, etc.) and decrypt and use this information at runtime.

## Features

- **Encrypt `.env` files**: Encrypt plaintext `.env` files into `.env.enc` files.
- **Decrypt `.env.enc` files**: Decrypt `.env.enc` files at runtime and load environment variables.
- **Multi-environment support**: Create separate encrypted files for different environments (e.g., `development`, `production`).
- **CLI tool**: Provides a command-line interface for managing encrypted files.
- **Integration with `pydantic_settings`**: Supports managing decrypted environment variables using `pydantic_settings`.

## Installation

Install using Poetry:

```bash
poetry add envvault

# Or install using pip:
pip install envvault
```

## Usage

### 1. Initialize

Initialize the `master key` and an empty `.env.enc` file:

```bash
envvault init --env development
```

This will generate the following files:
- `master.key`: The master key used for encryption and decryption.
- `.env.development.enc`: An empty encrypted file.

---

### 2. Edit Encrypted File

Edit the `.env.enc` file using your default editor:

```bash
envvault edit --env development
```

The editor will open a temporary file. After editing, the content will be re-encrypted and saved to `.env.development.enc`.

---

### 3. View Decrypted Environment Variables

Decrypt and view the contents of the `.env.enc` file:

```bash
envvault view --env development
```

---

### 4. Use in Code

Load decrypted environment variables in your code:

```python
from envvault.settings import Settings

# Load configuration for the development environment
settings = Settings.from_credentials(env_name="development")
print("API Key:", settings.API_KEY)
print("Database URL:", settings.DATABASE_URL)
```

---

## Examples

### Initialize and Edit Encrypted File

1. Initialize:
   ```bash
   envvault init --env development
   ```

2. Edit:
   ```bash
   envvault edit --env development
   ```

   Enter the following content in the editor:
   ```yaml
   API_KEY=your_api_key_here
   DATABASE_URL=your_database_url_here
   ```

3. View:
   ```bash
   envvault view --env development
   ```

   Output:
   ```
   API_KEY=your_api_key_here
   DATABASE_URL=your_database_url_here
   ```

---

### Use in Code

```python
from envvault.settings import Settings

# Load configuration for the development environment
settings = Settings.from_credentials(env_name="development")

print("API Key:", settings.API_KEY)
print("Database URL:", settings.DATABASE_URL)
```

---

## Configuration

### Default Editor

You can set the default editor using the `EDITOR` environment variable. For example:

```bash
export EDITOR=code  # Use VS Code
export EDITOR=nano  # Use Nano
export EDITOR=vim   # Use Vim
```

---

### Multi-Environment Support

EnvVault supports creating separate encrypted files for different environments. For example:

- `.env.development.enc`: Development environment.
- `.env.production.enc`: Production environment.

Specify the environment name using the `--env` parameter in CLI commands.

---

## Contributing

Issues and Pull Requests are welcome!

---

## License

MIT
