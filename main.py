import discord,os,asyncio
from discord.ext import commands
from dotenv import load_dotenv
from aioconsole import ainput

intents = discord.Intents.all()
load_dotenv("keys.env")
token = os.environ.get("DISCORD_API_KEY") 
client = commands.Bot(command_prefix="!", intents=intents)

red = "\033[91m"
reset = "\033[0m"
blue = "\033[38;2;0;51;204m"
green = '\033[92m'
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} (ID: {client.user.id})')
    while True:
        banner =r'''
    ________      _____  ________                
    ___  __ )_______  /_ ___  __ \_______   __   
    __  __  |  __ \  __/ __  / / /  _ \_ | / /   
    _  /_/ // /_/ / /_   _  /_/ //  __/_ |/ /    
    /_____/ \____/\__/   /_____/ \___/_____/     
                                                
    _________                         ______     
    __  ____/____________________________  /____ 
    _  /    _  __ \_  __ \_  ___/  __ \_  /_  _ \
    / /___  / /_/ /  / / /(__  )/ /_/ /  / /  __/
    \____/  \____//_/ /_//____/ \____//_/  \___/ 
    '''
        print(f"{blue}{banner}{reset}")
        print('''
    0) Print server and owner info
    1) Print user count and other statistics
    2) Dm server owners
    3) Broadcast announcement
    4) Leave guild
    5) Quit
    ''')
        uinput = await ainput("Choose function: ")
        if uinput == '0':
            print('-' * 100)
            print(f'{"Guild Name":<35} | {"Owner":<20} | {"Members":<10}')
            print('-' * 100)
            for guild in client.guilds:
                owner_name = str(guild.owner) if guild.owner else f"Unknown (ID: {guild.owner_id})"
                print(f'''{green}{guild.name:<35} {reset}| {green}{owner_name:<20}{reset} |{green} {guild.member_count:<10}{reset}''')
            print('-' * 100)
        elif uinput == '1':
            total_members = sum(guild.member_count for guild in client.guilds)
            print(f"Number of users: {green}{total_members}{reset}")
            print(f"Ping: {green}{round(client.latency * 1000)}ms{reset}")
            print(f"Number of guilds the bot has been added to {green}{len(client.guilds)}{reset}")
            print(f"Number of shards {green}{client.shard_count if client.shard_count else 1}{reset}")
            print(f"Average number of members per server: {green}{round(total_members / len(client.guilds)) if client.guilds else 0}{reset}")
            print(f"Number of commands: {green}{len(client.commands)}{reset}")
        elif uinput == '2':
            try:
                print('-' * 100)
                print(f'{"Guild Name":<35} | {"Owner":<20} | {"Owner ID":<10}')
                print('-' * 100)
                for guild in client.guilds:
                    owner_name = str(guild.owner) if guild.owner else f"Unknown (ID: {guild.owner_id})"
                    print(f'{green}{guild.name:<35}{reset} |{green} {owner_name:<20}{reset} | {green}{guild.owner_id:<10}{reset}')
                print('-' * 100)
                owner_ = await ainput("Owner do you want to DM(Owner ID only): ")
                owner = await(client.fetch_user(owner_))
                message = await ainput("Message you want to send:  ")
                embed = discord.Embed(title=f"Message from the developer of {client.user.name} ", description=message, color=discord.Color.blue())
                embed.set_footer(text=client.user.name, icon_url=client.user.avatar)
                await owner.send(embed=embed)
            except Exception as e: print(e)
        elif uinput == '3':
            announcement = await ainput("Message to be broadcasted: ")
            embed = discord.Embed(title=f"📢 {client.user.name} Developer Update", description=announcement, color=discord.Color.blue())
            embed.set_footer(text=client.user.name, icon_url=client.user.avatar)

            for guild in client.guilds:
                try:
                    owner = guild.owner or await guild.fetch_member(guild.owner_id) 
                    await owner.send(embed=embed)

                    print(f"sent to {owner.name}")
                    await asyncio.sleep(5) 
                except Exception as e:
                    print(f"{red}Failed to alert owner of {guild.name}: {e}{reset}")
                    target_channel = None
                    for channel in guild.text_channels:
                        if channel.name == "serversentinel-update":
                            target_channel = channel
                            break
                    try:

                        if target_channel:
                            await target_channel.send(embed=embed)
                        else:

                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                                guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
                            }
                            new_channel = await guild.create_text_channel("serversentinel-update", overwrites=overwrites, reason="Developer Update")
                            await new_channel.send(embed=embed)
                    except discord.Forbidden:
                        print(f"Missing permissions to create/send in {guild.name}")
                    except Exception as e2:
                        print(f"Fallback failed in {guild.name}: {e2}")
            print("Broadcast complete.")
        elif uinput == '4':
            print('-' * 100)
            print(f'{"Guild Name":<35} | {"Owner":<20} | {"Members":<10} | {"Guild ID":<20}')
            print('-' * 100)
            for guild in client.guilds:
                owner_name = str(guild.owner) if guild.owner else f"Unknown (ID: {guild.owner_id})"
                print(f'{green}{guild.name:<35} {reset}|{green} {owner_name:<20}{reset} | {green}{guild.member_count:<10}{reset} |{green} {guild.id:<20}{reset}')
            print('-' * 100)
            guild_ = await ainput("Guild to leave(Guild ID only): ")
            guild =client.get_guild(int(guild_))
            await guild.leave()
            print(f"{red}Left {guild.name}{reset}")
        elif uinput == '5':
            await client.close()
            print(f"{red}Stopping program{reset}")


client.run(token)
