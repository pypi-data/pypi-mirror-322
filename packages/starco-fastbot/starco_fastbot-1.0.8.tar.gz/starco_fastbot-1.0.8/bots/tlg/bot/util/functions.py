import os,shutil
from .enum import *
from .filteres import *
from ..classes import Conversation
from telegram.ext import Filters
import time
from utility import directory_creator,root_path,ZipUtility

def setuper(value:str,subset:str,unit:str='',type:str='',hide:int=0,toggle:int=0):
    return {'value':value,'subset':subset,'unit':unit,'type':type,'hide':hide,'toggle':toggle}


def backup_database(self,chat_id=''):
    try:
        path = self.db.path
        database_dir = directory_creator(['database'])
        shutil.copy2(path,database_dir)
        zip_path = root_path()+'/database.zip'
        ziper=ZipUtility()
        ziper.zip_files(database_dir,zip_path)
        print(zip_path)
        with open(zip_path,'rb') as f:
            if chat_id=='':chat_id = self.host_id
            print(chat_id)
            self.bot.bot.send_document(chat_id, f,caption=self.get_bot_username())
    finally:
        try:os.remove(zip_path)
        except:pass
        try:shutil.rmtree(database_dir)
        except:pass

def get_product(self,id:int,status=CONFIRMED):
    try:
        return self.db.do('products',condition=f"id={id} AND status={status}")[0]
    except:return {}

def get_orders_by_pid(self,pid:int,status=WAITING):
    try:
        return self.db.do('orders',condition=f"pid={pid} AND status={status}")
    except:return []

def get_order(self,id:int,status=WAITING):
    try:
        return self.db.do('orders',condition=f"id={id} AND status={status}")[0]
    except:return {}

def setup_force_join(self):
    e = Node()
    e.filters = match_btn('force_join', self)

    def act(self: Conversation, *args):
        force_joins = self.db.do('force_join')
        if force_joins:
            self.send('lists', [['add_force_join'], [self.back_menu_key]])

            for i in force_joins:
                msg = f"{self.text('title',slash=True)}: {i['title']}\n"
                msg += f"{self.text('channel_id',slash=True)}: {i['channel_id']}"
                msg += f"{self.text('link',slash=True)}: {i['link']}"
                self.send(msg, {'delete_fj': i['id']}, t=False)
        else:
            self.send('no_item', [['add_force_join'], [self.back_menu_key]])
        return -1
    e.callback = act
    self.node('force_join', [e])
    ########################################
    e = Node()
    e.pattern = self.check_inline_keyboards('delete_fj')

    def act(self: Conversation, *args):
        id = int(self.splited_query_data()[1])
        self.db.do('force_join', delete=True)
        self.edit_message_text('deleted', self.get_msg_id())
        return -1
    e.callback = act
    self.node('delete_fj', [e])
    ########################################
    e = Node()
    e.filters = match_btn('add_force_join', self)
    e.msg = 'enter_title'
    e.btn = [[self.back_menu_key]]

    s = Node()
    s.filters = Filters.text
    s.msg = 'enter_channel_id'
    s.btn = [[self.back_menu_key]]

    s1 = Node()
    s1.filters = Filters.text
    s1.msg = 'enter_channel_link'
    s1.btn = [[self.back_menu_key]]

    s2 = Node()
    s2.filters = Filters.text
    def act(self: Conversation, *args):
        title = self.userdata(self.stat_key('add_force_join', 1))['text']
        channel_id = self.userdata(self.stat_key('add_force_join', 2))['text']
        link = self.get_text()
        self.db.do('force_join', {'id': self.time(), 'title': title,'channel_id':channel_id, 'link': link,'status':CONFIRMED})
        self.send('done', self.menu_keys)
        return -1

    s2.callback = act
    self.node('add_force_join', [e], [[s],[s1], [s2]])
 
import os

def path_maker(path_list=[],relative_path='.',start_path=None):
    '''
    start_path=None=>os.getcwd()
    '''
    if (sep_path := os.environ.get('start_path',''))!='':
        p = os.path.dirname(__file__).split(sep_path)[0]+sep_path
        p = p.rstrip(os.sep)
    else:
        start_path = os.getcwd() if start_path==None else start_path
        p = os.path.abspath(os.path.join(start_path,relative_path))
    for i in path_list:
        p += '/'+str(i)
        if not os.path.exists(p):
            os.mkdir(p)
    return p