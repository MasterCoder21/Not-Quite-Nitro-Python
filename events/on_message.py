from discord.ext import commands
from discord import utils
import discord


class emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def getemote(self, arg:commands.EmojiConverter):
        # emoji = utils.get(self.bot.emojis, name=arg.strip(":"))

        return arg

    async def getinstr(self, content):
        ret = []

        spc = content.split(" ")
        cnt = content.split(":")

        if len(cnt) > 1:
            for item in spc:
                if item.count(":") > 1:
                    wr = ""
                    if item.startswith("<") and item.endswith(">"):
                        ret.append(item)
                    else:
                        cnt = 0
                        for i in item:
                            if cnt == 2:
                                aaa = wr.replace(" ", "")
                                ret.append(aaa)
                                wr = ""
                                cnt = 0

                            if i != ":":
                                wr += i
                            else:
                                if wr == "" or cnt == 1:
                                    wr += " : "
                                    cnt += 1
                                else:
                                    aaa = wr.replace(" ", "")
                                    ret.append(aaa)
                                    wr = ":"
                                    cnt = 1

                        aaa = wr.replace(" ", "")
                        ret.append(aaa)
                else:
                    ret.append(item)
        else:
            return content

        return ret

    # i added extra indent by mistake -_-

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if ":" in message.content:
            msg = [i for i in message.content.split(" ")]
            ret = ""
            em = False
            for word in msg:
                if word.startswith("<") and word.endswith(">"):
                    emoji = await self.getemote(word)
                    ret += f"{emoji} "
                else:
                    ret += f"{word} "


            webhooks = await message.channel.webhooks()
            webhook = utils.get(webhooks, name="Imposter NQN")
            if webhook is None:
                webhook = await message.channel.create_webhook(name="Imposter NQN")

            if len(ret) == 0:
                return
            await webhook.send(ret, username=message.author.name, avatar_url=message.author.avatar_url)
            await message.delete()


def setup(bot):
    bot.add_cog(emoji(bot))
