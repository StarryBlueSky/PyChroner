# coding=utf-8
import discord

if not discord.opus.is_loaded():
    discord.opus.load_opus("opus")
