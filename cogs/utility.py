import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta
import pytz
import difflib

# Comprehensive timezone mappings
TIMEZONE_MAP = {
    # === ASIA ===
    # East Asia
    'japan': 'Asia/Tokyo', 'tokyo': 'Asia/Tokyo', 'osaka': 'Asia/Tokyo', 'kyoto': 'Asia/Tokyo',
    'china': 'Asia/Shanghai', 'beijing': 'Asia/Shanghai', 'shanghai': 'Asia/Shanghai', 
    'hong kong': 'Asia/Hong_Kong', 'guangzhou': 'Asia/Shanghai', 'shenzhen': 'Asia/Shanghai',
    'south korea': 'Asia/Seoul', 'korea': 'Asia/Seoul', 'seoul': 'Asia/Seoul', 'busan': 'Asia/Seoul',
    'taiwan': 'Asia/Taipei', 'taipei': 'Asia/Taipei',
    'mongolia': 'Asia/Ulaanbaatar', 'ulaanbaatar': 'Asia/Ulaanbaatar',
    
    # Southeast Asia
    'singapore': 'Asia/Singapore',
    'thailand': 'Asia/Bangkok', 'bangkok': 'Asia/Bangkok',
    'vietnam': 'Asia/Ho_Chi_Minh', 'hanoi': 'Asia/Bangkok', 'ho chi minh': 'Asia/Ho_Chi_Minh', 'saigon': 'Asia/Ho_Chi_Minh',
    'philippines': 'Asia/Manila', 'manila': 'Asia/Manila',
    'indonesia': 'Asia/Jakarta', 'jakarta': 'Asia/Jakarta', 'bali': 'Asia/Makassar', 'surabaya': 'Asia/Jakarta',
    'malaysia': 'Asia/Kuala_Lumpur', 'kuala lumpur': 'Asia/Kuala_Lumpur',
    'myanmar': 'Asia/Yangon', 'yangon': 'Asia/Yangon', 'burma': 'Asia/Yangon',
    'cambodia': 'Asia/Phnom_Penh', 'phnom penh': 'Asia/Phnom_Penh',
    'laos': 'Asia/Vientiane', 'vientiane': 'Asia/Vientiane',
    'brunei': 'Asia/Brunei',
    
    # South Asia
    'india': 'Asia/Kolkata', 'delhi': 'Asia/Kolkata', 'mumbai': 'Asia/Kolkata', 'bangalore': 'Asia/Kolkata',
    'chennai': 'Asia/Kolkata', 'hyderabad': 'Asia/Kolkata', 'kolkata': 'Asia/Kolkata', 'pune': 'Asia/Kolkata',
    'pakistan': 'Asia/Karachi', 'karachi': 'Asia/Karachi', 'lahore': 'Asia/Karachi', 'islamabad': 'Asia/Karachi',
    'bangladesh': 'Asia/Dhaka', 'dhaka': 'Asia/Dhaka',
    'nepal': 'Asia/Kathmandu', 'kathmandu': 'Asia/Kathmandu',
    'sri lanka': 'Asia/Colombo', 'colombo': 'Asia/Colombo',
    'bhutan': 'Asia/Thimphu', 'thimphu': 'Asia/Thimphu',
    'maldives': 'Indian/Maldives', 'male': 'Indian/Maldives',
    
    # Central Asia
    'kazakhstan': 'Asia/Almaty', 'almaty': 'Asia/Almaty', 'astana': 'Asia/Almaty',
    'uzbekistan': 'Asia/Tashkent', 'tashkent': 'Asia/Tashkent',
    'turkmenistan': 'Asia/Ashgabat', 'ashgabat': 'Asia/Ashgabat',
    'kyrgyzstan': 'Asia/Bishkek', 'bishkek': 'Asia/Bishkek',
    'tajikistan': 'Asia/Dushanbe', 'dushanbe': 'Asia/Dushanbe',
    'afghanistan': 'Asia/Kabul', 'kabul': 'Asia/Kabul',
    
    # Middle East
    'uae': 'Asia/Dubai', 'dubai': 'Asia/Dubai', 'abu dhabi': 'Asia/Dubai', 'sharjah': 'Asia/Dubai',
    'saudi arabia': 'Asia/Riyadh', 'riyadh': 'Asia/Riyadh', 'jeddah': 'Asia/Riyadh', 'mecca': 'Asia/Riyadh',
    'israel': 'Asia/Jerusalem', 'jerusalem': 'Asia/Jerusalem', 'tel aviv': 'Asia/Jerusalem',
    'iran': 'Asia/Tehran', 'tehran': 'Asia/Tehran',
    'iraq': 'Asia/Baghdad', 'baghdad': 'Asia/Baghdad',
    'turkey': 'Europe/Istanbul', 'istanbul': 'Europe/Istanbul', 'ankara': 'Europe/Istanbul',
    'qatar': 'Asia/Qatar', 'doha': 'Asia/Qatar',
    'kuwait': 'Asia/Kuwait', 'kuwait city': 'Asia/Kuwait',
    'bahrain': 'Asia/Bahrain', 'manama': 'Asia/Bahrain',
    'oman': 'Asia/Muscat', 'muscat': 'Asia/Muscat',
    'jordan': 'Asia/Amman', 'amman': 'Asia/Amman',
    'lebanon': 'Asia/Beirut', 'beirut': 'Asia/Beirut',
    'syria': 'Asia/Damascus', 'damascus': 'Asia/Damascus',
    'yemen': 'Asia/Aden', 'aden': 'Asia/Aden', 'sanaa': 'Asia/Aden',
    
    # === EUROPE ===
    # Western Europe
    'uk': 'Europe/London', 'london': 'Europe/London', 'manchester': 'Europe/London', 'birmingham': 'Europe/London',
    'england': 'Europe/London', 'scotland': 'Europe/London', 'wales': 'Europe/London', 'ireland': 'Europe/Dublin',
    'france': 'Europe/Paris', 'paris': 'Europe/Paris', 'marseille': 'Europe/Paris', 'lyon': 'Europe/Paris',
    'germany': 'Europe/Berlin', 'berlin': 'Europe/Berlin', 'munich': 'Europe/Berlin', 'frankfurt': 'Europe/Berlin',
    'spain': 'Europe/Madrid', 'madrid': 'Europe/Madrid', 'barcelona': 'Europe/Madrid', 'valencia': 'Europe/Madrid',
    'italy': 'Europe/Rome', 'rome': 'Europe/Rome', 'milan': 'Europe/Rome', 'venice': 'Europe/Rome', 'florence': 'Europe/Rome',
    'portugal': 'Europe/Lisbon', 'lisbon': 'Europe/Lisbon', 'porto': 'Europe/Lisbon',
    'netherlands': 'Europe/Amsterdam', 'amsterdam': 'Europe/Amsterdam', 'rotterdam': 'Europe/Amsterdam',
    'belgium': 'Europe/Brussels', 'brussels': 'Europe/Brussels', 'antwerp': 'Europe/Brussels',
    'switzerland': 'Europe/Zurich', 'zurich': 'Europe/Zurich', 'geneva': 'Europe/Zurich', 'bern': 'Europe/Zurich',
    'austria': 'Europe/Vienna', 'vienna': 'Europe/Vienna', 'salzburg': 'Europe/Vienna',
    
    # Northern Europe
    'sweden': 'Europe/Stockholm', 'stockholm': 'Europe/Stockholm',
    'norway': 'Europe/Oslo', 'oslo': 'Europe/Oslo',
    'denmark': 'Europe/Copenhagen', 'copenhagen': 'Europe/Copenhagen',
    'finland': 'Europe/Helsinki', 'helsinki': 'Europe/Helsinki',
    'iceland': 'Atlantic/Reykjavik', 'reykjavik': 'Atlantic/Reykjavik',
    
    # Eastern Europe
    'russia': 'Europe/Moscow', 'moscow': 'Europe/Moscow', 'st petersburg': 'Europe/Moscow',
    'poland': 'Europe/Warsaw', 'warsaw': 'Europe/Warsaw', 'krakow': 'Europe/Warsaw',
    'ukraine': 'Europe/Kiev', 'kiev': 'Europe/Kiev', 'kyiv': 'Europe/Kiev',
    'czech republic': 'Europe/Prague', 'czechia': 'Europe/Prague', 'prague': 'Europe/Prague',
    'romania': 'Europe/Bucharest', 'bucharest': 'Europe/Bucharest',
    'hungary': 'Europe/Budapest', 'budapest': 'Europe/Budapest',
    'greece': 'Europe/Athens', 'athens': 'Europe/Athens',
    'bulgaria': 'Europe/Sofia', 'sofia': 'Europe/Sofia',
    'serbia': 'Europe/Belgrade', 'belgrade': 'Europe/Belgrade',
    'croatia': 'Europe/Zagreb', 'zagreb': 'Europe/Zagreb',
    
    # === AMERICAS ===
    # North America
    'usa': 'America/New_York', 'united states': 'America/New_York',
    'new york': 'America/New_York', 'nyc': 'America/New_York', 'boston': 'America/New_York',
    'los angeles': 'America/Los_Angeles', 'la': 'America/Los_Angeles', 'san francisco': 'America/Los_Angeles',
    'chicago': 'America/Chicago', 'houston': 'America/Chicago', 'dallas': 'America/Chicago',
    'denver': 'America/Denver', 'phoenix': 'America/Phoenix',
    'seattle': 'America/Los_Angeles', 'portland': 'America/Los_Angeles',
    'miami': 'America/New_York', 'atlanta': 'America/New_York', 'washington': 'America/New_York',
    'las vegas': 'America/Los_Angeles', 'san diego': 'America/Los_Angeles',
    
    'canada': 'America/Toronto', 'toronto': 'America/Toronto', 'montreal': 'America/Toronto',
    'vancouver': 'America/Vancouver', 'calgary': 'America/Edmonton', 'ottawa': 'America/Toronto',
    
    'mexico': 'America/Mexico_City', 'mexico city': 'America/Mexico_City', 'guadalajara': 'America/Mexico_City',
    
    # Central America
    'guatemala': 'America/Guatemala',
    'belize': 'America/Belize',
    'honduras': 'America/Tegucigalpa',
    'el salvador': 'America/El_Salvador',
    'nicaragua': 'America/Managua',
    'costa rica': 'America/Costa_Rica',
    'panama': 'America/Panama',
    
    # Caribbean
    'jamaica': 'America/Jamaica', 'kingston': 'America/Jamaica',
    'cuba': 'America/Havana', 'havana': 'America/Havana',
    'dominican republic': 'America/Santo_Domingo',
    'puerto rico': 'America/Puerto_Rico',
    'bahamas': 'America/Nassau',
    'trinidad': 'America/Port_of_Spain',
    
    # South America
    'brazil': 'America/Sao_Paulo', 'sao paulo': 'America/Sao_Paulo', 'rio': 'America/Sao_Paulo',
    'rio de janeiro': 'America/Sao_Paulo', 'brasilia': 'America/Sao_Paulo',
    'argentina': 'America/Argentina/Buenos_Aires', 'buenos aires': 'America/Argentina/Buenos_Aires',
    'chile': 'America/Santiago', 'santiago': 'America/Santiago',
    'colombia': 'America/Bogota', 'bogota': 'America/Bogota',
    'peru': 'America/Lima', 'lima': 'America/Lima',
    'venezuela': 'America/Caracas', 'caracas': 'America/Caracas',
    'ecuador': 'America/Guayaquil', 'quito': 'America/Guayaquil',
    'bolivia': 'America/La_Paz', 'la paz': 'America/La_Paz',
    'paraguay': 'America/Asuncion', 'asuncion': 'America/Asuncion',
    'uruguay': 'America/Montevideo', 'montevideo': 'America/Montevideo',
    
    # === AFRICA ===
    'egypt': 'Africa/Cairo', 'cairo': 'Africa/Cairo', 'alexandria': 'Africa/Cairo',
    'south africa': 'Africa/Johannesburg', 'johannesburg': 'Africa/Johannesburg', 'cape town': 'Africa/Johannesburg',
    'nigeria': 'Africa/Lagos', 'lagos': 'Africa/Lagos', 'abuja': 'Africa/Lagos',
    'kenya': 'Africa/Nairobi', 'nairobi': 'Africa/Nairobi',
    'ethiopia': 'Africa/Addis_Ababa', 'addis ababa': 'Africa/Addis_Ababa',
    'morocco': 'Africa/Casablanca', 'casablanca': 'Africa/Casablanca', 'marrakech': 'Africa/Casablanca',
    'algeria': 'Africa/Algiers', 'algiers': 'Africa/Algiers',
    'tunisia': 'Africa/Tunis', 'tunis': 'Africa/Tunis',
    'ghana': 'Africa/Accra', 'accra': 'Africa/Accra',
    'tanzania': 'Africa/Dar_es_Salaam', 'dar es salaam': 'Africa/Dar_es_Salaam',
    'uganda': 'Africa/Kampala', 'kampala': 'Africa/Kampala',
    'zimbabwe': 'Africa/Harare', 'harare': 'Africa/Harare',
    
    # === OCEANIA ===
    'australia': 'Australia/Sydney', 'sydney': 'Australia/Sydney', 'melbourne': 'Australia/Sydney',
    'brisbane': 'Australia/Brisbane', 'perth': 'Australia/Perth', 'adelaide': 'Australia/Adelaide',
    'new zealand': 'Pacific/Auckland', 'auckland': 'Pacific/Auckland', 'wellington': 'Pacific/Auckland',
    'fiji': 'Pacific/Fiji',
    'papua new guinea': 'Pacific/Port_Moresby',
    
    # === TIMEZONE ABBREVIATIONS ===
    'utc': 'UTC', 'gmt': 'GMT',
    'est': 'America/New_York', 'edt': 'America/New_York',
    'cst': 'America/Chicago', 'cdt': 'America/Chicago',
    'mst': 'America/Denver', 'mdt': 'America/Denver',
    'pst': 'America/Los_Angeles', 'pdt': 'America/Los_Angeles',
    'akst': 'America/Anchorage', 'hst': 'Pacific/Honolulu',
    'bst': 'Europe/London', 'cet': 'Europe/Paris', 'eet': 'Europe/Athens',
    'jst': 'Asia/Tokyo', 'kst': 'Asia/Seoul', 'ist': 'Asia/Kolkata',
    'aest': 'Australia/Sydney', 'acst': 'Australia/Adelaide', 'awst': 'Australia/Perth',
    
    # === FULL TIMEZONE NAMES ===
    'coordinated universal time': 'UTC', 'greenwich mean time': 'GMT',
    'eastern standard time': 'America/New_York', 'eastern daylight time': 'America/New_York',
    'central standard time': 'America/Chicago', 'central daylight time': 'America/Chicago',
    'mountain standard time': 'America/Denver', 'mountain daylight time': 'America/Denver',
    'pacific standard time': 'America/Los_Angeles', 'pacific daylight time': 'America/Los_Angeles',
    'alaska standard time': 'America/Anchorage', 'hawaii standard time': 'Pacific/Honolulu',
    'british summer time': 'Europe/London', 'central european time': 'Europe/Paris', 'eastern european time': 'Europe/Athens',
    'japan standard time': 'Asia/Tokyo', 'korea standard time': 'Asia/Seoul', 'indian standard time': 'Asia/Kolkata',
    'australian eastern standard time': 'Australia/Sydney', 'australian central standard time': 'Australia/Adelaide', 'australian western standard time': 'Australia/Perth',
}

# Display names for autocomplete (shows abbreviation + full name)
DISPLAY_MAP = {
    # Abbreviations
    'utc': 'UTC(Coordinated Universal Time)', 'gmt': 'GMT(Greenwich Mean Time)',
    'est': 'EST(Eastern Standard Time)', 'edt': 'EDT(Eastern Daylight Time)',
    'cst': 'CST(Central Standard Time)', 'cdt': 'CDT(Central Daylight Time)',
    'mst': 'MST(Mountain Standard Time)', 'mdt': 'MDT(Mountain Daylight Time)',
    'pst': 'PST(Pacific Standard Time)', 'pdt': 'PDT(Pacific Daylight Time)',
    'akst': 'AKST(Alaska Standard Time)', 'hst': 'HST(Hawaii Standard Time)',
    'bst': 'BST(British Summer Time)', 'cet': 'CET(Central European Time)', 'eet': 'EET(Eastern European Time)',
    'jst': 'JST(Japan Standard Time)', 'kst': 'KST(Korea Standard Time)', 'ist': 'IST(Indian Standard Time)',
    'aest': 'AEST(Australian Eastern Standard Time)', 'acst': 'ACST(Australian Central Standard Time)', 'awst': 'AWST(Australian Western Standard Time)',
    
    # Full names
    'coordinated universal time': 'UTC(Coordinated Universal Time)', 'greenwich mean time': 'GMT(Greenwich Mean Time)',
    'eastern standard time': 'EST(Eastern Standard Time)', 'eastern daylight time': 'EDT(Eastern Daylight Time)',
    'central standard time': 'CST(Central Standard Time)', 'central daylight time': 'CDT(Central Daylight Time)',
    'mountain standard time': 'MST(Mountain Standard Time)', 'mountain daylight time': 'MDT(Mountain Daylight Time)',
    'pacific standard time': 'PST(Pacific Standard Time)', 'pacific daylight time': 'PDT(Pacific Daylight Time)',
    'alaska standard time': 'AKST(Alaska Standard Time)', 'hawaii standard time': 'HST(Hawaii Standard Time)',
    'british summer time': 'BST(British Summer Time)', 'central european time': 'CET(Central European Time)', 'eastern european time': 'EET(Eastern European Time)',
    'japan standard time': 'JST(Japan Standard Time)', 'korea standard time': 'KST(Korea Standard Time)', 'indian standard time': 'IST(Indian Standard Time)',
    'australian eastern standard time': 'AEST(Australian Eastern Standard Time)', 'australian central standard time': 'ACST(Australian Central Standard Time)', 'australian western standard time': 'AWST(Australian Western Standard Time)',
}

class Utility(commands.Cog):
    """Utility commands including reminders"""
    
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []  # Will store: (user_id, channel_id, time, message)
        self.afk_users = {}  # Store AFK users: {user_id: reason}
        self.check_reminders.start()
    
    def cog_unload(self):
        self.check_reminders.cancel()
    
    @tasks.loop(seconds=30)
    async def check_reminders(self):
        """Check for reminders that need to be sent"""
        current_time = datetime.now()
        reminders_to_remove = []
        
        for reminder in self.reminders:
            user_id, channel_id, remind_time, message = reminder
            
            if current_time >= remind_time:
                try:
                    channel = self.bot.get_channel(channel_id)
                    user = self.bot.get_user(user_id)
                    
                    if channel and user:
                        embed = discord.Embed(
                            title="⏰ Reminder!",
                            description=message,
                            color=discord.Color.blue(),
                            timestamp=datetime.now()
                        )
                        embed.set_footer(text=f"Reminder for {user.name}")
                        
                        await channel.send(f"{user.mention}", embed=embed)
                    
                    reminders_to_remove.append(reminder)
                except Exception as e:
                    print(f"Error sending reminder: {e}")
                    reminders_to_remove.append(reminder)
        
        # Remove sent reminders
        for reminder in reminders_to_remove:
            self.reminders.remove(reminder)
    
    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()
    
    @app_commands.command(name='remind', description='Set a reminder')
    @app_commands.describe(
        time='Time format: 10s, 5m, 2h, 1d',
        message='What to remind you about'
    )
    async def remind(self, interaction: discord.Interaction, time: str, message: str):
        """
        Set a reminder
        Format: /remind time:10s message:Check the oven
        Time format: 10s, 5m, 2h, 1d (seconds, minutes, hours, days)
        """
        # Parse time
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        
        if time[-1] not in time_units:
            return await interaction.response.send_message("❌ Invalid time format! Use: 10s, 5m, 2h, or 1d", ephemeral=True)
        
        try:
            amount = int(time[:-1])
            unit = time[-1]
            seconds = amount * time_units[unit]
            
            if seconds < 10:
                return await interaction.response.send_message("❌ Reminder must be at least 10 seconds!", ephemeral=True)
            if seconds > 2592000:  # 30 days
                return await interaction.response.send_message("❌ Reminder cannot be longer than 30 days!", ephemeral=True)
            
            remind_time = datetime.now() + timedelta(seconds=seconds)
            
            # Add reminder to list
            self.reminders.append((interaction.user.id, interaction.channel.id, remind_time, message))
            
            embed = discord.Embed(
                title="✅ Reminder Set!",
                description=f"I'll remind you about: **{message}**",
                color=discord.Color.green()
            )
            embed.add_field(
                name="When",
                value=discord.utils.format_dt(remind_time, style='R')
            )
            
            await interaction.response.send_message(embed=embed)
            
        except ValueError:
            await interaction.response.send_message("❌ Invalid time format! Use: 10s, 5m, 2h, or 1d", ephemeral=True)
    
    @app_commands.command(name='reminders', description='List your active reminders')
    async def list_reminders(self, interaction: discord.Interaction):
        """List your active reminders"""
        user_reminders = [r for r in self.reminders if r[0] == interaction.user.id]
        
        if not user_reminders:
            return await interaction.response.send_message("You have no active reminders!", ephemeral=True)
        
        embed = discord.Embed(
            title=f"⏰ Your Reminders ({len(user_reminders)})",
            color=discord.Color.blue()
        )
        
        for i, (_, _, remind_time, message) in enumerate(user_reminders[:10], 1):
            time_str = discord.utils.format_dt(remind_time, style='R')
            embed.add_field(
                name=f"{i}. {time_str}",
                value=message[:100],
                inline=False
            )
        
        if len(user_reminders) > 10:
            embed.set_footer(text=f"Showing 10 of {len(user_reminders)} reminders")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='poll', description='Create a poll')
    @app_commands.describe(
        question='The poll question',
        options='Poll options separated by commas (e.g., Option1, Option2, Option3)'
    )
    async def poll(self, interaction: discord.Interaction, question: str, options: str):
        """Create a poll"""
        # Split options by comma
        options_list = [opt.strip() for opt in options.split(',')]
        
        if len(options_list) < 2:
            return await interaction.response.send_message("❌ You need at least 2 options!", ephemeral=True)
        if len(options_list) > 10:
            return await interaction.response.send_message("❌ Maximum 10 options allowed!", ephemeral=True)
        
        # Emoji numbers
        emoji_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        embed = discord.Embed(
            title="📊 " + question,
            description="\n".join([f"{emoji_numbers[i]} {option}" for i, option in enumerate(options_list)]),
            color=discord.Color.blue(),
            timestamp=interaction.created_at
        )
        embed.set_footer(text=f"Poll by {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed)
        msg = await interaction.original_response()
        
        # Add reactions
        for i in range(len(options_list)):
            await msg.add_reaction(emoji_numbers[i])
    
    @app_commands.command(name='afk', description='Set your AFK status')
    @app_commands.describe(reason='Reason for being AFK')
    async def afk(self, interaction: discord.Interaction, reason: str = "AFK"):
        """Set your AFK status"""
        self.afk_users[interaction.user.id] = reason
        
        embed = discord.Embed(
            title="💤 AFK",
            description=f"{interaction.user.mention} is now AFK: {reason}",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Check for AFK users"""
        if message.author.bot:
            return
        
        # Check if user returned from AFK
        if message.author.id in self.afk_users:
            reason = self.afk_users.pop(message.author.id)
            await message.channel.send(
                f"Welcome back {message.author.mention}! You were AFK: {reason}",
                delete_after=5
            )
        
        # Check if AFK user was mentioned
        for user_id in self.afk_users:
            user = self.bot.get_user(user_id)
            if user and user.mentioned_in(message):
                reason = self.afk_users[user_id]
                await message.channel.send(
                    f"💤 {user.display_name} is currently AFK: {reason}",
                    delete_after=10
                )
    
    @app_commands.command(name='ping', description='Check bot latency')
    async def ping(self, interaction: discord.Interaction):
        """Check bot latency"""
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: **{latency}ms**",
            color=discord.Color.green() if latency < 200 else discord.Color.red()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='suggest', description='Submit a suggestion')
    @app_commands.describe(suggestion='Your suggestion')
    async def suggest(self, interaction: discord.Interaction, suggestion: str):
        """Submit a suggestion"""
        embed = discord.Embed(
            title="💡 New Suggestion",
            description=suggestion,
            color=discord.Color.blue(),
            timestamp=interaction.created_at
        )
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"User ID: {interaction.user.id}")
        
        await interaction.response.send_message(embed=embed)
        msg = await interaction.original_response()
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
    
    @app_commands.command(name='timer', description='Start a countdown timer')
    @app_commands.describe(time='Time format: 10s, 5m, 2h')
    async def timer(self, interaction: discord.Interaction, time: str):
        """
        Start a countdown timer
        Format: /timer time:30s
        Time format: 10s, 5m, 2h (seconds, minutes, hours)
        """
        # Parse time
        time_units = {'s': 1, 'm': 60, 'h': 3600}
        
        if not time or time[-1] not in time_units:
            return await interaction.response.send_message("❌ Invalid time format! Use: 10s, 5m, or 2h\nExample: `/timer time:30s`", ephemeral=True)
        
        try:
            amount = int(time[:-1])
            unit = time[-1]
            seconds = amount * time_units[unit]
            
            if seconds < 1:
                return await interaction.response.send_message("❌ Timer must be at least 1 second!", ephemeral=True)
            if seconds > 86400:  # 24 hours
                return await interaction.response.send_message("❌ Timer cannot exceed 24 hours!", ephemeral=True)
            
            # Format display time
            if seconds < 60:
                display_time = f"{seconds} second{'s' if seconds != 1 else ''}"
            elif seconds < 3600:
                display_time = f"{seconds // 60} minute{'s' if seconds // 60 != 1 else ''}"
            else:
                display_time = f"{seconds // 3600} hour{'s' if seconds // 3600 != 1 else ''}"
            
            embed = discord.Embed(
                title="⏱️ Timer Started",
                description=f"Timer set for **{display_time}**",
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Started by {interaction.user.name}")
            
            await interaction.response.send_message(embed=embed)
            msg = await interaction.original_response()
            
            await asyncio.sleep(seconds)
            
            embed = discord.Embed(
                title="⏰ Timer Complete!",
                description=f"Your **{display_time}** timer is up!",
                color=discord.Color.green()
            )
            
            await msg.edit(embed=embed)
            await interaction.followup.send(f"{interaction.user.mention} ⏰ Time's up!")
            
        except ValueError:
            await interaction.response.send_message("❌ Invalid time format! Use: 10s, 5m, or 2h\nExample: `/timer time:30s`", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {e}")
    
    @app_commands.command(name='calculate', description='Calculate a mathematical expression')
    @app_commands.describe(expression='The mathematical expression to calculate')
    async def calculate(self, interaction: discord.Interaction, expression: str):
        """Calculate a mathematical expression"""
        try:
            # Remove any potentially dangerous characters
            allowed_chars = '0123456789+-*/()%. '
            if not all(c in allowed_chars for c in expression):
                return await interaction.response.send_message("❌ Invalid characters in expression!", ephemeral=True)
            
            result = eval(expression)
            
            embed = discord.Embed(
                title="🧮 Calculator",
                color=discord.Color.blue()
            )
            embed.add_field(name="Expression", value=f"```{expression}```", inline=False)
            embed.add_field(name="Result", value=f"```{result}```", inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error calculating: {e}", ephemeral=True)
    
    @app_commands.command(name='say', description='Make the bot say something')
    @app_commands.describe(message='The message for the bot to say')
    @commands.has_permissions(manage_messages=True)
    async def say(self, interaction: discord.Interaction, message: str):
        """Make the bot say something"""
        await interaction.response.send_message("✅ Message sent!", ephemeral=True)
        await interaction.channel.send(message)
    
    @app_commands.command(name='embed', description='Create a custom embed')
    @app_commands.describe(title='Embed title', description='Embed description')
    @commands.has_permissions(manage_messages=True)
    async def create_embed(self, interaction: discord.Interaction, title: str, description: str):
        """Create a custom embed"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blue(),
            timestamp=interaction.created_at
        )
        embed.set_footer(text=f"Created by {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed)
    
    async def timezone_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        """Autocomplete for timezone locations"""
        if not current:
            # Return first 25 locations when no input
            keys = list(TIMEZONE_MAP.keys())[:25]
            return [app_commands.Choice(name=DISPLAY_MAP.get(key, key.title()), value=key) for key in keys]
        else:
            # Find close matches
            matches = difflib.get_close_matches(current.lower(), TIMEZONE_MAP.keys(), n=25, cutoff=0.3)
            return [app_commands.Choice(name=DISPLAY_MAP.get(match, match.title()), value=match) for match in matches]
    
    @app_commands.command(name='timezone', description='Check the current time in any timezone')
    @app_commands.describe(location='City, country, or timezone (e.g., Tokyo, EST, UTC)')
    @app_commands.autocomplete(location=timezone_autocomplete)
    async def timezone(self, interaction: discord.Interaction, location: str):
        """Check the current time in any timezone"""
        
        # Normalize input
        location_lower = location.lower().strip()
        
        # Try to find timezone
        timezone_str = None
        
        # Check if it's in our map
        if location_lower in TIMEZONE_MAP:
            timezone_str = TIMEZONE_MAP[location_lower]
        else:
            # Try to find it directly in pytz
            for tz in pytz.all_timezones:
                if location_lower in tz.lower():
                    timezone_str = tz
                    break
        
        if not timezone_str:
            # Suggest similar timezones
            suggestions = []
            for key in TIMEZONE_MAP.keys():
                if location_lower in key or key in location_lower:
                    suggestions.append(key.title())
            
            error_msg = f"❌ Timezone '{location}' not found!"
            if suggestions:
                error_msg += f"\n\nDid you mean: {', '.join(suggestions[:5])}?"
            else:
                error_msg += "\n\nTry: New York, London, Tokyo, EST, GMT, UTC, etc."
            
            return await interaction.response.send_message(error_msg, ephemeral=True)
        
        try:
            # Get timezone object
            tz = pytz.timezone(timezone_str)
            
            # Get current time in that timezone
            current_time = datetime.now(tz)
            
            # Format time
            time_12h = current_time.strftime("%I:%M:%S %p")
            time_24h = current_time.strftime("%H:%M:%S")
            date_str = current_time.strftime("%A, %B %d, %Y")
            
            # Get UTC offset
            utc_offset = current_time.strftime("%z")
            utc_offset_formatted = f"UTC{utc_offset[:3]}:{utc_offset[3:]}"
            
            # Create embed
            embed = discord.Embed(
                title=f"🌍 Time in {location.title()}",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name="📅 Date", value=date_str, inline=False)
            embed.add_field(name="🕐 12-Hour", value=time_12h, inline=True)
            embed.add_field(name="🕐 24-Hour", value=time_24h, inline=True)
            embed.add_field(name="🌐 Timezone", value=f"{timezone_str}\n({utc_offset_formatted})", inline=False)
            
            embed.set_footer(text=f"Requested by {interaction.user.name}")
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error getting timezone: {e}", ephemeral=True)

    @app_commands.command(name='help', description='Show available commands')
    async def help_command(self, interaction: discord.Interaction):
        """Show help information"""
        embed = discord.Embed(
            title="🥣 Cereal Bot Commands",
            description="Here are all available slash commands:",
            color=discord.Color.blue()
        )
        
        # Get all slash commands
        commands = []
        for cog_name, cog in self.bot.cogs.items():
            cog_commands = []
            for command in cog.get_app_commands():
                cog_commands.append(f"`/{command.name}` - {command.description or 'No description'}")
            if cog_commands:
                commands.append(f"**{cog_name}**\n" + "\n".join(cog_commands))
        
        embed.description += "\n\n" + "\n\n".join(commands)
        
        embed.set_footer(text="Use /command to run commands")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))