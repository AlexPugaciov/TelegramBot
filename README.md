# Telegram EventBot

This project is a Telegram bot built using the Aiogram library. The bot is designed to manage event participants, allowing users to add and remove players, and update weather information.

## Features

- **Participant Management:** Users can mark their participation, add, and remove other players.
- **Weather Updates:** Weather Updates: The bot sends current weather information at a scheduled time.
- **Interactive Buttons:** Buttons in messages for user interaction.
- **Redis Integration:** Uses Redis for bot state and data storage.



## Installation

1. **Clone the repository:**
```bash
    git clone https://gitlab.skillbox.ru/aleksandr_pugachiov/python_basic_diploma.git
    cd <repository_folder>
```
2. **Create a virtual environment and activate it:**
```bash
    python -m venv venv
    source venv/bin/activate   # For Windows use venv\Scripts\activate
```
3. **Install dependencies:**
```bash
    pip install -r requirements.txt
```
4. **Configure environment variables:**

Create a .env file and specify the parameters for your bot and Redis:
```env
    TOKEN=your_bot_token
    REDIS=your_redis_password
    REDIS_HOST=your_redis_server_address
    WEATHER_API=your_weather_api_key
```
5. **Run**
To start the bot, use the command:
```bash
    python main.py
```

## Key Components
- main.py: Main script for launching the bot. Configures the bot and task scheduler.
- redisdb.py: Module for interacting with Redis. Contains functions for handling data and variables.
- buttons.py: Defines buttons for user interaction.
- weather.py: Module for fetching weather data.
- state.py: Defines states for managing input processes.
- utils.py: Utility and helper functions.
- handlers.py: Manages user actions through buttons and commands, updates the list of participants, and keeps information in the chat current.


## Code Description

This project uses a Telegram bot written with the Aiogram library. The main functionality includes sending and editing messages with weather information and managing a list of players.

1. ### Importing Libraries and Initialization:
    - Necessary modules from the Aiogram library and other helper modules, such as weather, redisdb, buttons, config, etc., are imported.
    - The bot, router, and Redis connection are initialized for storing data about current sessions and variables.
2. ### Function send_message:

    - Sends a message with the weather forecast and control buttons.
    - Pins the message in the chat and saves its ID in Redis.
3. ### Function *edit_message*:

    - Edits the current message, adding the updated weather forecast and player list.
    - Shows the time of the last update.
4. ### Handler for the /start Command:

    - Initializes the variables needed for the bot. 
    - Sends a welcome message and pins the main message in the chat.
5. ### Handler *process_callback*:

    - Handles button presses ("I'm going", "Not going", "Add player", "Remove player").
    - Adds and removes players from the list and displays corresponding notifications.
6. ### Handlers for *GuestName.Name* and *GuestName.del_Name* States:

    - Responsible for adding and removing player names from the list.
    - Updates the message with current data.
7. ### Handler for Incorrect Messages:

    - Deletes messages that arrive in the wrong topic (thread).

## Functions

- ### dict_to_string(d: dict)

  - The function takes a dictionary where the keys are user IDs and the values are dictionaries with player names and timestamps. It returns a string representing a sorted list of players with timestamps.
- ### get_next_day(day, hour, minute)

  - The function calculates the date and time for the next specified day of the week and time. Returns a datetime object with the corresponding value.
- ### get_weather(api_key, city, target_times)

  - The function requests weather data for a given city using the OpenWeatherMap API. Returns a string with the weather forecast for the nearest specified times.
- ### get_weather_next_day()

  - The function calls get_weather with parameters to get the weather forecast for the following days. Parameters include the API key, city name, and target times.    

## Usage
    
### Commands
       
- ***/start:*** Initializes the bot and starts it. Sets initial parameters and sends a message with weather information.
        
### Handling CallbackQuery

- ✅ I'm going: Adds the user to the list of participants.
- ❌ Not going: Removes the user from the list of participants.
- ✅ Add player: Prompts for the player's name to add.
- ❌ Remove player: Removes a player from the list by name.
- Update weather: Updates the message with weather information.



## Notes
    
- The bot uses Redis to store the state and information about current participants.
- Ensure that Redis is running and accessible at the specified address and port.
- The OpenWeatherMap API is used for weather data retrieval. Make sure you have a valid API key.

