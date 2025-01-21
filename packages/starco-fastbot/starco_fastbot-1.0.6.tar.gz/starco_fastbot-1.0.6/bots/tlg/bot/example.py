
from bots.tlg.bot.util.enum import *
from bots.tlg.bot.util.functions import *
from bots.tlg.bot import TlgBot
from bots.tlg.bot.util.functions import setuper

# from lib.admin import Admin
# from lib.user import User

# from bots.tlg.bot.util.packs import Start
# def Admin(bot: TlgBot):
#     self = Conversation(Role.ADMIN.value, bot)
#     self.menu_keys = [
#         ['users', 'parameters'],
#     ]
#     ################################
#     self.pack(Start)


token = ''
proxy = None  # 'http://127.0.0.1:8889/'
db_configs = {
}

init={
    'setting':{
        'start_pm':setuper('سلام','',hide=1),
        'bot_status':setuper(str(1),'',type='int'),
    }
}
bot = TlgBot(
    token,
    1741889490,
    db_config=db_configs,
    db_tables_need_init=init,
    debug_mode=True,
    proxy=proxy,
    host_id='',
    scheduler_status=True,
    edit_mode=True,
    editors_id=[1741889490],
)


if __name__ == "__main__":
    # bot.add(Admin(bot))
    # bot.add(User(bot))
    bot.run_poll()
