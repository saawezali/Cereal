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
- `/weather` - Get weather information (requires API key)
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
Create a `.env` file in the root directory by copying `.env.example`:
```bash
cp .env.example .env
```
Then edit `.env` with your actual values:
```
DISCORD_TOKEN=your_bot_token_here
WEATHER_API_KEY=your_openweather_api_key_here  # Optional
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
├── bot.py                 # Main bot file with health check server
├── core/                  # Core functionality
│   ├── __init__.py       # Core module exports
│   ├── config.py         # Configuration management
│   ├── constants.py      # Bot constants and settings
│   └── logger.py         # Structured logging
├── db/                    # Database module
│   ├── __init__.py       # Database exports
│   ├── base.py           # Database connection & operations
│   ├── models.py         # SQLAlchemy models
│   ├── repository.py     # Repository pattern implementation
│   └── migration/        # Database migration scripts
│       ├── __init__.py
│       ├── base.py       # Migration utilities
│       └── example_migration.py
├── cogs/                  # Feature modules (cogs)
│   ├── moderation.py     # Moderation commands
│   ├── games.py          # Game commands
│   ├── fun.py            # Fun & meme commands
│   └── utility.py        # Utility commands
├── scripts/               # Utility scripts
│   └── backup_db.py      # Database backup script
├── tests/                 # Unit tests
│   └── test_basic.py     # Basic functionality tests
│
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker containerization
├── docker-compose.yml   # Docker Compose configuration
├── README.md            # This file
├── LICENSE              # MIT License
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

## ➕ Invite Your Bot to Servers

Once your bot is public, others can add it to their servers:

### Make Your Bot Public
1. In [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your bot → "Bot" section
3. Turn **ON** "Public Bot" 
4. Keep "Requires OAuth2 Code Grant" **OFF**

### Generate Invite Link
1. Go to "OAuth2" → "URL Generator"
2. Select scopes: `bot` and `applications.commands`
3. Select permissions:
   - Send Messages
   - Use Slash Commands
   - Read Message History
   - Embed Links
   - Attach Files
   - Add Reactions
   - Kick Members (for moderation)
   - Ban Members (for moderation)
   - Manage Messages (for moderation)
4. **Copy the generated URL** and share it!

### Share Your Bot
- **Direct Link:** Share the OAuth2 URL with server owners
- **GitHub:** Add the invite link to your repository
- **Bot Lists:** Submit to sites like top.gg, discordbotlist.com
- **Communities:** Share in Discord bot development servers

**Invite Link Format:** `https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=PERMISSIONS&scope=bot%20applications.commands`

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

## � Deployment

### Local Development
```bash
# Clone and setup
git clone https://github.com/yourusername/cereal-bot.git
cd cereal-bot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your tokens
python bot.py
```

### Production Deployment

#### Option 1: Docker (Recommended)
```dockerfile
# Add this Dockerfile to your project
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "bot.py"]
```

```bash
docker build -t cereal-bot .
docker run -d --env-file .env cereal-bot
```

#### Option 2: Systemd Service (Linux)
Create `/etc/systemd/system/cereal-bot.service`:
```ini
[Unit]
Description=Cereal Discord Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/cereal-bot
ExecStart=/path/to/venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable cereal-bot
sudo systemctl start cereal-bot
```

#### Option 3: PM2 (Node.js process manager, works with Python)
```bash
npm install -g pm2
pm2 start bot.py --name cereal-bot --interpreter python3
pm2 startup
pm2 save
```

### Environment Variables for Production
- Set `LOG_LEVEL=WARNING` for production
- Use a production database URL if needed
- Set up proper monitoring and alerts

## 📊 Monitoring & Health Checks

The bot includes built-in health monitoring:

- **Health Check Endpoint**: `http://localhost:8080/health`
- **Metrics Available**:
  - Bot status and uptime
  - Guild and user counts
  - Discord API latency
  - Memory usage

### Using Health Checks

```bash
# Check bot health
curl http://localhost:8080/health

# Expected response:
{
  "status": "healthy",
  "bot_name": "Cereal#9626",
  "guilds": 5,
  "users": 1250,
  "latency": 45.67,
  "uptime": "3600.5"
}
```

### Database Backups

Automated database backups are available:

```bash
# Create backup
python scripts/backup_db.py

# List available backups
python scripts/backup_db.py list
```

Backups are stored in the `backups/` directory with timestamps.

## 🧪 Testing & Quality Assurance

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest tests/ -v

# Run with coverage
pip install pytest-cov
python -m pytest tests/ --cov=. --cov-report=html
```

### Code Quality

```bash
# Check syntax
python -m py_compile bot.py core/*.py db/*.py cogs/*.py

# Lint code
pip install flake8
flake8 . --max-line-length=127 --max-complexity=10
```

### CI/CD Pipeline

The project includes GitHub Actions for automated testing:

- **Multi-Python Version Testing**: Python 3.8-3.11
- **Syntax Validation**: Automatic compilation checks
- **Code Quality**: Flake8 linting
- **Automated Deployment**: Ready for production deployment

## 🔒 Security Features

- **Input Validation**: All user inputs are validated and sanitized
- **Rate Limiting**: Built-in cooldowns prevent spam
- **Secure Token Storage**: Environment variables for sensitive data
- **Permission Checks**: Discord permission system integration
- **Error Handling**: Comprehensive error handling without data leakage

- [x] Slash command conversion (completed)
- [x] Permission system for moderation commands (completed)
- [x] Autocomplete for timezone command (completed)
- [x] API integration for dynamic content (completed)
- [x] Database integration (SQLite) (completed)
- [x] XP system removal (completed)
- [ ] Unit tests and integration tests
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Health check endpoints
- [ ] Database migrations system
- [ ] Error monitoring (Sentry)
- [ ] Auto-moderation (spam filter, bad word filter)
- [ ] Custom prefix per server
- [ ] Economy system
- [ ] Giveaway system
- [ ] Tickets system
- [ ] Web dashboard
- [ ] Advanced logging system
- [ ] Translation command

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## � Legal & Policies

- **[Privacy Policy](PRIVACY_POLICY.md)** - How we handle your data
- **[Terms of Service](TERMS_OF_SERVICE.md)** - Usage rules and guidelines
- **[License](LICENSE)** - MIT License terms

## �📜 License

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