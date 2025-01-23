# PyRexBot

<p align="center">
  <img src="https://i.ibb.co/vVx1xfb/Picsart-25-01-20-22-05-41-616.png" alt="PyRexBot Logo" width="300"/>
</p>

**PyRexBot** simplifies Telegram bot development with an intuitive interface for commands, messaging, buttons, and more. Build interactive Telegram bots effortlessly, from basic to advanced, with clean and reusable code.

---

## 🚀 Features

- **Easy Command Handling**: Add commands with simple callbacks.
- **Message Processing**: Handle messages with text or media filters.
- **Interactive Buttons**: Create inline keyboard buttons with ease.
- **Advanced Functionalities**: Support for inline queries, message editing, file sharing, and more.
- **Fully Asynchronous**: Built on `python-telegram-bot` 20.0+ for fast and reliable performance.
- **Error Handling**: Add custom global error handlers for debugging.

---

## 🛠 Installation

Install PyRexBot using pip:

```bash
pip install PyRexBot
```

---

## 📦 Quick Start

Here’s how you can build a basic bot in minutes:

```python
from PyRexBot import PyRexBot

# Initialize the bot
bot = PyRexBot("YOUR_TELEGRAM_BOT_TOKEN")

# Define a command
async def start_command(update, context):
    await bot.reply(update, "Welcome to PyRexBot!")

# Add the command
bot.add_command("start", start_command)

# Run the bot
bot.start()
```

---

## 📚 Examples

### 1. Adding Inline Buttons

```python
async def button_example(update, context):
    buttons = [("Click Me", "button_callback")]
    await bot.reply(update, "Here's a button!", buttons=buttons)

bot.add_command("button", button_example)
```

### 2. Sending Media (Photo)

```python
async def send_photo_example(update, context):
    await bot.send_photo(update.message.chat_id, "https://example.com/image.jpg", caption="Look at this!")

bot.add_command("photo", send_photo_example)
```

### 3. Handling Inline Queries

```python
async def inline_query_handler(update, context):
    # Handle inline query logic here
    pass

bot.add_inline_query_handler(inline_query_handler)
```

---

## 🛠 Full API Reference

### Core Methods:
- **`add_command(name: str, callback)`**: Add a new command (e.g., `/start`).
- **`add_message_handler(callback, text_only=True)`**: Handle text or media messages.
- **`add_button_handler(callback)`**: Handle inline button clicks.
- **`add_inline_query_handler(callback)`**: Handle inline queries.
- **`send_message(chat_id, text, buttons=None)`**: Send a message with optional buttons.
- **`send_photo(chat_id, photo, caption=None, buttons=None)`**: Send a photo with optional caption and buttons.
- **`reply(update, text, buttons=None)`**: Reply to a user’s message.
- **`edit_message(chat_id, message_id, text, buttons=None)`**: Edit a previously sent message.
- **`delete_message(chat_id, message_id)`**: Delete a message.

For a full list of methods and examples, check out the [Wiki](https://github.com/TraxDinosaur/PyRexBot/wiki/PyRexBot).

---

## 🐛 Issues

Encountered a bug or need help? Report it [here](https://github.com/TraxDinosaur/PyRexBot/issues).

---

## 📜 License

This project is licensed under the **CC-BY-SA 4.0**. See the [LICENSE](https://github.com/TraxDinosaur/PyRexBot/blob/main/LICENSE) for details.

---

## 🌟 Acknowledgments

Big thanks to the contributors of `python-telegram-bot` for the robust foundation, and to the developers and testers who helped shape **PyRexBot**.

---

## 📬 Contact

- **Author**: [TraxDinosaur](https://github.com/TraxDinosaur)  
- **Website**: [TraxDinosaur.github.io](https://traxdinosaur.github.io)  
- **GitHub**: [TraxDinosaur](https://github.com/TraxDinosaur)  

---

Happy Bot Building with PyRexBot! 🦖🤖