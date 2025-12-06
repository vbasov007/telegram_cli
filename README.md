# Telegram CLI Sender

A command-line tool to send Telegram messages with attachments to specified users.

## Features

- Send text messages or load message content from .txt/.md files
- Send files as attachments (photos, videos, documents, audio)
- Support for multiple attachments in a single command
- Automatic file type detection (photos, videos, documents, etc.)
- Send to users by username, phone number, or user ID

## Setup

### 1. Install Dependencies

First, activate your virtual environment and install the required packages:

```bash
.venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 2. Get Telegram API Credentials

1. Go to https://my.telegram.org/auth
2. Log in with your phone number
3. Navigate to 'API development tools'
4. Create a new application (if you don't have one)
5. Copy your `api_id` and `api_hash`

### 3. Configure the Application

1. Copy the example config file:
   ```bash
   copy telegram_send_config.ini.example telegram_send_config.ini
   ```

2. Edit `telegram_send_config.ini` and add your credentials:
   ```ini
   api_id = YOUR_API_ID
   api_hash = YOUR_API_HASH
   ```

### 4. First Run

On the first run, you'll be prompted to log in with your phone number and enter the verification code sent to your Telegram account. This creates a session file that will be reused for subsequent runs.

## Building Executable

If you want to create a standalone .exe file that doesn't require Python to be installed:

### Method 1: Using the Batch Script (Windows)

```bash
# Activate your virtual environment
.venv\Scripts\activate

# Run the build script
build.bat
```

### Method 2: Using the Python Build Script (Cross-platform)

```bash
# Activate your virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Run the build script
python build.py
```

### Method 3: Using the Spec File (Advanced)

For customized builds with additional options:

```bash
# Activate your virtual environment
.venv\Scripts\activate

# Run the spec-based build
build_with_spec.bat
# Or
python -m PyInstaller telegram_send.spec
```

### After Building

The executable will be created at `dist\telegram_send.exe`. To use it:

1. Copy `telegram_send.exe` to your desired location
2. Copy or create `telegram_send_config.ini` in the same directory as the .exe
3. Run the executable from command line:
   ```bash
   telegram_send.exe @username "Hello!"
   ```

Note: The first time you run the .exe, it will create a session file in the same directory.

## Usage

### Basic Syntax

```bash
python telegram_send.py <recipient> "<message>" [options]
```

### Examples

#### Send a text message:

```bash
python telegram_send.py @username "Hello, World!"
python telegram_send.py +1234567890 "Hello!"
python telegram_send.py 123456789 "Hello by user ID!"
```

#### Send message from a file:

You can load message content from .txt or .md files:

```bash
python telegram_send.py @username message.txt
python telegram_send.py @username announcement.md
```

This is useful for:
- Long messages with formatting
- Pre-written announcements
- Markdown-formatted content
- Messages with multiple lines

#### Send a message with an attachment:

```bash
python telegram_send.py @username "Check this photo!" -a photo.jpg
python telegram_send.py @username "Here's a document" -a report.pdf
```

#### Send message from file with attachments:

```bash
python telegram_send.py @username message.txt -a photo.jpg -a document.pdf
```

#### Send multiple attachments:

```bash
python telegram_send.py @username "Multiple files" -a file1.pdf -a photo.jpg -a video.mp4
```

#### Send attachment without text message:

```bash
python telegram_send.py @username -a document.pdf
```

### Recipient Formats

- **Username**: `@username` (with @ prefix)
- **Phone number**: `+1234567890` (with + and country code)
- **User ID**: `123456789` (numeric ID)

### Supported File Types

The tool automatically detects file types and sends them appropriately:

- **Photos**: .jpg, .jpeg, .png, .gif, .bmp, .webp
- **Videos**: .mp4, .avi, .mkv, .mov, .webm
- **Audio**: .mp3, .wav, .ogg, .m4a, .flac
- **Voice**: .ogg, .opus (sent as voice messages)
- **Documents**: All other file types

### Command-line Options

```
positional arguments:
  recipient             Recipient username (with @), phone number (with +), or user ID
  message              Message text or path to .txt/.md file (optional if attachments are provided)

optional arguments:
  -h, --help           Show help message
  -a, --attachment     File to attach (can be used multiple times)
```

### Message Files

When providing a message, you can either:
1. **Pass text directly**: `"Your message here"`
2. **Reference a file**: `message.txt` or `message.md`

The script automatically detects if the message parameter is a .txt or .md file and reads its content. This is particularly useful for:
- Sending formatted markdown messages
- Managing long messages in separate files
- Reusing message templates

## Security Notes

- Keep your `telegram_send_config.ini` file secure and never commit it to version control
- The session file (`telegram_cli_session.session`) contains your authentication token
- Add both files to `.gitignore` if using git

## Project Files

### Main Files
- **telegram_send.py** - Main script
- **telegram_send_config.ini** - Your API credentials (not in repo)
- **telegram_send_config.ini.example** - Template for telegram_send_config.ini
- **requirements.txt** - Runtime dependencies
- **requirements-dev.txt** - Development dependencies (PyInstaller)

### Build Scripts
- **build.bat** - Simple Windows batch build script
- **build.py** - Cross-platform Python build script
- **build_with_spec.bat** - Windows batch script using spec file
- **telegram_send.spec** - PyInstaller specification file for advanced builds

### Generated Files (not in repo)
- **telegram_cli_session.session** - Telegram authentication session
- **dist/** - Built executable output directory
- **build/** - PyInstaller build artifacts

## Troubleshooting

### "telegram_send_config.ini not found"
Make sure you've created `telegram_send_config.ini` from `telegram_send_config.ini.example` and filled in your API credentials.

### "File not found" errors
Ensure the attachment files exist and the paths are correct. Use absolute paths if needed.

### "Telegram API error"
Check that your API credentials are correct and your account has permission to send messages to the recipient.

### Authentication issues
Delete the `.session` file and run the script again to re-authenticate.

### Build errors
- Ensure you've activated the virtual environment before building
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Install build dependencies: `pip install -r requirements-dev.txt`
- On Windows, you may need to run the build script as administrator

### Executable not working
- Make sure `telegram_send_config.ini` is in the same directory as the .exe
- The first run will create a session file; ensure you have write permissions
- Try running from Command Prompt to see any error messages

## License

This tool is provided as-is for personal use.
