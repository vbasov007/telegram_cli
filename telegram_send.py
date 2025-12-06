#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
from pyrogram import Client
from pyrogram.errors import RPCError


def get_base_path():
    """Get the base path for the application, handling both script and exe."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return Path(sys.executable).parent
    else:
        # Running as script
        return Path(__file__).parent


def load_config():
    base_path = get_base_path()
    config_file = base_path / "telegram_send_config.ini"

    if not config_file.exists():
        print("Error: telegram_send_config.ini not found. Please create it from telegram_send_config.ini.example")
        print(f"Looking for config at: {config_file.absolute()}")
        sys.exit(1)

    config = {}
    with open(config_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()

    required_keys = ['api_id', 'api_hash']
    for key in required_keys:
        if key not in config:
            print(f"Error: {key} not found in telegram_send_config.ini")
            sys.exit(1)

    return config


def load_message_from_file(message_param):
    if not message_param:
        return ''

    if os.path.isfile(message_param):
        file_ext = Path(message_param).suffix.lower()
        if file_ext in ['.txt', '.md']:
            try:
                with open(message_param, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"Loaded message from: {message_param}")
                    return content
            except Exception as e:
                print(f"Error reading message file: {e}")
                sys.exit(1)

    return message_param


def send_message(recipient, message, attachments, config):
    api_id = int(config['api_id'])
    api_hash = config['api_hash']

    base_path = get_base_path()
    session_path = str(base_path / "telegram_cli_session")

    app = Client(
        session_path,
        api_id=api_id,
        api_hash=api_hash
    )

    with app:
        try:
            if attachments:
                for attachment in attachments:
                    if not os.path.exists(attachment):
                        print(f"Error: File not found: {attachment}")
                        continue

                    file_path = Path(attachment)
                    file_ext = file_path.suffix.lower()

                    caption = message if message else None

                    if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                        app.send_photo(recipient, attachment, caption=caption)
                        print(f"Sent photo: {attachment}")
                    elif file_ext in ['.mp4', '.avi', '.mkv', '.mov', '.webm']:
                        app.send_video(recipient, attachment, caption=caption)
                        print(f"Sent video: {attachment}")
                    elif file_ext in ['.mp3', '.wav', '.ogg', '.m4a', '.flac']:
                        app.send_audio(recipient, attachment, caption=caption)
                        print(f"Sent audio: {attachment}")
                    elif file_ext in ['.ogg', '.opus']:
                        app.send_voice(recipient, attachment, caption=caption)
                        print(f"Sent voice: {attachment}")
                    else:
                        app.send_document(recipient, attachment, caption=caption)
                        print(f"Sent document: {attachment}")

                    message = None
            else:
                if message:
                    app.send_message(recipient, message)
                    print(f"Message sent to {recipient}")
                else:
                    print("Error: No message or attachments provided")
                    sys.exit(1)

            print("Operation completed successfully!")

        except RPCError as e:
            print(f"Telegram API error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Send Telegram messages with attachments from command line',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Send a text message:
    python telegram_send.py @username "Hello, World!"
    python telegram_send.py +1234567890 "Hello!"

  Send message from file:
    python telegram_send.py @username message.txt
    python telegram_send.py @username message.md

  Send a message with attachment:
    python telegram_send.py @username "Check this out!" -a photo.jpg

  Send message from file with attachments:
    python telegram_send.py @username message.txt -a photo.jpg -a doc.pdf

  Send multiple attachments:
    python telegram_send.py @username "Files attached" -a file1.pdf -a file2.jpg

  Send attachment without message:
    python telegram_send.py @username -a document.pdf
        """
    )

    parser.add_argument(
        'recipient',
        help='Recipient username (with @), phone number (with +), or user ID'
    )

    parser.add_argument(
        'message',
        nargs='?',
        default='',
        help='Message text or path to .txt/.md file (optional if attachments are provided)'
    )

    parser.add_argument(
        '-a', '--attachment',
        action='append',
        dest='attachments',
        help='File to attach (can be used multiple times)'
    )

    args = parser.parse_args()

    if not args.message and not args.attachments:
        parser.error("Either message or attachment must be provided")

    message = load_message_from_file(args.message)

    config = load_config()
    send_message(args.recipient, message, args.attachments, config)


if __name__ == '__main__':
    main()
