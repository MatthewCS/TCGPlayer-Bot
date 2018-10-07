import commands
import discord
import json

client = discord.Client()

@client.event
async def on_ready():
    print("Ay yo chief we good")

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    else:
        content = msg.content.lower()
        if len(content) < 4 or content[:4] != "tcg.":
            return
        else:
            await handle_message(msg)

async def handle_message(msg):
    # because discord.ext.commands is too simple for us.
    cmd_string = msg.content[4:]
    cmd = cmd_string.split()
    if cmd[0] in commands.commands.keys():
        func = commands.commands[cmd[0]]
        async with msg.channel.typing():
            await func(msg, cmd)

def main():
    with open("./keys.json") as f:
        keys = json.load(f)
    client.run(keys["discord"]["token"])

if __name__ == "__main__":
    main()
