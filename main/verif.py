import discord
import datetime

from discord.ui import View, Button
from discord.ext import commands
from discord.utils import get

from database.postgresql import pcursor
from bot import bot
from .faceit import faceit_get_player_elo
from .playtime import playtime


def from_steam64(sid: str):
    y = int(sid) - 76561197960265728
    x = y % 2
    return f"STEAM_1:{x}:{(y - x) // 2}"


class VerifButtons(View):
    def __init__(self):
        super().__init__(timeout=None)

        button = Button(style=discord.ButtonStyle.url,
                        url="https://yacheru.ru/login", label="Привязать")
        self.add_item(button)

        button = Button(style=discord.ButtonStyle.blurple,
                        label="Обновить роли", custom_id="update-roles")
        self.add_item(button)

        async def button_callback(inter: discord.Interaction):
            try:
                await inter.response.defer(thinking=True, ephemeral=True)
                pcursor.execute("SELECT steam FROM connections WHERE user_id = %s", (inter.user.id,))
                data = pcursor.fetchone()

                if data:
                    if data[0] is not None:
                        faceit_level = faceit_get_player_elo(user=inter.user.id, steamid=data[0])
                        steamid = from_steam64(data[0])
                        valid_role = get(inter.guild.roles, id=1159334533913661450)
                        roles = []
                        roles_to_add = []
                        roles_names = []

                        if faceit_level:
                            role_map = {
                                1: [1146225914355646494, "<:1_:1158680548970074154>"],
                                2: [1146226059600212068, "<:2_:1158680552367456296>"],
                                3: [1146226079560912946, "<:3_:1158680554275864656>"],
                                4: [1146226099999752353, "<:4_:1158680557346095134>"],
                                5: [1146226121575252079, "<:5_:1158680559065763871>"],
                                6: [146226141619822652, "<:6_:1158680562551234600>"],
                                7: [114622619094064743, "<:7_:1158680564191215616>"],
                                8: [1146226227116523561, "<:8_:1158680567160766485>"],
                                9: [1146226622211555409, "<:9_:1158680569337618484>"],
                                10: [1146226259681087590, "<:10:1158680572466561075>"]
                            }

                            faceit_icon = role_map.get(
                                faceit_level, [None, None])[1]

                            faceit_role_id = role_map.get(
                                faceit_level, [None, None])[0]

                            faceit_role = get(inter.guild.roles, id=faceit_role_id)
                            roles.append(f"{faceit_role.mention} {faceit_icon}")
                            roles_to_add.append(faceit_role)
                            roles_names.append(faceit_role.name)

                        if valid_role:
                            roles.append(f"{valid_role.mention} <:valid:1159335185830125588>")
                            roles_to_add.append(valid_role)
                            roles_names.append(valid_role.name)

                        if steamid:
                            timeroleid = playtime(
                                user=inter.user.id, steamid=steamid)
                            timerole = get(inter.guild.roles, id=timeroleid)
                            roles.append(f"{timerole.mention} <:time:1160165904080977920>")
                            roles_to_add.append(timerole)
                            roles_names.append(timerole.name)

                        await inter.user.add_roles(*roles_to_add)

                        embed = discord.Embed(title="Вы прошли верификацию!", description=f"Вы получили роли: {', '.join(roles)}", color=discord.Colour.blurple(), timestamp=datetime.datetime.now())
                        embed.set_thumbnail(url=inter.user.avatar.url if inter.user.avatar else inter.user.default_avatar)
                        await inter.followup.send(embed=embed, ephemeral=True)
                        print(f"[{datetime.datetime.now().strftime('%H:%M:%S, %d/%m')}] [VERIF] [INFO] USER: {inter.user.name} GET ROLES: {', '.join(roles_names)}")
                    else:
                        await inter.followup.send("Ваш steam-профиль не был найден. Пожалуйста, укажите свой steam-профиль в [интеграциях](https://support.discord.com/hc/en-us/articles/8063233404823-Connections-Linked-Roles-Community-Members) и пройдите [привязку](https://yacheru.ru/login)", ephemeral=True)
                else:
                    await inter.followup.send("Вы ещё не прошли [привязку](https://yacheru.ru/login). Пройдите её и повторите своё нажатие.", ephemeral=True)
            except Exception as e:
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S, %d/%m')}] [VERIF] [ERROR] WITH CODE: {e}")
        button.callback = button_callback


class VerifButton(View):
    def __init__(self):
        super().__init__(timeout=None)

        button = Button(style=discord.ButtonStyle.url,
                        url="https://yacheru.ru/login", label="Привязать")
        self.add_item(button)


@bot.command()
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def verif(ctx: commands.Context):
    await ctx.channel.purge(limit=1)
    embed_img = discord.Embed(title="", description="",
                              color=discord.Colour.blurple())
    embed_img.set_image(url="https://cdn.discordapp.com/attachments/1129601347352809532/1160178547340615752/7490d612b8f3175a.png?ex=6533b778&is=65214278&hm=4bbaebf03e667e10ee5f18d812ae6dc04f9a32b75ce2fa2a2324d2c1e3d1e88b&")

    embed = discord.Embed(title="Верификация", description="Привяжите свой steam-профиль к [discord-аккаунту](https://support.discord.com/hc/en-us/articles/8063233404823-Connections-Linked-Roles-Community-Members) и пройдите процесс [привязки](https://yacheru.ru/login), чтобы получить некоторые серверные роли и открыть полный доступ к серверу:\n\n- <:faceit:1158655587488370729> Lvl Faceit\n- <:time:1160165904080977920> общий онлайн на INFINITY\n- <:valid:1159335185830125588> Роль пройденной верификации: <@&1159334533913661450>", color=discord.Colour.blurple())
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/1129601347352809532/1145402533750259842/f165c33c6d13951e.png")
    await ctx.send(embeds=[embed_img, embed], view=VerifButtons())


@bot.tree.command(name="steam", description="Мой steam-профиль")
async def steam(inter: discord.Interaction):
    pcursor.execute(
        "SELECT steam FROM connections WHERE user_id = %s", (inter.user.id,))
    data = pcursor.fetchone()

    embed = discord.Embed(
        title="", color=discord.Colour.dark_embed(), timestamp=datetime.datetime.now())
    embed.set_author(name=f"{inter.user.name}",
                     icon_url=inter.user.avatar.url if inter.user.avatar else inter.user.default_avatar)
    embed.set_footer(icon_url=inter.guild.icon.url)

    if data:
        embed.add_field(
            name="", value=f"Ваш steam профиль: https://steamcommunity.com/profiles/{data[0]}/")
        await inter.response.send_message(embed=embed)
    else:
        embed.add_field(
            name="", value="Ваш steam-профиль не найден. Убедитесь, что привязали его в интеграциях своего профиля discord. После чего [перейдите по ссылке](https://yacheru.ru/login) и пройдите процесс привязки\n- Узнать больше об интеграциях: [__**Клик**__](https://support.discord.com/hc/en-us/articles/8063233404823-Connections-Linked-Roles-Community-Members)")
        await inter.response.send_message(embed=embed, view=VerifButton())
