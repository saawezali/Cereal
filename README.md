# 🥣 Cereal Discord Bot

A feature-rich Discord bot with moderation, games, music, memes, and utility commands.

## ✨ Features

### 🛡️ Moderation
- `/kick` - Kick members
- `/ban` / `/unban` - Ban/unban members
- `/mute` / `/unmute` - Timeout members
- `/clear` - Bulk delete messages
- `/warn` - Warn members
- `/slowmode` - Set channel slowmode

### 🎮 Games
- `!truthordare` / `!tod` - Play Truth or Dare
- `!wouldyourather` / `!wyr` - Would You Rather questions
- `!neverhaveiever` / `!nhie` - Never Have I Ever
- `!8ball` - Ask the magic 8-ball
- `!rps` - Rock Paper Scissors
- `!flip` - Flip a coin
- `!roll` - Roll dice

### 😂 Fun & Memes
- `!meme` - Get random memes from Reddit
- `!dadjoke` - Get a dad joke
- `!fact` - Random facts
- `!roast` - Roast someone
- `!compliment` - Compliment someone
- `!ship` - Ship two users
- `!avatar` - View user's avatar
- `!userinfo` - Get user information
- `!serverinfo` - Get server information

### 🔧 Utility
- `!remind` - Set reminders
- `!reminders` - View your reminders
- `!poll` - Create a poll
- `!suggest` - Submit suggestions
- `!timer` - Start a countdown
- `!calculate` - Calculator
- `!ping` - Check bot latency
- `!say` - Make bot say something (mod only)
- `!embed` - Create custom embeds (mod only)

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
```bash
cp .env.example .env
```
Edit `.env` and add your Discord bot token:
```
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=None
```

4. **Run the bot**
```bash
python bot.py
```

## 🎮 Usage

Cereal supports both **slash commands** (`/`) and **prefix commands** (`!`):

```
/ping          or    !ping
/meme          or    !meme
/kick @user    or    !kick @user
```

Slash commands have autocomplete and parameter hints for better UX!

## 📁 Project Structure

```
cereal-bot/
│
├── bot.py                 # Main bot file
├── cogs/
│   ├── moderation.py     # Moderation commands
│   ├── games.py          # Game commands
│   ├── music.py          # Music commands
│   ├── fun.py            # Fun & meme commands
│   └── utility.py        # Utility commands
│
├── .env                  # Environment variables (create from .env.example)
├── .env.example          # Example environment file
├── requirements.txt      # Python dependencies
└── README.md            # This file
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

- [ ] Database integration (PostgreSQL/SQLite)
- [ ] Leveling system with XP and ranks
- [ ] Auto-moderation (spam filter, bad word filter)
- [ ] Custom prefix per server
- [ ] Economy system
- [ ] Giveaway system
- [ ] Tickets system
- [ ] Web dashboard
- [ ] Logging system
- [ ] Music system (requires Lavalink setup - currently disabled)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📜 License

This project is licensed under the MIT License.

## 🙏 Credits

- Built with [discord.py](https://github.com/Rapptz/discord.py)
- Music powered by [Lavalink](https://github.com/freyacodes/Lavalink)
- Memes from Reddit
- Jokes from various APIs

## 📧 Support

For issues or questions, please:
- Open an issue on GitHub
- Join our Discord server (coming soon)

---

Made with ❤️ and ☕ by [Your Name]