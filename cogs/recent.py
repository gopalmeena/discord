import discord
from discord.ext import commands
from .utils.db import fetch_query


class Recent(commands.Cog):
    def __init__(self, bot):
        """
        This class is for !recent command. !recent command return
        all the queries for which given query is substring.
        """
        self.bot = bot

    @commands.command()
    async def recent(self, ctx, *, search_query):
        search_query = search_query.strip()
        # retrieve user queries
        user_id = ctx.message.author.id
        queries = self.get_recent_queries(str(user_id), str(search_query))
        await ctx.send('\n'.join(queries))

    def get_recent_queries(self, user_id, search_query):
        queries = fetch_query(user_id, search_query)
        return [query[0] for query in queries]

def setup(bot):
    bot.add_cog(Recent(bot))