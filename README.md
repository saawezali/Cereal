# 🥣 Cereal Discord Bot

A feature-rich Discord bot with moderation, games, fun commands, and utility tools.

## ✨ Features

### 🛡️ Moderation
- `/kick` - Kick members from the server
- `/ban` / `/unban` - Ban/unban members
- `/mute` / `/unmute` - Timeout members
- `/clear` - Bulk delete messages
- `/warn` - Warn members
- `/slowmode` - Set channel slowmode

### 🎮 Games
- `/truthordare` - Play Truth or Dare
- `/wouldyourather` - Would You Rather questions
- `/neverhaveiever` - Never Have I Ever
- `/8ball` - Ask the magic 8-ball
- `/rps` - Rock Paper Scissors
- `/flip` - Flip a coin
- `/roll` - Roll dice

### 😂 Fun & Memes
- `/meme` - Get random memes from Reddit
- `/dadjoke` - Get a dad joke
- `/fact` - Random facts
- `/roast` - Roast someone
- `/compliment` - Compliment someone
- `/quote` - Get inspirational quotes
- `/ship` - Ship two users together
- `/avatar` - View user's avatar
- `/userinfo` - Get user information
- `/serverinfo` - Get server information

### 🔧 Utility
- `/remind` - Set reminders
- `/reminders` - View your active reminders
- `/poll` - Create interactive polls
- `/afk` - Set AFK status
- `/suggest` - Submit suggestions
- `/timer` - Start a countdown timer
- `/calculate` - Calculate mathematical expressions
- `/ping` - Check bot latency
- `/say` - Make bot say something
- `/embed` - Create custom embeds
- `/timezone` - Check time in any timezone (with autocomplete)
- `/help` - Show all available commands

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/cereal-bot.git
cd cereal-bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
Create a `.env` file in the root directory:
```
DISCORD_TOKEN=your_bot_token_here
```

4. **Run the bot**
```bash
python bot.py
```

## 🎮 Usage

Cereal primarily uses **slash commands** (`/`) for the best user experience:

```
/ping
/meme
/kick @user
/timezone Tokyo
/compliment @user
```

Slash commands provide:
- **Autocomplete** for parameters (like timezone locations)
- **Parameter hints** and validation
- **Better mobile experience**
- **Permission checking** built into Discord

Some legacy prefix commands (`!`) may still work but are being phased out.

## 📁 Project Structure

```
cereal-bot/
│
├── bot.py                 # Main bot file
├── cogs/
│   ├── moderation.py     # Moderation commands
│   ├── games.py          # Game commands
│   ├── fun.py            # Fun & meme commands
│   └── utility.py        # Utility commands
│
├── .env                  # Environment variables (create from .env.example)
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── CONTRIBUTING.md      # Developer documentation
```

## 🔑 Getting Your Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" section
4. Click "Add Bot"
5. Under "Token", click "Copy" to get your bot token
6. Enable these **Privileged Gateway Intents**:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
7. Go to "OAuth2" > "URL Generator"
8. Select scopes: `bot` and `applications.commands`
9. Select permissions you need (Administrator for all features)
10. Use the generated URL to invite your bot

## 🛠️ Customization

### Change Command Prefix
Edit `bot.py`:
```python
command_prefix='!'  # Change to your preferred prefix
```

### Add More Commands
Create new commands in the appropriate cog file or create a new cog in `cogs/`.

### Customize Bot Status
Edit `bot.py` in the `on_ready` function:
```python
await self.change_presence(
    activity=discord.Game(name="Your custom status")
)
```

## 📝 To-Do / Future Features

- [x] Slash command conversion (completed)
- [x] Permission system for moderation commands (completed)
- [x] Autocomplete for timezone command (completed)
- [x] API integration for dynamic content (completed)
- [ ] Database integration (PostgreSQL/SQLite)
- [ ] Leveling system with XP and ranks
- [ ] Auto-moderation (spam filter, bad word filter)
- [ ] Custom prefix per server
- [ ] Economy system
- [ ] Giveaway system
- [ ] Tickets system
- [ ] Web dashboard
- [ ] Advanced logging system
- [ ] Weather command
- [ ] Translation command

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📜 License

This project is licensed under the MIT License.

## 🙏 Credits

- Built with [discord.py](https://github.com/Rapptz/discord.py)
- Memes from Reddit API
- Dad jokes from [icanhazdadjoke](https://icanhazdadjoke.com/)
- Facts from [uselessfacts.jsph.pl](https://uselessfacts.jsph.pl/)
- Quotes from [zenquotes.io](https://zenquotes.io/)
- Evil insults from [evilinsult.com](https://evilinsult.com/)
- Timezone data from [pytz](https://pythonhosted.org/pytz/)

## 📧 Support

For issues or questions, please:
- Open an issue on GitHub
- Join our Discord server (coming soon)

---

Made with ❤️ by Saawez Ali