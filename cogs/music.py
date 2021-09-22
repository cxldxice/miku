import asyncio
from datetime import datetime
import discord
import youtube_dl
from discord.ext import commands

import assets
import utils


voice_client_class = discord.voice_client.VoiceClient


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.spotify = utils.get_spotify()

    async def __engine_play(self, ctx, source_url):
        voice_client = ctx.voice_client

        if voice_client:
            source = await discord.FFmpegOpusAudio.from_probe(executable="assets/ffmpeg.exe", source=source_url, **assets.FFMPEG_OPTIONS)

            voice_client.stop()
            voice_client.play(source)

        else:
            pass

    async def __send_card(self, ctx, info, now=True):
        card = discord.Embed(description=info["title"], color=(0x37c8be))

        if now:
            card.title = "Now playing"
        else:
            card.title = "Added to queue"
        
        card.set_image(url=info["thumbnail"])
        card.set_footer(text="cxldxice.github.io/miku")
        await ctx.send(embed=card)

    async def __join_in_channel(self, ctx):
        if ctx.author.voice is None:
            await ctx.reply("You're not in a voice channel!", mention_author=False)

        else:
            author_channel = ctx.author.voice.channel

            if ctx.voice_client is None:
                await author_channel.connect()
                #await ctx.reply(f"Miku connected to `{author_channel.name}`", mention_author=False)

            elif ctx.voice_client.channel is author_channel:
                await ctx.reply("Miku is already in your channel", mention_author=False)

            else:
                await ctx.voice_client.move_to(author_channel)
                #await ctx.reply(f"Miku moved to `{author_channel.name}`", mention_author=False)

    @commands.command("join")
    async def __join(self, ctx):
        await self.__join_in_channel(ctx)

    @commands.command("play")
    async def __play(self, ctx, *, undefined_input):
        if ctx.voice_client is None:
            await self.__join_in_channel(ctx)

        voice_client = ctx.voice_client
        input_type = utils.define_input(undefined_input)

        if input_type["url"]:
            if not input_type["playlist"]:
                if input_type["service"] == "youtube":
                    info = utils.get_youtube_info(undefined_input)
                else:
                    #other service
                    pass

            else:
                #playlist engine
                pass

        else:
            info = utils.get_youtube_info(undefined_input, query=True)
             
        try:
            self.queue[str(ctx.guild.id)].append(info)
        except:
            self.queue[str(ctx.guild.id)] = []
            self.queue[str(ctx.guild.id)].append(info)

        if not voice_client.is_playing():
            await self.__engine_play(ctx, info["source"])
            await self.__send_card(ctx, info)
            await self.__await_queue(ctx, info)

        else:
            await self.__send_card(ctx, now=False)

    async def __await_queue(self, ctx):
        if len(self.queue[str(ctx.guild.id)]) > 0:
            info = self.queue[str(ctx.guild.id)][0]
            del self.queue[str(ctx.guild.id)][0]
            await asyncio.sleep(info["duration"])
            
            try:
                info = self.queue[str(ctx.guild.id)][0]
                await self.__engine_play(ctx, info["source"])
                await self.__send_card(ctx, info)
                
                self.__await_queue()
            except:
                pass

            
        



def setup(bot):
    bot.add_cog(Music(bot))