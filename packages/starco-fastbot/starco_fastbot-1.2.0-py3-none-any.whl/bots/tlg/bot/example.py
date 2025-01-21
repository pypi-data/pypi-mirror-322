

# from lib.admin import Admin
# from lib.user import User

# from bots.tlg.bot.util.packs import Start
# from bots.tlg.bot import TlgBot,Conversation
# from bots.tlg.bot.util.filteres import *

# def Admin(bot: TlgBot):
#     self = Conversation(Role.ADMIN.value)
#     self.menu_keys = [
#         ['managing', 'setting'],
#         ['statistics', 'support'],
#     ]
    # Start(self)
#     ##########################



from bots.tlg.bot.util.enum import *
from bots.tlg.bot import TlgBot
import os,sys


############################# Config ############################################
try:
    if sys.argv[1]=='test':
        os.environ["testMode"]="1"
except Exception as e:pass

token = ''
proxy =None
if os.environ.get("testMode","0")=="1":
    print('Run As TestMode')
    token = ''
    proxy = 'http://127.0.0.1:8889/'
bot_dir ='/root/bot_dir'
##########################################################################

bot = TlgBot(bot_dir, [1119223961], token, proxy=proxy, editors_id=[1119223961])

# bot.add_table('service_types', {'id': 0, 'title': '', 'del': 0})

bot.add_setting('off_support_pm','off_support_pm','texts',hide=1)
bot.add_setting('add_hi','سلام وقت تون بخیر','texts')

bot.init_db()

if __name__ == "__main__":
    bot.add(Admin(bot))
    bot.add(User(bot))