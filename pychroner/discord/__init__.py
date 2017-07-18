# coding=utf-8
from logging import getLogger

import discord

logger = getLogger(__name__)

if not discord.opus.is_loaded():
    try:
        discord.opus.load_opus("opus")
    except:
        logger.warning("Discord.py could not load Opus library. So PyChroner may not be connecting Discord VC like MusicBot.")
