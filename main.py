import random
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = True

bot =  commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Nós estamos prontos para começar, {bot.user.name}")

@bot.event
async def on_member_join(member):
    guild = member.guild
    role = discord.utils.get(guild.roles, name="Membro")
    if role not in member.roles:
        await member.add_roles(role)
        print(f"Adicionando o cargo {role.name} para {member.name}")

@bot.command()
async def cargo(ctx, rolename):
    guild = ctx.guild
    blocked_roles = ["ADM", "rollem", "Jockie Music"] #Cargos bloqueados
    role = discord.utils.get(guild.roles, name=rolename) #Detecta o cargo
    if role is None:
        await ctx.send(f"O cargo `{rolename}` não foi encontrado.") #Se o cargo não for encontrado, retorne esta mensagem.
        return
    if role not in ctx.author.roles:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention}, agora você tem o cargo **{role.name}**!")
    else:
        await ctx.send(f"{ctx.author.mention}, você já possui o cargo **{role.name}**.")
    if rolename in blocked_roles:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention}, você não pode adicionar o cargo **{role.name}**.")
        return

bot.run(token, log_handler=handler, log_level=logging.DEBUG)