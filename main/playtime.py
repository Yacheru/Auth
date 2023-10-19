import time
import datetime
from database.mysql import check_and_reconnect, connect_to_database
from database.postgresql import pcursor


def playtime(user: int, steamid: str):
    try:
        table_names = [
            'u3978_levels_ranks.lvl_base',
            'u3978_levels_ranks1.lvl_base',
            'u3978_levels_ranks2.lvl_base',
            'u3978_levels_ranks3.lvl_base',
            'u3978_levels_ranks4.lvl_base',
            'u3978_levels_ranks5.lvl_base',
            'u3978_levels_ranksaimonl.lvl_base',
            'u3978_levels_ranksawponly.lvl_base',
            'u3978_levels_ranksdm.lvl_base',
            'u3978_levels_ranksmaniac.lvl_base',
            'u3978_levels_ranksmigeim.lvl_base',
            'u3978_levels_ranksp1.lvl_base',
            'u3978_levels_ranksretake.lvl_base',
            'u3978_rankmirage.lvl_base',
            'u3978_rankmirage2.lvl_base',
            'u3978_rankmirage3.lvl_base',
            'u3978_rankmirageded2.lvl_base',
            'u3978_ranksarenakaz.lvl_base',
            'u3978_ranksdust2.lvl_base'
        ]

        total_playtime = 0
        timespend = 0

        connection = connect_to_database()
        connection = check_and_reconnect(connection)
        mcursor = connection.cursor()

        for table_name in table_names:
            now = time.time()

            mcursor.execute(f"SELECT playtime FROM {table_name} WHERE steam = %s", (steamid,))
            result = mcursor.fetchall()

            timespend += time.time() - now

            for row in result:
                total_playtime += row['playtime']
                
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S, %d/%m')}] [MYSQL] TIME SPEND TO FETCHING DATA: {timespend}")

        number_ranges = {
            (0, 9): 1159044396596080660,
            (10, 19): 1159042119021887539,
            (20, 29): 1161506832947355819,
            (30, 39): 1159042447716921344,
            (40, 49): 1161533022718398585,
            (50, 59): 1159042247539572786,
            (60, 69): 1161506968993792101,
            (70, 79): 1159042324123361290,
            (80, 89): 1159042537785401355,
            (90, 99): 1161507036400451695,
            (100, 119): 1159042570689724456,
            (120, 149): 1159042894489976933,
            (150, 199): 1159042946507735070,
            (200, 249): 1159042995849547840,
            (250, 299): 1159043028024049724,
            (300, 349): 1159043054351695882,
            (350, 399): 1159043092406603797,
            (400, 449): 1159043198312788008,
            (450, 499): 1159043250263441430,
            (500, 599): 1159043335604940820,
            (600, 699): 1159043373219463208,
            (700, 799): 1159043412746579978,
            (800, 899): 1159043442593247282,
            (900, 999): 1159043469382275092,
            (1000, 1099): 1159043507516874773,
            (1100, 1199): 1161506344650678303,
            (1200, 1299): 1161506424334057602,
            (1300, 1399): 1161506469288620124,
            (1400, 1499): 1161506506827649055,
            (1500, 9999999): 1161506546732253234,
        }

        number_to_check = total_playtime // 3600

        pcursor.execute("UPDATE connections SET infhours = %s WHERE user_id = %s", (number_to_check, user,))

        for range_, message in number_ranges.items():
            if range_[0] <= number_to_check <= range_[1]:
                return message
    except Exception as e:
        print(f"[PLAYTIME] [ERROR] WITH CODE: {e}")