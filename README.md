# Cereal Discord Bot

**Enhance your Discord server with fun, moderation, and utility features!**

Cereal is a comprehensive Discord bot designed to make your server more engaging and easier to manage. With over 40 commands across moderation, games, entertainment, and utilities, Cereal helps create a better community experience for everyone.

## 🤖 Invite Cereal to Your Server

[![Add to Discord](https://img.shields.io/badge/Add_to_Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/api/oauth2/authorize?client_id=1368984903559155833&permissions=8&scope=bot%20applications.commands)

## ✨ Features

### 🛡️ Moderation Tools
Keep your server safe and organized with powerful moderation commands:
- Member management (kick, ban, mute, warn)
- Message cleanup and slowmode
- Automated moderation features

### 🎮 Games & Entertainment
Make your server more fun with interactive games and entertainment:
- Truth or Dare, Would You Rather, Never Have I Ever
- Magic 8-ball, Rock Paper Scissors, coin flips, dice rolls
- Random memes, dad jokes, and fun interactions

### 😂 Fun Commands
Lighten up your server with fun and social features:
- Roast and compliment commands
- User shipping and avatar viewing
- Inspirational quotes and random facts

### 🔧 Utility Features
Helpful tools for server management and daily use:
- Reminders and timers
- Interactive polls and suggestions
- Timezone conversion and weather information
- Custom embeds and message formatting
- Server and user information displays

## 🚀 Getting Started

### For Server Admins:
1. **Invite the bot** using the link above
2. **Set permissions** - Give the bot appropriate roles and permissions
3. **Configure settings** - Use `/help` to see available commands
4. **Test commands** - Try `/ping` to verify the bot is working

### For Members:
- Use `/help` to see all available commands
- Start with fun commands like `/meme` or `/8ball`
- Explore moderation features if you have permissions

## 📋 Commands Overview

| Category | Commands |
|----------|----------|
| **Moderation** | kick, ban, mute, warn, clear, slowmode |
| **Games** | truthordare, wouldyourather, 8ball, rps, flip, roll |
| **Fun** | meme, dadjoke, roast, compliment, ship, avatar |
| **Utility** | remind, poll, timer, weather, timezone, ping |

## ⚙️ Setup & Permissions

### Required Permissions:
- **Send Messages** - To respond to commands
- **Use Slash Commands** - For all bot interactions
- **Embed Links** - For rich message formatting
- **Read Message History** - For context-aware commands

### Optional Permissions (for full functionality):
- **Manage Messages** - For moderation commands
- **Manage Roles** - For mute/unmute features
- **Manage Channels** - For slowmode
- **Mention Everyone** - For announcements

## 🔒 Privacy & Terms

Cereal respects your privacy and follows Discord's guidelines:

- **[Privacy Policy](https://saawezali.github.io/Cereal/privacy-policy.html)** - How we handle your data
- **[Terms of Service](https://saawezali.github.io/Cereal/terms-of-service.html)** - Usage rules and guidelines

## 🆘 Support & Help

### Getting Help:
- Use `/help` command in Discord for a full list of commands
- Check command-specific help with `/command_name help`

### Issues & Questions:
- **GitHub Issues**: [Report bugs or request features](https://github.com/saawezali/Cereal/issues)
- **Discord Support**: Join our support server (coming soon)

### Common Issues:
- **Bot not responding?** Check if it has proper permissions
- **Commands not working?** Try `/ping` to test connectivity
- **Missing features?** Some commands require specific permissions

## 📊 Bot Statistics

- **Commands**: 40+ available features
- **Uptime**: 99%+ reliability
- **Support**: Active development and maintenance

## 🎯 Why Choose Cereal?

- ✅ **Free to use** - No premium features or paywalls
- ✅ **Regular updates** - New features added frequently
- ✅ **Community focused** - Built for Discord communities
- ✅ **Easy setup** - Simple invite and configuration
- ✅ **Privacy conscious** - Transparent data practices
- ✅ **Active support** - Help when you need it

## 🚀 Future Features

We're constantly working on new features! Upcoming additions may include:
- Advanced moderation automation
- Custom welcome messages
- Music commands
- Server backups
- And much more!

---

**Made with ❤️ for the Discord community**

## 🛠️ For Developers

### Prerequisites
- Python 3.8 or higher
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))
- Git for version control

### Quick Setup
1. **Clone the repository**
```bash
git clone https://github.com/saawezali/Cereal.git
cd Cereal
```

2. **Set up virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your actual API keys and bot token
```

5. **Run the bot**
```bash
python bot.py
```

### Project Structure
```
Cereal/
├── bot.py                 # Main bot application
├── core/                  # Core functionality
│   ├── config.py         # Configuration management
│   ├── constants.py      # Bot constants
│   └── logger.py         # Logging setup
├── cogs/                 # Command modules
│   ├── moderation.py     # Moderation commands
│   ├── games.py          # Game commands
│   ├── fun.py            # Fun commands
│   └── utility.py        # Utility commands
├── db/                   # Database layer
│   ├── models.py         # SQLAlchemy models
│   └── repository.py     # Data access layer
├── tests/                # Unit tests
├── scripts/              # Utility scripts
└── docs/                 # Documentation
```

### 🤝 Contributing
We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed information on:
- Development setup
- Code standards
- Testing guidelines
- Pull request process

### 📋 Development Features
- **Slash Commands**: Modern Discord command system
- **Database Integration**: SQLite with SQLAlchemy ORM
- **Health Monitoring**: Built-in health check endpoints
- **Docker Support**: Containerized deployment
- **CI/CD Pipeline**: Automated testing and deployment
- **Comprehensive Testing**: Unit and integration tests

---

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
