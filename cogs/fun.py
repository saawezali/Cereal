import discord
from discord import app_commands
from discord.ext import commands
import random
import aiohttp

class Fun(commands.Cog):
    """Fun commands and memes"""
    
    def __init__(self, bot):
        self.bot = bot
        self.session = None
    
    async def cog_load(self):
        """Create aiohttp session when cog loads"""
        self.session = aiohttp.ClientSession()
    
    async def cog_unload(self):
        """Close aiohttp session when cog unloads"""
        if self.session:
            await self.session.close()
    
    @commands.hybrid_command(name='meme', description='Get a random meme from Reddit')
    async def meme(self, ctx: commands.Context):
        """Get a random meme from Reddit"""
        subreddits = ['memes', 'dankmemes', 'me_irl', 'wholesomememes', 'funny']
        
        # Try multiple times to get a valid image meme
        for attempt in range(5):
            subreddit = random.choice(subreddits)
            
            try:
                async with self.session.get(
                    f'https://www.reddit.com/r/{subreddit}/hot.json?limit=100',
                    headers={'User-agent': 'Cereal Bot 1.0'}
                ) as resp:
                    if resp.status != 200:
                        continue
                    
                    data = await resp.json()
                    posts = data['data']['children']
                    
                    # Filter for image posts only
                    image_posts = [
                        post['data'] for post in posts 
                        if post['data'].get('post_hint') == 'image' 
                        and not post['data'].get('over_18', False)
                    ]
                    
                    if not image_posts:
                        continue
                    
                    post = random.choice(image_posts)
                    
                    embed = discord.Embed(
                        title=post['title'][:256],  # Discord limit
                        color=discord.Color.random(),
                        url=f"https://reddit.com{post['permalink']}"
                    )
                    embed.set_image(url=post['url'])
                    embed.set_footer(text=f"👍 {post['ups']} | r/{subreddit}")
                    
                    return await ctx.send(embed=embed)
                    
            except Exception as e:
                print(f"Meme error attempt {attempt + 1}: {e}")
                continue
        
        await ctx.send("❌ Couldn't fetch a meme right now. Try again!")
    
    @commands.hybrid_command(name='dadjoke', description='Get a random dad joke')
    async def dad_joke(self, ctx: commands.Context):
        """Get a random dad joke"""
        async with self.session.get('https://icanhazdadjoke.com/',
                                   headers={'Accept': 'application/json'}) as resp:
            if resp.status == 200:
                data = await resp.json()
                embed = discord.Embed(
                    title="😄 Dad Joke",
                    description=data['joke'],
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Couldn't fetch a joke right now!")
    
    @commands.hybrid_command(name='fact', description='Get a random fact')
    async def random_fact(self, ctx: commands.Context):
        """Get a random fact"""
        async with self.session.get('https://uselessfacts.jsph.pl/random.json?language=en') as resp:
            if resp.status == 200:
                data = await resp.json()
                embed = discord.Embed(
                    title="🧠 Random Fact",
                    description=data['text'],
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Couldn't fetch a fact right now!")
    
    @commands.hybrid_command(name='roast', description='Roast someone (or yourself)')
    @app_commands.describe(member='The member to roast (optional)')
    async def roast(self, ctx: commands.Context, member: discord.Member = None):
        """Roast someone (or yourself)"""
        target = member or ctx.author
        
        roasts = [
            f"{target.mention}, I'd explain it to you but I left my crayons at home.",
            f"{target.mention}, you're like a cloud. When you disappear, it's a beautiful day.",
            f"{target.mention}, if brains were dynamite, you wouldn't have enough to blow your nose.",
            f"{target.mention}, you bring everyone so much joy... when you leave the room.",
            f"{target.mention}, I'd agree with you but then we'd both be wrong.",
            f"{target.mention}, you're proof that evolution can go in reverse.",
            f"{target.mention}, somewhere out there is a tree tirelessly producing oxygen for you. Go apologize to it.",
        ]
        
        embed = discord.Embed(
            title="🔥 Roasted!",
            description=random.choice(roasts),
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='compliment', description='Give someone a compliment')
    @app_commands.describe(member='The member to compliment (optional)')
    async def compliment(self, ctx: commands.Context, member: discord.Member = None):
        """Give someone a compliment"""
        target = member or ctx.author
        
        compliments = [
            f"{target.mention}, you're more helpful than you realize!",
            f"{target.mention}, you have the best laugh!",
            f"{target.mention}, you're a great listener!",
            f"{target.mention}, you light up the room!",
            f"{target.mention}, you're awesome and you know it!",
            f"{target.mention}, you're even better than a unicorn, because you're real!",
            f"{target.mention}, you're a gift to those around you!",
        ]
        
        embed = discord.Embed(
            title="💝 Compliment",
            description=random.choice(compliments),
            color=discord.Color.pink()
        )
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='ship', description='Ship two members together')
    @app_commands.describe(member1='First member', member2='Second member (optional)')
    async def ship(self, ctx: commands.Context, member1: discord.Member, member2: discord.Member = None):
        """Ship two members together"""
        if not member2:
            member2 = ctx.author
        
        # Calculate ship percentage based on user IDs for consistency
        ship_percentage = (member1.id + member2.id) % 101
        
        # Create ship name
        name1 = member1.display_name[:len(member1.display_name)//2]
        name2 = member2.display_name[len(member2.display_name)//2:]
        ship_name = name1 + name2
        
        # Determine relationship status
        if ship_percentage < 25:
            status = "💔 Not meant to be..."
            color = discord.Color.dark_gray()
        elif ship_percentage < 50:
            status = "😐 Could work with effort"
            color = discord.Color.orange()
        elif ship_percentage < 75:
            status = "💕 Good match!"
            color = discord.Color.blue()
        else:
            status = "💖 Perfect match!"
            color = discord.Color.red()
        
        embed = discord.Embed(
            title=f"💘 {ship_name}",
            description=f"{member1.mention} + {member2.mention}",
            color=color
        )
        embed.add_field(name="Love Percentage", value=f"{ship_percentage}%")
        embed.add_field(name="Status", value=status)
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='avatar', aliases=['av', 'pfp'], description="Get someone's avatar")
    @app_commands.describe(member='The member whose avatar to get (optional)')
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        """Get someone's avatar"""
        member = member or ctx.author
        
        embed = discord.Embed(
            title=f"{member.display_name}'s Avatar",
            color=member.color
        )
        embed.set_image(url=member.display_avatar.url)
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='userinfo', aliases=['ui', 'whois'], description='Get information about a user')
    @app_commands.describe(member='The member to get info about (optional)')
    async def user_info(self, ctx: commands.Context, member: discord.Member = None):
        """Get information about a user"""
        member = member or ctx.author
        
        roles = [role.mention for role in member.roles[1:]]  # Exclude @everyone
        
        embed = discord.Embed(
            title=f"User Info - {member}",
            color=member.color,
            timestamp=ctx.message.created_at
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
        embed.add_field(name="Status", value=str(member.status).title(), inline=True)
        
        embed.add_field(
            name="Account Created",
            value=discord.utils.format_dt(member.created_at, style='R'),
            inline=True
        )
        embed.add_field(
            name="Joined Server",
            value=discord.utils.format_dt(member.joined_at, style='R'),
            inline=True
        )
        embed.add_field(name="Bot?", value="Yes" if member.bot else "No", inline=True)
        
        if roles:
            embed.add_field(
                name=f"Roles ({len(roles)})",
                value=', '.join(roles) if len(roles) <= 10 else f"{len(roles)} roles",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='serverinfo', aliases=['si'], description='Get information about the server')
    async def server_info(self, ctx: commands.Context):
        """Get information about the server"""
        guild = ctx.guild
        
        embed = discord.Embed(
            title=f"{guild.name}",
            color=discord.Color.blue(),
            timestamp=ctx.message.created_at
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(
            name="Created",
            value=discord.utils.format_dt(guild.created_at, style='R'),
            inline=True
        )
        
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        
        embed.add_field(name="Boost Level", value=guild.premium_tier, inline=True)
        embed.add_field(name="Boosts", value=guild.premium_subscription_count, inline=True)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))