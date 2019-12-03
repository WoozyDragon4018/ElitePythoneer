"""
Ping pong.
"""
import time
import discord
from discord.ext import commands

PING_CPU_PASSES = 20


class PingPongCog(commands.Cog):
    @commands.guild_only()
    @commands.command(aliases=["pong"])
    async def ping(self, ctx):
        """Get latencies of the bot"""
        # Calculate the message-send time. This is the time taken to the response.
        message_send_time = time.monotonic()

        pong_or_ping = (
            ":ping_pong: Ping!" if ctx.invoked_with == "pong" else ":ping_pong: Pong!"
        )

        msg = await ctx.send(f"{pong_or_ping}...")
        message_send_time = time.monotonic() - message_send_time

        heartbeat_latency = ctx.bot.latency

        # Calculate the event loop latency. This is a good representation of how
        # slow the loop is running. We spin the processor up first on the
        # current core to get an accurate measurement of speed when the CPU core
        # is under full load.

        # Time to do a round trip on the event loop, and time to callback.
        end_sync, end_async, end_fn = 0, 0, 0
        sync_latency, async_latency, function_latency = 0, 0, 0

        # Used to measure latency of a task.
        async def coro():
            """
            Empty coroutine that is used to determine the rough waiting time
            in the event loop.
            """
            pass

        # Measures time between the task starting and the callback being hit.
        def sync_callback(_):
            """
            Callback invoked once a coroutine has been ensured as a future.
            This measures the rough time needed to invoke a callback.
            """
            nonlocal end_sync
            end_sync = time.monotonic()

        def fn_callback():
            """
            Makes a guesstimate on how long a function takes to invoke relatively.
            """
            nonlocal end_fn
            end_fn = time.monotonic()

        for _ in range(0, 200):
            pass  # Dummy work to spin the CPU up

        for i in range(0, PING_CPU_PASSES):
            start = time.monotonic()
            async_call = ctx.bot.loop.create_task(coro())
            async_call.add_done_callback(sync_callback)
            await async_call
            end_async = time.monotonic()

            sync_latency += end_sync - start
            async_latency += end_async - start

            start = time.monotonic()
            fn_callback()
            function_latency += end_fn - start

        function_latency /= PING_CPU_PASSES
        async_latency /= PING_CPU_PASSES
        sync_latency /= PING_CPU_PASSES

        # We match the latencies with respect to the total time taken out of all
        # of them
        total_ping = 1.05 * (message_send_time + heartbeat_latency)
        total_loop = 1.05 * (async_latency + sync_latency + function_latency)

        message_send_time_pct = message_send_time * 100 / total_ping
        heartbeat_latency_pct = heartbeat_latency * 100 / total_ping
        async_latency_pct = async_latency * 100 / total_loop
        sync_latency_pct = sync_latency * 100 / total_loop
        function_latency_pct = function_latency * 100 / total_loop

        joiner = lambda *a: "\n".join(a)

        pong = joiner(
            f"```      WSS: {heartbeat_latency * 1_000: 8.2f}ms {self.make_progress_bar(heartbeat_latency_pct)} ",
            f"    HTTPS: {message_send_time * 1_000: 8.2f}ms {self.make_progress_bar(message_send_time_pct)} ",
            "",
            f"    Stack: {function_latency * 1_000_000: 8.2f}µs {self.make_progress_bar(function_latency_pct)} ",
            f"     Sync: {sync_latency * 1_000_000: 8.2f}µs {self.make_progress_bar(sync_latency_pct)} ",
            f"    Async: {async_latency * 1_000_000: 8.2f}µs {self.make_progress_bar(async_latency_pct)} ```",
        ).replace(" ", "\N{ZERO WIDTH SPACE}\N{FIGURE SPACE}")

        emb = discord.Embed(title=pong_or_ping, description=pong, colour=0xFE6B64)
        emb.set_footer(text=f"Requested by {ctx.author}")

        await msg.edit(content="", embed=emb)

    @staticmethod
    def make_progress_bar(percent):
        full = "\N{EM DASH}"
        empty = "\N{FIGURE SPACE}"
        percent_per_block = 5

        return "".join(
            full if i < percent else empty for i in range(0, 100, percent_per_block)
        )


def setup(bot):
    bot.add_cog(PingPongCog())
