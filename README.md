# DeadByCat
 Code for the "Dead By Cat" Discord bot


# Shrine of Secrets Bot

## Overview

The Shrine of Secrets Bot is a Discord bot designed for players of the popular game Dead by Daylight. It provides real-time updates on the game's Shrine of Secrets, allowing players to stay informed about the latest perks available without having to leave Discord. The bot fetches data from an external API and presents it in an easy-to-read format directly in your Discord server.

## Features

- **Shrine Updates:** Automatically posts weekly updates about the Shrine of Secrets, including perk names, descriptions, and costs.
- **Perk Information:** Offers detailed information about each perk available in the Shrine, including its usage tier and icon.
- **Commands:**
  - `!shrine`: Manually fetches and displays the current Shrine of Secrets.
  - `!ping`: Checks the bot's responsiveness and connectivity.

## Setup

1. **Clone the Repository:**

2. **Install Dependencies:**

3. **Configure Environment:**
- Create a `.env` file in the project root.
- Add your Discord bot token:
  ```
  DISCORD_TOKEN=your_bot_token_here
  ```

4. **Run the Bot:**


## Usage

- Add the bot to your Discord server using the bot invite link.
- Use `!shrine` to get the latest Shrine of Secrets.
- Use `!ping` to check if the bot is online.

## Configuration

- **config.py**: Contains configuration variables such as the token and scheduled time for automated messages.
- **Scheduled Messages:** To change the scheduled time for automatic Shrine updates, modify the `scheduled_time` variable in `config.py`.

## Project Structure

- `app.py`: The main bot application.
- `/main`: Contains the core functionality.
- `async_def.py`: Asynchronous functions for fetching Shrine data.
- `commands.py`: Defines bot commands.
- `functions.py`: Includes scheduler and other utility functions.
- `config.py`: Configuration file.
- `requirements.txt`: List of project dependencies.

## Contributing

Contributions to the Shrine of Secrets Bot are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

# CPGPU License

## Acknowledgments

- Thanks to the creators of discord.py for their amazing library.
- This bot uses the [Nightlight API](https://api.nightlight.gg) for fetching Shrine of Secrets data.
