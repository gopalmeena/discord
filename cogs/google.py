import discord
import os
from datetime import datetime
from discord.ext import commands
from googleapiclient.discovery import build

from .utils.db import persist_query
from .utils.logger import logger

class Google(commands.Cog):
    def __init__(self, bot):
        """
        This class is for !google command. !google command return
        top 5 google result link and persist given query in database.
        """
        self.bot = bot

    @commands.command()
    async def google(self, ctx, *, search_query):
        search_query = search_query.strip()
        # persist user query
        searched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        user_id = ctx.message.author.id
        self.persist_search_query(str(user_id), str(search_query), searched_at)
        # get top 5 results from google custom search
        result_links = self.google_search(search_query)
        await ctx.send('\n'.join(result_links))


    def google_search(self, search_query):
        # actual results received from normal google search and results returned from this api may differ.
        # For more info: https://support.google.com/customsearch/answer/70392?hl=en
        service = build("customsearch", "v1", developerKey=os.environ.get("DEVELOPER_KEY"))
        result = service.cse().list(q=search_query,cx=os.environ.get("CX_ID"), num=5).execute()

        try:
            items = result["items"]
            return [item["link"] for item in items]
        except Exception as e:
            logger.exception(e)

    def persist_search_query(self, user_id, search_query, searched_at):
        return persist_query(user_id, search_query, searched_at)


def setup(bot):
    bot.add_cog(Google(bot))
