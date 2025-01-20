# MyVenv

MyVenv is a simple Windows utility that helps you create or activate a Python virtual environment directly in the current CMD shell. With MyVenv, you can streamline your virtual environment management workflow using a single command.

## Features
- Automatically creates a virtual environment if it doesn't exist.
- Activates the virtual environment in the current CMD shell.
- Adds the virtual environment folder to `.gitignore` to prevent accidental commits.

## Installation

You can install MyVenv via pip:

```sh
pip install myvenv
```

## Usage

After installing MyVenv, you can use the `myvenv.bat` script in your terminal to create or activate a virtual environment.

### Command Syntax
```cmd
myvenv [ENV_NAME]
```

- `ENV_NAME` (optional): The name of the virtual environment folder. Defaults to `venv` if not provided.

### Examples

#### Create and Activate Default Virtual Environment
```cmd
myvenv
```
This creates (if it doesn't already exist) and activates a virtual environment named `venv`.

#### Create and Activate a Custom Virtual Environment
```cmd
myvenv mycustomenv
```
This creates (if it doesn't already exist) and activates a virtual environment named `mycustomenv`.

## How It Works
1. **Environment Name**: The script checks for the provided environment name or defaults to `venv`.
2. **Virtual Environment Creation**: If the specified folder doesn't exist, it creates a virtual environment using `python -m venv`.
3. **Git Ignore Update**: The script ensures the virtual environment folder is listed in `.gitignore` to prevent accidental commits.
4. **Activation**: The script activates the virtual environment in the current CMD shell.

## Project Structure
- `myvenv.bat`: Batch script for managing virtual environments.
- `setup.py`: Python setup script for packaging and distribution.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to submit a pull request or open an issue.

## Author
ILikeAI (Josh)  
[GitHub Profile](https://github.com/ILikeAI)

joshlikesai@gmail.com

## Feedback

If you encounter any issues or have ideas for improvement, please let us know by creating an issue in the [GitHub repository](https://github.com/ILikeAI/myvenv).

