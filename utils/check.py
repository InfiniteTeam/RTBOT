import discord
from discord.ext import commands
from . import errors, datamgr

class Checks:
    def __init__(self,userdb):
        self.userdb=userdb
    
    async def registered(self, ctx: commands.Context):
        if ctx.author.id in userdb.keys():
            return True
        raise errors.NotRegistered

    def is_registered(self):
        return commands.check(self.registered)

    async def master(self, ctx: commands.Context):
        if ctx.author.id in [386715407697969173,467666650183761920,474094390441410561]:
            return True
        raise errors.NotMaster

    def is_master(self):
        return commands.check(self.master)