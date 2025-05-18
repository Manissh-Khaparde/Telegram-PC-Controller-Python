# 📡 Telegram PC Controller in Python

![GitHub Repo Stars](https://img.shields.io/github/stars/Manissh-Khaparde/Telegram-PC-Controller-Python?style=social) ![GitHub Forks](https://img.shields.io/github/forks/Manissh-Khaparde/Telegram-PC-Controller-Python?style=social) ![GitHub Issues](https://img.shields.io/github/issues/Manissh-Khaparde/Telegram-PC-Controller-Python)

## Overview

Welcome to the **Telegram PC Controller** repository! This project allows you to control your PC remotely using a Telegram bot. Built with Python, it offers a simple yet powerful way to manage your computer from anywhere. 

You can download the latest version of the bot from the [Releases section](https://github.com/Manissh-Khaparde/Telegram-PC-Controller-Python/releases). Make sure to download and execute the necessary files to get started.

## Features

- **Remote Control**: Manage your PC from your mobile device.
- **Easy Setup**: Quick installation and configuration process.
- **Multiple Commands**: Execute various commands on your PC.
- **Real-Time Feedback**: Get immediate responses from your PC.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following:

- Python 3.6 or higher
- Telegram account
- Basic knowledge of Python

### Installation

1. **Clone the Repository**

   Open your terminal and run:

   ```bash
   git clone https://github.com/Manissh-Khaparde/Telegram-PC-Controller-Python.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd Telegram-PC-Controller-Python
   ```

3. **Install Required Libraries**

   Use pip to install the necessary libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Your Telegram Bot**

   - Create a new bot using the [BotFather](https://t.me/botfather) on Telegram.
   - Obtain your bot token and save it in a `.env` file in the project directory.

   Example `.env` file:

   ```
   TELEGRAM_TOKEN=your_bot_token_here
   ```

5. **Run the Bot**

   Start the bot by executing:

   ```bash
   python main.py
   ```

### Commands

The bot supports several commands for remote control. Here are a few examples:

- **/start**: Initialize the bot.
- **/shutdown**: Shut down the PC.
- **/restart**: Restart the PC.
- **/sleep**: Put the PC to sleep.
- **/status**: Get the current status of the PC.

You can add more commands as needed by modifying the `commands.py` file.

## Libraries Used

This project utilizes several libraries to function effectively:

- **psutil**: For system and process utilities.
- **pyautogui**: For controlling the mouse and keyboard.
- **dotenv**: For managing environment variables.
- **shutil**: For file operations.
- **signal**: For handling signals.
- **subprocess**: For running shell commands.
- **telebot**: For interacting with the Telegram Bot API.
- **time**: For time-related functions.

## Troubleshooting

If you encounter issues while running the bot, consider the following:

- Ensure your Python version is compatible.
- Check your internet connection.
- Verify your bot token is correct.
- Review the logs for any error messages.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to create a pull request. Please ensure your code follows the project's style guidelines.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of the libraries used in this project.
- Special thanks to the open-source community for their support and resources.

## Conclusion

The **Telegram PC Controller** is a versatile tool for anyone looking to manage their computer remotely. With easy setup and a range of features, it provides a seamless experience. Download the latest version from the [Releases section](https://github.com/Manissh-Khaparde/Telegram-PC-Controller-Python/releases) and start controlling your PC today!

Feel free to reach out with any questions or feedback. Happy coding!