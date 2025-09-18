🌦️ Llevo Paraguas? - Your Personal Weather Bot

A friendly, automated Telegram bot that sends you daily weather forecasts for Buenos Aires, so you never have to wonder, "¿Llevo paraguas?" (Should I bring an umbrella?).
✨ Features

    Automated Daily Forecasts: Automatically sends a detailed weather report at scheduled times:

        7:00 AM: Today's forecast to start your day.

        11:00 PM: Tomorrow's forecast so you can plan ahead.

    Smart Notifications: Delivers a human-readable summary with emojis, including highs, lows, chance of rain, and a breakdown for the morning, afternoon, and evening.

    Subscription-Based: Any user can start a conversation with the bot to subscribe to the daily alerts.

    Built to Scale: The broadcasting logic is designed to handle multiple subscribers efficiently.

🛠️ How It Works

The bot is built in Python using the python-telegram-bot library. It fetches comprehensive weather data from the Open-Meteo API, which provides a generous free tier.

The core logic is handled by a long-running application that uses an internal scheduler (JobQueue) to trigger the broadcast messages at the correct times. User subscriptions (chat_ids) are saved locally in a user_data.json file, making the service persistent.
📂 Project Structure

The project is organized into a clean and modular structure:

LlevoParguas/
├── .env              # Environment variables (BOT_TOKEN)
├── app.py            # Main application entry point
├── user_data.json    # Stores subscriber chat IDs
├── requirements.txt  # Project dependencies
└── src/
    ├── functions/
    │   └── broadcast.py # Logic for scheduled message broadcasting
    ├── handlers/
    │   └── handlers.py  # Handles user commands like /start
    └── models/
        ├── users.py       # Manages loading/saving user data
        └── weather_api.py # Fetches and parses data from Open-Meteo

🚀 Getting Started

Follow these instructions to get a local copy up and running.
Prerequisites

    Python 3.10+

    A Telegram Bot Token from BotFather

Installation & Setup

    Clone the repository:

    git clone [https://github.com/your-username/LlevoParguas.git](https://github.com/your-username/LlevoParguas.git)
    cd LlevoParguas

    Create and activate a Python virtual environment:

    python3 -m venv venv
    source venv/bin/activate

    Install the required dependencies:
    (You should create a requirements.txt file for this by running pip freeze > requirements.txt)

    pip install python-telegram-bot python-dotenv openmeteo-requests requests-cache retry-requests pandas

    Create the environment file:
    Create a file named .env in the root directory and add your Telegram Bot Token:

    BOT_TOKEN="YOUR_SUPER_SECRET_BOT_TOKEN"

Running the Bot

Once everything is set up, start the bot with this command:

python3 app.py

The bot will now be running and will send out the scheduled messages.
💬 Usage

To subscribe to the daily weather alerts, simply find the bot on Telegram and press the "Start" button. You will receive a welcome message confirming your subscription.
🔧 Technologies Used

    python-telegram-bot: The library used to interact with the Telegram Bot API.

    Open-Meteo: The weather data provider.

    pandas: For easy data manipulation of the weather forecast.

    python-dotenv: To manage environment variables.