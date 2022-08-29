import discord, asyncio, os, json, glob
from discord.ext import commands
from datetime import datetime

if not os.path.exists('settings'):
    os.mkdir('settings')
with open('settings.json', 'r', encoding='utf8') as f:
    awa = json.load(f)

bot = commands.Bot(command_prefix=awa['prefix'], help_command=None, intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("[Status Tracker]System is on ready.")
    await asyncio.sleep(3)
    while True:
        try:
            files = glob.glob('settings/*.json')
            for file in files:
                with open(file, 'r', encoding='utf8') as f:
                    wt1 = json.load(f)
                guild = bot.get_guild(wt1['gid'])
                for u in wt1['users']:
                    member = guild.get_member(u['id'])
                    if str(member.status) != u['activitynow']:
                        lastac = u['activitynow']
                        u['activitynow'] = str(member.status)
                        time_1 = datetime.strptime(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S")
                        time_2 = datetime.strptime(datetime.fromtimestamp(u["time"]).strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S")
                        time_interval = time_1-time_2
                        u['log'].append(f'[{str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))}]{lastac} lasted for {str(time_interval)}.')
                        if wt1['logtoggle'] == True:
                            try:
                                channel = bot.get_channel(wt1['logchannel'])
                                await channel.send(f'[User:{str(member)} | {str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))}]{lastac} lasted for {str(time_interval)}.\nNow change to **{str(member.status)}**.')
                            except:
                                pass
                        u['time'] = datetime.now().timestamp()
                dumpdata = json.dumps(wt1, ensure_ascii=False)
                with open(file, 'w', encoding = 'utf8') as f:
                    f.write(dumpdata)
            await asyncio.sleep(3)
        except:
            pass
                

@bot.event
async def on_guild_join(guild):
    if not os.path.exists(f'settings/{str(guild.id)}.json'):
        jsondata = {'gid':guild.id, 'users':[], "logchannel":None, "logtoggle":False}
        dumpdata = json.dumps(jsondata, ensure_ascii=False)
        with open(f'settings/{str(guild.id)}.json', 'w', encoding = 'utf8') as f:
            f.write(dumpdata)
@bot.command()
async def reset(ctx):
    au = ctx.author
    roles = au.roles
    isa = 0
    for a in roles:
        for c in a.permissions:
            if c[0] == 'administrator' and c[1] == True:
                isa = 1
    if ctx.author.id == ctx.guild.owner.id:
        isa = 1
    if isa == 1:
        jsondata = {'gid':ctx.guild.id, 'users':[], "logchannel":None, "logtoggle":False}
        dumpdata = json.dumps(jsondata, ensure_ascii=False)
        with open(f'settings/{str(ctx.guild.id)}.json', 'w', encoding = 'utf8') as f:
            f.write(dumpdata)
        
        await ctx.send('Reset complete.')
    else:
        await ctx.send('You dont have permission ``administrator``.')

@bot.group()
async def tracker(ctx):
    pass
@tracker.command()
async def track(ctx, userid):
    au = ctx.author
    roles = au.roles
    isa = 0
    for a in roles:
        for c in a.permissions:
            if c[0] == 'administrator' and c[1] == True:
                isa = 1
    if ctx.author.id == ctx.guild.owner.id:
        isa = 1
    if isa == 1:
        if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
            try:
                with open(f'settings/{str(ctx.guild.id)}.json', 'r', encoding = 'utf8') as f:
                    wt1 = json.load(f)
                user = ctx.guild.get_member(int(str(userid).replace('<', '').replace('>', '').replace('!', '').replace('@', '')))
                exists = False
                for u in wt1['users']:
                    if u['id'] == user.id:
                        exists = True
                        break
                if exists == False:
                    wt1['users'].append({"id":user.id, "log":[], "activitynow":str(user.status), "time":datetime.now().timestamp()})
                    jsondata = json.dumps(wt1, ensure_ascii=False)
                    with open(f'settings/{str(ctx.guild.id)}.json', 'w', encoding = 'utf8') as f:
                        f.write(jsondata)
                    await ctx.send(f'Start tracking {user.mention}.\n``一生只追蹤你一人``')
                else:
                    await ctx.send('Error because ``User is tracked``.')
            except Exception as e:
                await ctx.send(f'Error because ``{str(e)}``.')
        else:
            await ctx.send(f'Lost file ``settings/{str(ctx.guild.id)}.json``\nPlease use ``>>reset``.')
    else:
        await ctx.send('You dont have permission ``administrator``.')
@tracker.command()
async def untrack(ctx, userid):
    au = ctx.author
    roles = au.roles
    isa = 0
    for a in roles:
        for c in a.permissions:
            if c[0] == 'administrator' and c[1] == True:
                isa = 1
    if ctx.author.id == ctx.guild.owner.id:
        isa = 1
    if isa == 1:
        if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
            try:
                with open(f'settings/{str(ctx.guild.id)}.json', 'r', encoding = 'utf8') as f:
                    wt1 = json.load(f)
                user = ctx.guild.get_member(int(str(userid).replace('<', '').replace('>', '').replace('!', '').replace('@', '')))
                exists = False
                for u in wt1['users']:
                    if u['id'] == user.id:
                        exists = True
                        break
                if exists == True:
                    ndata = []
                    for u in wt1['users']:
                        if u['id'] == user.id:
                            continue
                        ndata.append(u)
                    wt1['users'] = ndata
                    jsondata = json.dumps(wt1, ensure_ascii=False)
                    with open(f'settings/{str(ctx.guild.id)}.json', 'w', encoding = 'utf8') as f:
                        f.write(jsondata)
                    await ctx.send(f'Untrack {user.mention}.')
                else:
                    await ctx.send('Error because ``User isnt tracked``.')
            except Exception as e:
                await ctx.send(f'Error because ``{str(e)}``.')
        else:
            await ctx.send(f'Lost file ``settings/{str(ctx.guild.id)}.json``\nPlease use ``>>reset``.')
    else:
        await ctx.send('You dont have permission ``administrator``.')
@tracker.command()
async def list(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        try:
            with open(f'settings/{str(ctx.guild.id)}.json', 'r', encoding = 'utf8') as f:
                wt1 = json.load(f)
            msg = ''
            for i, u in enumerate(wt1['users']):
                tu = bot.get_user(u['id'])
                msg += f"[{str(i)}]{str(tu)}(id:{str(tu.id)})\n"
            if msg == '':
                msg = 'Nobody is tracked.'
            await ctx.send(f'**Tracking List**\n{msg}')
        except Exception as e:
            await ctx.send(f'Error because ``{str(e)}``.')
    else:
        await ctx.send(f'Lost file ``settings/{str(ctx.guild.id)}.json``\nPlease use ``>>reset``.')

@bot.group()
async def log(ctx):
    pass
@log.command()
async def toggle(ctx):
    au = ctx.author
    roles = au.roles
    isa = 0
    for a in roles:
        for c in a.permissions:
            if c[0] == 'administrator' and c[1] == True:
                isa = 1
    if ctx.author.id == ctx.guild.owner.id:
        isa = 1
    if isa == 1:
        if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
            try:
                with open(f'settings/{str(ctx.guild.id)}.json', 'r', encoding = 'utf8') as f:
                    wt1 = json.load(f)
                if wt1['logtoggle'] == False:
                    wt1['logtoggle'] = True
                else:
                    wt1['logtoggle'] = False
                jsondata = json.dumps(wt1, ensure_ascii=False)
                with open(f'settings/{str(ctx.guild.id)}.json', 'w', encoding = 'utf8') as f:
                    f.write(jsondata)
                
                if wt1['logtoggle'] == True:
                    await ctx.send('Log message is ``enabled`` now.')
                else:
                    await ctx.send('Log message is ``disabled`` now.')
            except Exception as e:
                await ctx.send(f'Error because ``{str(e)}``.')
        else:
            await ctx.send(f'Lost file ``settings/{str(ctx.guild.id)}.json``\nPlease use ``>>reset``.')
    else:
        await ctx.send('You dont have permission ``administrator``.')
@log.command()
async def check(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        try:
            with open(f'settings/{str(ctx.guild.id)}.json', 'r', encoding = 'utf8') as f:
                wt1 = json.load(f)
            
            if wt1['logtoggle'] == True:
                await ctx.send(f'Log message is ``enable`` now.\nLog message channel id:{str(wt1["logchannel"])}')
                try:
                    channel = bot.get_channel(wt1['logchannel'])
                    tid = channel.id
                except:
                    await ctx.send('[WARN]Log message channel is **invaild**.')
            else:
                await ctx.send('Log message is ``disabled`` now.')
        except Exception as e:
            await ctx.send(f'Error because ``{str(e)}``.')
    else:
        await ctx.send(f'Lost file ``settings/{str(ctx.guild.id)}.json``\nPlease use ``>>reset``.')
@log.command()
async def logchannel(ctx):
    au = ctx.author
    roles = au.roles
    isa = 0
    for a in roles:
        for c in a.permissions:
            if c[0] == 'administrator' and c[1] == True:
                isa = 1
    if ctx.author.id == ctx.guild.owner.id:
        isa = 1
    if isa == 1:
        if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
            try:
                with open(f'settings/{str(ctx.guild.id)}.json', 'r', encoding = 'utf8') as f:
                    wt1 = json.load(f)
                wt1['logchannel'] = ctx.channel.id
                jsondata = json.dumps(wt1, ensure_ascii=False)
                with open(f'settings/{str(ctx.guild.id)}.json', 'w', encoding = 'utf8') as f:
                    f.write(jsondata)
                
                await ctx.send(f'Log message channel is changed to {ctx.channel.mention} now.')
            except Exception as e:
                await ctx.send(f'Error because ``{str(e)}``.')
        else:
            await ctx.send(f'Lost file ``settings/{str(ctx.guild.id)}.json``\nPlease use ``>>reset``.')
    else:
        await ctx.send('You dont have permission ``administrator``.')

@bot.group()
async def status(ctx):
    pass
@status.command()
async def now(ctx, userid):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        try:
            with open(f'settings/{str(ctx.guild.id)}.json', 'r', encoding = 'utf8') as f:
                wt1 = json.load(f)
            user = ctx.guild.get_member(int(str(userid).replace('<', '').replace('>', '').replace('!', '').replace('@', '')))
            exists = False
            tdata = None
            for u in wt1['users']:
                if u['id'] == user.id:
                    exists = True
                    tdata = u
                    break
            if exists == True:
                time_1 = datetime.strptime(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S")
                time_2 = datetime.strptime(datetime.fromtimestamp(u["time"]).strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S")
                time_interval = time_1-time_2
                await ctx.send(f"**{user.mention}'s Status**\nStatus:{str(user.status)}\nElasped for {time_interval}(Start from {datetime.fromtimestamp(u['time']).strftime('%Y/%m/%d %H:%M:%S')})")
            else:
                await ctx.send('Error because ``User isnt tracked``.')
        except Exception as e:
            await ctx.send(f'Error because ``{str(e)}``.')
    else:
        await ctx.send(f'Lost file ``settings/{str(ctx.guild.id)}.json``\nPlease use ``>>reset``.')
@status.command()
async def log(ctx, userid):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        try:
            with open(f'settings/{str(ctx.guild.id)}.json', 'r', encoding = 'utf8') as f:
                wt1 = json.load(f)
            user = ctx.guild.get_member(int(str(userid).replace('<', '').replace('>', '').replace('!', '').replace('@', '')))
            exists = False
            tdata = None
            for u in wt1['users']:
                if u['id'] == user.id:
                    exists = True
                    tdata = u
                    break
            if exists == True:
                msg = f"## {str(user)}'s status log ##\n"
                for l in tdata['log']:
                    msg += l + '\n'
                time_1 = datetime.strptime(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S")
                time_2 = datetime.strptime(datetime.fromtimestamp(tdata["time"]).strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S")
                time_interval = time_1-time_2
                msg += f"\n## Status Now:{str(user.status)} | Elasped for {time_interval}(Start from {datetime.fromtimestamp(tdata['time']).strftime('%Y/%m/%d %H:%M:%S')}) ##"
                with open('settings.json', 'r', encoding='utf8') as f:
                    awaawa = json.load(f)
                with open(f'temp_{str(awaawa["tempnum"])}.txt', 'w', encoding = 'utf8') as f:
                    f.write(msg)
                file = discord.File(f'temp_{str(awaawa["tempnum"])}.txt')
                await ctx.send(file = file)
                os.remove(f'temp_{str(awaawa["tempnum"])}.txt')
                awaawa['tempnum'] += 1
                with open('settings.json', 'w', encoding = 'utf8') as f:
                    dumpdata = json.dumps(awaawa, ensure_ascii=False)
                    f.write(dumpdata)
            else:
                await ctx.send('Error because ``User isnt tracked``.')
        except Exception as e:
            await ctx.send(f'Error because ``{str(e)}``.')
    else:
        await ctx.send(f'Lost file ``settings/{str(ctx.guild.id)}.json``\nPlease use ``>>reset``.')

@bot.command(aliases=['fbk'])
async def fubuki(ctx):
    await ctx.send('https://imgur.com/RvjMEnn')
@bot.command(aliases=['help', 'cmd'])
async def cmds(ctx):
    await ctx.send(f"""**Command List**
Bot Prefix: ``{awa['prefix']}``

**General**
{awa['prefix']}cmds - Command List(aliases:cmd, help)
{awa['prefix']}reset - Reset settings file(Permission ``administrator`` needed).
**Tracker**
{awa['prefix']}tracker track <Member> - Start tracking the member you mentioned(Permission ``administrator`` needed).
{awa['prefix']}tracker untrack <Member> - Untrack the member you mentioned(Permission ``administrator`` needed).
{awa['prefix']}tracker list - Tracker list.
**Log**
{awa['prefix']}log toggle - Enable/Disable log message(Permission ``administrator`` needed).
{awa['prefix']}log channel - Set the channel where you use the command as log message channel(Permission ``administrator`` needed).
{awa['prefix']}log check - Check log message channel and whether log message is enabled.
**Status**
{awa['prefix']}status now <Member> - Check the member you mentioned's status.
{awa['prefix']}status log <Member> - Check the member you mentioned's status log.

Status Tracker v{str(awa['version'])} by {awa['author']}""")

bot.run(awa['token'])