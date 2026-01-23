# 🥣 Cereal Bot - Developer Documentation

Welcome to the Cereal Bot development team! This document contains everything you need to know to contribute effectively.

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Development Setup](#development-setup)
4. [Code Architecture](#code-architecture)
5. [Adding New Features](#adding-new-features)
6. [Coding Standards](#coding-standards)
7. [Testing Guidelines](#testing-guidelines)
8. [Git Workflow](#git-workflow)
9. [API Reference](#api-reference)
10. [Deployment](#deployment)
11. [Troubleshooting](#troubleshooting)

---

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.8 or higher
- **Git**: For version control
- **Discord Account**: For testing
- **Code Editor**: VS Code recommended with Python extension

### Initial Setup

1. **Clone the repository**
```bash
git clone https://github.com/saawezali/Cereal.git
cd Cereal
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file with your credentials:
```env
DISCORD_TOKEN=your_test_bot_token_here
```

5. **Create a test Discord server**
- Create a new Discord server for development
- Invite your test bot with administrator permissions
- Keep this separate from production

6. **Run the bot**
```bash
python bot.py
```

---

## 📁 Project Structure

```
Cereal/
│
├── bot.py                      # Main entry point - bot initialization
├── core/                       # Core functionality
│   ├── __init__.py            # Core module exports
│   ├── config.py              # Configuration management
│   ├── constants.py           # Bot constants and settings
│   └── logger.py              # Structured logging
├── db/                         # Database module
│   ├── __init__.py            # Database exports
│   ├── base.py                # Database connection & operations
│   ├── models.py              # SQLAlchemy models
│   ├── repository.py          # Repository pattern implementation
│   └── migration/             # Database migration scripts
│       ├── __init__.py
│       ├── base.py            # Migration utilities
│       └── example_migration.py
├── cogs/                       # Feature modules (cogs)
│   ├── moderation.py          # Moderation commands
│   ├── games.py               # Game commands
│   ├── fun.py                 # Fun & memes
│   └── utility.py             # Utility commands
│
├── .env                       # Environment variables (not in repo)
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── CONTRIBUTING.md           # Developer documentation
```
│   ├── __init__.py
│   ├── test_moderation.py
│   ├── test_games.py
│   └── test_utility.py
│
├── data/                       # Data storage (to be created)
│   └── database.db            # SQLite database
│
├── logs/                       # Log files (to be created)
│   └── bot.log
│
├── .env                        # Environment variables (not in git)
├── .env.example                # Example environment file
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── README.md                   # User documentation
├── CONTRIBUTING.md             # This file
└── LICENSE                     # MIT License
```

---

## 🏗️ Code Architecture

### Bot Structure

The bot follows a **Cog-based architecture** for modularity:

```python
# bot.py - Main bot class
class CerealBot(commands.Bot):
    def __init__(self):
        # Initialize bot with intents
        
    async def setup_hook(self):
        # Load all cogs automatically
        
    async def on_ready(self):
        # Bot startup tasks
```

### Cog Structure

Each cog is a self-contained feature module:

```python
# cogs/example.py
class ExampleCog(commands.Cog):
    """Description of what this cog does"""
    
    def __init__(self, bot):
        self.bot = bot
        # Initialize cog-specific variables
    
    @commands.command(name='example')
    async def example_command(self, ctx):
        """Command description"""
        # Command logic
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Event listener"""
        # Event handling

async def setup(bot):
    await bot.add_cog(ExampleCog(bot))
```

### Key Components

1. **Commands**: User-invoked functions (e.g., `!kick`, `!play`)
2. **Events**: Bot reactions to Discord events (e.g., `on_message`, `on_member_join`)
3. **Tasks**: Background loops (e.g., checking reminders)
4. **Checks**: Permission validators (e.g., `@commands.has_permissions()`)
5. **Error Handlers**: Graceful error management

---

## ➕ Adding New Features

### Creating a New Command

1. **Choose the appropriate cog** or create a new one
2. **Add the command function**:

```python
@commands.command(name='hello', aliases=['hi', 'hey'])
@commands.cooldown(1, 5, commands.BucketType.user)  # 1 use per 5 seconds
async def hello(self, ctx, name: str = None):
    """Say hello to someone
    
    Parameters:
    -----------
    name : str, optional
        Name of person to greet
    """
    target = name or ctx.author.display_name
    
    embed = discord.Embed(
        title="👋 Hello!",
        description=f"Hello, {target}!",
        color=discord.Color.blue()
    )
    
    await ctx.send(embed=embed)
```

3. **Add error handling**:

```python
@hello.error
async def hello_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏰ Slow down! Try again in {error.retry_after:.1f}s")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing required argument!")
    else:
        await ctx.send(f"❌ Error: {error}")
```

### Creating a New Cog

1. **Create file in `cogs/` directory**:

```python
# cogs/economy.py
import discord
from discord.ext import commands

class Economy(commands.Cog):
    """Economy system with virtual currency"""
    
    def __init__(self, bot):
        self.bot = bot
        self.currency_name = "Cereal Coins"
    
    @commands.command(name='balance', aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        """Check your balance"""
        member = member or ctx.author
        # TODO: Fetch from database
        balance = 1000
        
        embed = discord.Embed(
            title=f"💰 {member.display_name}'s Balance",
            description=f"**{balance:,}** {self.currency_name}",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='daily')
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        """Claim your daily reward"""
        reward = 100
        # TODO: Add to database
        
        await ctx.send(f"✅ You claimed **{reward}** {self.currency_name}!")

async def setup(bot):
    await bot.add_cog(Economy(bot))
```

2. **Bot will auto-load it** (if following naming convention)

### Adding Event Listeners

```python
@commands.Cog.listener()
async def on_member_join(self, member):
    """Welcome new members"""
    channel = member.guild.system_channel
    if channel:
        embed = discord.Embed(
            title="👋 Welcome!",
            description=f"Welcome to {member.guild.name}, {member.mention}!",
            color=discord.Color.green()
        )
        await channel.send(embed=embed)

@commands.Cog.listener()
async def on_message_delete(self, message):
    """Log deleted messages"""
    if message.author.bot:
        return
    
    print(f"Message deleted: {message.content} by {message.author}")
    # TODO: Log to database or channel
```

### Creating Background Tasks

```python
from discord.ext import tasks

class TaskExample(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_task.start()  # Start the task
    
    def cog_unload(self):
        self.check_task.cancel()  # Stop on unload
    
    @tasks.loop(minutes=30)
    async def check_task(self):
        """Run every 30 minutes"""
        print("Task running!")
        # Your task logic here
    
    @check_task.before_loop
    async def before_check_task(self):
        await self.bot.wait_until_ready()
```

---

## 📝 Coding Standards

### Python Style Guide

Follow **PEP 8** with these specifics:

**Naming Conventions:**
```python
# Variables and functions: snake_case
user_count = 10
def calculate_total():
    pass

# Classes: PascalCase
class ModerationCog:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_WARNINGS = 3
DEFAULT_COLOR = discord.Color.blue()

# Private methods: _leading_underscore
def _internal_helper():
    pass
```

**Docstrings:**
```python
def complex_function(param1: str, param2: int = 5) -> bool:
    """Brief description of function
    
    Longer description if needed explaining the function's purpose,
    behavior, and any important notes.
    
    Parameters
    ----------
    param1 : str
        Description of param1
    param2 : int, optional
        Description of param2 (default is 5)
    
    Returns
    -------
    bool
        Description of return value
    
    Raises
    ------
    ValueError
        If param2 is negative
    
    Examples
    --------
    >>> complex_function("test", 10)
    True
    """
    if param2 < 0:
        raise ValueError("param2 must be positive")
    
    return len(param1) > param2
```

### Discord.py Best Practices

**1. Always use embeds for rich content:**
```python
# Good ✅
embed = discord.Embed(
    title="Title",
    description="Description",
    color=discord.Color.blue()
)
embed.add_field(name="Field", value="Value")
await ctx.send(embed=embed)

# Avoid ❌
await ctx.send("**Title**\nDescription\nField: Value")
```

**2. Use proper error handling:**
```python
# Good ✅
@commands.command()
async def safe_command(self, ctx):
    try:
        # Command logic
        result = risky_operation()
        await ctx.send(f"✅ Success: {result}")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")
        print(f"Error in safe_command: {e}")

# Avoid ❌
@commands.command()
async def unsafe_command(self, ctx):
    result = risky_operation()  # Could crash bot
    await ctx.send(result)
```

**3. Use type hints:**
```python
# Good ✅
async def kick_user(self, ctx: commands.Context, member: discord.Member, reason: str = None) -> None:
    await member.kick(reason=reason)

# Avoid ❌
async def kick_user(self, ctx, member, reason=None):
    await member.kick(reason=reason)
```

**4. Implement cooldowns to prevent spam:**
```python
@commands.command()
@commands.cooldown(1, 60, commands.BucketType.user)  # 1 use per 60 seconds per user
async def daily(self, ctx):
    await ctx.send("Here's your daily reward!")
```

**5. Check permissions properly:**
```python
@commands.command()
@commands.has_permissions(manage_messages=True)
@commands.bot_has_permissions(manage_messages=True)
async def clear(self, ctx, amount: int):
    await ctx.channel.purge(limit=amount)
```

### Embed Design Guidelines

```python
# Consistent color scheme
COLORS = {
    'success': discord.Color.green(),
    'error': discord.Color.red(),
    'warning': discord.Color.orange(),
    'info': discord.Color.blue(),
    'neutral': discord.Color.greyple()
}

# Use emojis for visual appeal
embed = discord.Embed(
    title="✅ Success",
    description="Operation completed successfully",
    color=COLORS['success']
)

# Add timestamps when relevant
embed.timestamp = ctx.message.created_at

# Set footers for attribution
embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
```

---

## 🧪 Testing Guidelines

### Manual Testing Checklist

Before submitting a PR, test:

- ✅ Command works with valid inputs
- ✅ Command handles invalid inputs gracefully
- ✅ Permissions are checked correctly
- ✅ Error messages are user-friendly
- ✅ Embeds display properly on mobile and desktop
- ✅ Command doesn't break other features
- ✅ Performance is acceptable (no long delays)

### Writing Unit Tests

Create tests in `tests/` directory:

```python
# tests/test_moderation.py
import pytest
import discord
from discord.ext import commands

# TODO: Implement proper testing framework
# For now, manual testing is required

class TestModeration:
    def test_kick_command(self):
        """Test kick command logic"""
        # Test implementation
        pass
    
    def test_ban_command(self):
        """Test ban command logic"""
        # Test implementation
        pass
```

### Test Bot Setup

Create a separate test bot token for development:
1. Create new application in Discord Developer Portal
2. Name it "Cereal Bot - DEV"
3. Use this token in your `.env` file
4. Never test with production bot

---

## 🔀 Git Workflow

### Branch Strategy

```
main (production)
  ↓
develop (development)
  ↓
feature/your-feature-name
fix/bug-description
hotfix/critical-fix
```

### Creating a Feature

```bash
# 1. Update develop branch
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/economy-system

# 3. Make changes and commit
git add .
git commit -m "feat: add economy system with balance and daily commands"

# 4. Push to remote
git push origin feature/economy-system

# 5. Create Pull Request on GitHub
```

### Commit Message Format

Follow **Conventional Commits**:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(games): add trivia command with multiple categories"
git commit -m "fix(moderation): resolve kick command permission bug"
git commit -m "docs: update README with new commands"
git commit -m "refactor(utility): optimize reminder checking loop"
```

### Pull Request Guidelines

**PR Title Format:**
```
[TYPE] Brief description of changes
```

**PR Description Template:**
```markdown
## Description
Brief description of what this PR does

## Changes Made
- Added X feature
- Fixed Y bug
- Updated Z documentation

## Testing
- [ ] Tested on test server
- [ ] All commands work as expected
- [ ] No errors in console
- [ ] Checked permission handling

## Screenshots (if applicable)
[Add screenshots of new features]

## Related Issues
Fixes #123
Related to #456
```

### Code Review Checklist

Reviewers should check:
- [ ] Code follows style guidelines
- [ ] No sensitive data in commits
- [ ] Functions have docstrings
- [ ] Error handling is implemented
- [ ] Permissions are checked
- [ ] User experience is good
- [ ] No performance issues

---

## 🔌 API Reference

### Discord.py Quick Reference

**Common Objects:**
```python
ctx.author          # User who invoked command
ctx.guild           # Server where command was used
ctx.channel         # Channel where command was used
ctx.message         # The message object
ctx.bot             # The bot instance

member.mention      # Mentionable string
member.id           # User ID
member.roles        # List of roles
member.top_role     # Highest role
member.guild_permissions  # Permissions

guild.members       # List of members
guild.channels      # List of channels
guild.roles         # List of roles
guild.owner         # Server owner
```

**Sending Messages:**
```python
# Simple message
await ctx.send("Hello!")

# With embed
embed = discord.Embed(title="Title", description="Desc")
await ctx.send(embed=embed)

# With reactions
msg = await ctx.send("React to this!")
await msg.add_reaction('👍')

# DM user
await ctx.author.send("Private message")

# Reply to message
await ctx.reply("Reply to you!")

# Delete message
await ctx.message.delete()

# Edit message
msg = await ctx.send("Original")
await msg.edit(content="Edited")
```

**Permissions:**
```python
# Check if user has permission
if ctx.author.guild_permissions.administrator:
    # User is admin

# Check if bot has permission
if ctx.guild.me.guild_permissions.manage_messages:
    # Bot can manage messages

# Permission decorators
@commands.has_permissions(kick_members=True)
@commands.bot_has_permissions(send_messages=True)
```

**Voice:**
```python
# Join voice
channel = ctx.author.voice.channel
await channel.connect()

# Leave voice
await ctx.voice_client.disconnect()

# Check if in voice
if ctx.voice_client:
    # Bot is in voice
```

### External APIs Used

**Reddit Memes:**
```python
import aiohttp

async with aiohttp.ClientSession() as session:
    async with session.get('https://www.reddit.com/r/memes/random.json',
                          headers={'User-agent': 'Cereal Bot'}) as resp:
        data = await resp.json()
        # Process data
```

**Dad Jokes:**
```python
async with session.get('https://icanhazdadjoke.com/',
                      headers={'Accept': 'application/json'}) as resp:
    data = await resp.json()
    joke = data['joke']
```

**Random Facts:**
```python
async with session.get('https://uselessfacts.jsph.pl/random.json?language=en') as resp:
    data = await resp.json()
    fact = data['text']
```

---

## 🚀 Deployment

### Local Development

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run bot
python bot.py

# View logs
tail -f logs/bot.log
```

### Production Deployment Options

#### Option 1: Railway.app (Recommended)

1. **Create account** at railway.app
2. **Create new project** → Deploy from GitHub
3. **Add environment variables** in Railway dashboard
4. **Deploy** - Railway auto-detects Python and runs bot

**Procfile** (create in root):
```
worker: python bot.py
```

**railway.json** (optional):
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python bot.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### Option 2: Render.com

1. **Create account** at render.com
2. **New Background Worker**
3. **Connect GitHub repo**
4. **Add environment variables**
5. **Deploy**

#### Option 3: VPS (DigitalOcean, Linode, etc.)

```bash
# SSH into server
ssh user@your-server-ip

# Install Python and dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Clone repo
git clone https://github.com/saawezali/Cereal.git
cd Cereal

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
nano .env
# Add your tokens

# Run with screen (keeps running after disconnect)
screen -S cereal-bot
python bot.py
# Press Ctrl+A then D to detach

# Or use systemd service (better for production)
```

**systemd service** (`/etc/systemd/system/cereal-bot.service`):
```ini
[Unit]
Description=Cereal Discord Bot
After=network.target

[Service]
Type=simple
User=saawezali
WorkingDirectory=/home/saawezali/Cereal
Environment="PATH=/home/saawezali/Cereal/venv/bin"
ExecStart=/home/saawezali/Cereal/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable cereal-bot
sudo systemctl start cereal-bot

# Check status
sudo systemctl status cereal-bot

# View logs
sudo journalctl -u cereal-bot -f
```

### Environment Variables for Production

```env
# Required
DISCORD_TOKEN=your_production_token

# Optional
ENVIRONMENT=production
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:pass@host:5432/db
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Bot doesn't respond to commands**
```
Possible causes:
- Message Content Intent not enabled
- Bot lacks permissions in channel
- Command has typo or wrong prefix
- Bot is offline/crashed

Solutions:
- Enable intents in Discord Developer Portal
- Check bot role permissions
- Verify command name and prefix
- Check console for errors
```

**2. Import errors**
```bash
# Error: ModuleNotFoundError: No module named 'discord'
# Solution:
pip install -r requirements.txt

# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

**3. Permission errors**
```python
# Error: Missing Permissions
# Solution: Check both user and bot permissions

@commands.has_permissions(manage_messages=True)  # User permission
@commands.bot_has_permissions(manage_messages=True)  # Bot permission
```

**4. Database errors**
```python
# Error: database is locked
# Solution: Use connection pooling or async database library

# Instead of sqlite3, use aiosqlite
import aiosqlite

async with aiosqlite.connect('database.db') as db:
    await db.execute("INSERT INTO ...")
    await db.commit()
```

### Debug Mode

Add debug logging to bot.py:

```python
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG for verbose output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

# Reduce discord.py verbosity if needed
logging.getLogger('discord').setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.WARNING)
```

### Getting Help

1. **Check Discord.py docs**: https://discordpy.readthedocs.io/
2. **Discord.py Discord server**: https://discord.gg/dpy
3. **GitHub Issues**: Create an issue with:
   - Clear description
   - Steps to reproduce
   - Error messages/logs
   - Python version
   - discord.py version

---

## 📚 Useful Resources

### Documentation
- **Discord.py**: https://discordpy.readthedocs.io/
- **Discord API**: https://discord.com/developers/docs
- **Python**: https://docs.python.org/3/

### Libraries
- **aiohttp** (HTTP requests): https://docs.aiohttp.org/
- **asyncpg** (PostgreSQL): https://magicstack.github.io/asyncpg/

### Tools
- **Discord Permissions Calculator**: https://discordapi.com/permissions.html
- **Discord Embed Generator**: https://cog-creators.github.io/discord-embed-sandbox/
- **JSON Formatter**: https://jsonformatter.org/

### Learning
- **Discord.py Guide**: https://guide.pycord.dev/
- **Python Asyncio**: https://realpython.com/async-io-python/
- **Git Tutorial**: https://www.atlassian.com/git/tutorials

---

## 🎯 Roadmap

### High Priority
- [ ] Database integration (PostgreSQL/SQLite)
- [ ] Proper logging system
- [ ] Error tracking (Sentry)
- [ ] Unit tests
- [ ] CI/CD pipeline

### Medium Priority
- [ ] Leveling system
- [ ] Economy system
- [ ] Auto-moderation
- [ ] Custom prefixes per server
- [ ] Giveaway system

### Low Priority
- [ ] Web dashboard
- [ ] Trivia game with categories
- [ ] Mini-games (hangman, etc.)
- [ ] Starboard

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- Discord.py community
- All contributors
- Coffee ☕

---

**Questions?** Open an issue or contact the maintainers!

**Happy coding! 🥣**