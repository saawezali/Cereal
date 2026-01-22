import discord
from discord import app_commands
from discord.ext import commands
import random

class Games(commands.Cog):
    """Fun game commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.truth_questions = [
            "What's the most embarrassing thing you've ever done?",
            "What's your biggest fear?",
            "Have you ever lied to your best friend?",
            "What's your most unusual talent?",
            "What's the worst gift you've ever received?",
            "Who was your first crush?",
            "What's something you've never told anyone?",
            "What's your guilty pleasure?",
        ]
        
        self.dare_challenges = [
            "Send a message in all caps for the next 5 messages",
            "Change your nickname to something silly for 10 minutes",
            "Share an embarrassing photo",
            "Do 10 pushups and post a video",
            "Speak in rhymes for the next 3 messages",
            "Tell a joke in the chat",
            "Compliment everyone online right now",
            "Share your most used emoji and explain why",
        ]
        
        self.wyr_questions = [
            "Would you rather be able to fly or be invisible?",
            "Would you rather live in the past or the future?",
            "Would you rather have unlimited money or unlimited free time?",
            "Would you rather never use social media again or never watch a movie again?",
            "Would you rather be too hot or too cold?",
            "Would you rather fight 100 duck-sized horses or 1 horse-sized duck?",
            "Would you rather lose all your memories or never be able to make new ones?",
            "Would you rather have no internet or no phone?",
        ]
        
        self.nhie_statements = [
            "Never have I ever skipped school",
            "Never have I ever told a lie to get out of trouble",
            "Never have I ever stalked someone on social media",
            "Never have I ever pretended to be sick",
            "Never have I ever regifted something",
            "Never have I ever fallen asleep during a movie",
            "Never have I ever googled myself",
            "Never have I ever sent a text to the wrong person",
        ]
    
    @app_commands.command(name='truthordare', description='Play Truth or Dare')
    async def truth_or_dare(self, interaction: discord.Interaction):
        """Play Truth or Dare"""
        embed = discord.Embed(
            title="🎲 Truth or Dare",
            description="Choose Truth or Dare!",
            color=discord.Color.purple()
        )
        
        view = TruthOrDareView(self.bot, interaction.user, self.truth_questions, self.dare_challenges)
        await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(name='wouldyourather', description='Get a Would You Rather question')
    async def would_you_rather(self, interaction: discord.Interaction):
        """Get a Would You Rather question"""
        question = random.choice(self.wyr_questions)
        
        embed = discord.Embed(
            title="🤔 Would You Rather",
            description=question,
            color=discord.Color.gold()
        )
        embed.set_footer(text="Choose your option!")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='neverhaveiever', description='Play Never Have I Ever')
    async def never_have_i_ever(self, interaction: discord.Interaction):
        """Play Never Have I Ever"""
        statement = random.choice(self.nhie_statements)
        
        embed = discord.Embed(
            title="🙈 Never Have I Ever",
            description=statement,
            color=discord.Color.green()
        )
        embed.set_footer(text="Have you done this?")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='8ball', description='Ask the magic 8ball a question')
    @app_commands.describe(question='Your question for the magic 8ball')
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        """Ask the magic 8ball a question"""
        responses = [
            "It is certain.", "Without a doubt.", "Yes, definitely.",
            "You may rely on it.", "As I see it, yes.", "Most likely.",
            "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
            "Cannot predict now.", "Concentrate and ask again.",
            "Don't count on it.", "My reply is no.", "My sources say no.",
            "Outlook not so good.", "Very doubtful."
        ]
        
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            color=discord.Color.blue()
        )
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Answer", value=random.choice(responses), inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='rps', description='Play Rock Paper Scissors')
    @app_commands.describe(choice='Choose rock, paper, or scissors')
    @app_commands.choices(choice=[
        app_commands.Choice(name='Rock', value='rock'),
        app_commands.Choice(name='Paper', value='paper'),
        app_commands.Choice(name='Scissors', value='scissors')
    ])
    async def rock_paper_scissors(self, interaction: discord.Interaction, choice: str):
        """Play Rock Paper Scissors"""
        choice = choice.lower()
        bot_choice = random.choice(['rock', 'paper', 'scissors'])
        
        # Determine winner
        if choice == bot_choice:
            result = "🤝 It's a tie!"
            color = discord.Color.gold()
        elif (choice == 'rock' and bot_choice == 'scissors') or \
             (choice == 'paper' and bot_choice == 'rock') or \
             (choice == 'scissors' and bot_choice == 'paper'):
            result = "🎉 You win!"
            color = discord.Color.green()
        else:
            result = "😔 You lose!"
            color = discord.Color.red()
        
        embed = discord.Embed(title="✊ Rock Paper Scissors", color=color)
        embed.add_field(name="Your choice", value=choice.capitalize(), inline=True)
        embed.add_field(name="My choice", value=bot_choice.capitalize(), inline=True)
        embed.add_field(name="Result", value=result, inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='flip', description='Flip a coin')
    async def coin_flip(self, interaction: discord.Interaction):
        """Flip a coin"""
        result = random.choice(['Heads', 'Tails'])
        embed = discord.Embed(
            title="🪙 Coin Flip",
            description=f"The coin landed on **{result}**!",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='roll', description='Roll dice')
    @app_commands.describe(dice='Format: NdN (e.g., 2d6 for two 6-sided dice)')
    async def dice_roll(self, interaction: discord.Interaction, dice: str = "1d6"):
        """Roll dice (format: NdN, e.g., 2d6 for two 6-sided dice)"""
        try:
            rolls, sides = map(int, dice.split('d'))
            if rolls > 25 or sides > 100:
                return await interaction.response.send_message("❌ Too many dice or sides! Max: 25d100", ephemeral=True)
            
            results = [random.randint(1, sides) for _ in range(rolls)]
            total = sum(results)
            
            embed = discord.Embed(title="🎲 Dice Roll", color=discord.Color.blue())
            embed.add_field(name="Rolls", value=', '.join(map(str, results)), inline=False)
            embed.add_field(name="Total", value=str(total), inline=False)
            
            await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message("❌ Invalid format! Use NdN (e.g., 2d6)", ephemeral=True)
class TruthOrDareView(discord.ui.View):
    def __init__(self, bot, user, truths, dares):
        super().__init__(timeout=30.0)
        self.bot = bot
        self.user = user
        self.truths = truths
        self.dares = dares
    
    @discord.ui.button(label="Truth", style=discord.ButtonStyle.primary, emoji="💬")
    async def truth_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            return await interaction.response.send_message("This isn't your game!", ephemeral=True)
        
        result = random.choice(self.truths)
        embed = discord.Embed(
            title="💬 Truth",
            description=result,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Asked by {self.user.name}")
        await interaction.response.send_message(embed=embed)
        self.stop()
    
    @discord.ui.button(label="Dare", style=discord.ButtonStyle.danger, emoji="🎯")
    async def dare_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            return await interaction.response.send_message("This isn't your game!", ephemeral=True)
        
        result = random.choice(self.dares)
        embed = discord.Embed(
            title="🎯 Dare",
            description=result,
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Asked by {self.user.name}")
        await interaction.response.send_message(embed=embed)
        self.stop()
async def setup(bot):
    await bot.add_cog(Games(bot))