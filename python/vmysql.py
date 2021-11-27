import vim
import json
import os 
import subprocess
import libtmux
from functools import update_wrapper
import typing as t
F = t.TypeVar("F", bound=t.Callable[..., t.Any])
if os.system("tmux ls") == 0:
    server = libtmux.Server()
    session = server.find_where({ "session_name": "mysql" })

def setupmethod(f: F) -> F:
    """Wraps a method so that it performs a check in debug mode if the
    first request was already handled.
    """

    def wrapper_func( *args: t.Any, **kwargs: t.Any) -> t.Any:
        if _is_account_exist(args[0]):
            raise AssertionError(
                    "this account is not defined in mysql_config.json"
            )
        return f( *args, **kwargs)

    return t.cast(F, update_wrapper(wrapper_func, f))

def panecheck(f: F) -> F:
    """Wraps a method so that it performs a check in debug mode if the
    first request was already handled.
    """

    def wrapper_func1( *args: t.Any, **kwargs: t.Any) -> t.Any:
        if _panecheck():
            raise AssertionError(
                    "panes numbers is larger then 3 I don't know which one to select !"
            )
        return f( *args, **kwargs)

    return t.cast(F, update_wrapper(wrapper_func1, f))

@panecheck
def send_message_c_l():
    stmt="c-l"
    _send_message(stmt)

@panecheck
def send_message_q():
    stmt="q"
    _send_message(stmt)

@panecheck
def send_message():
    stmt=vim.vars["mysql_stmt"]
    stmt = stmt.decode("utf-8")
    _send_message(stmt)


@setupmethod
def new_window(account):
    server = libtmux.Server()
    session = server.find_where({ "session_name": "mysql" })
    session.new_window(attach=True, window_name=account)
    pane = session.attached_window.attached_pane
    pane.send_keys("cd $HOME/mysql")
    pane.send_keys("vim "+account+".mysql")
    window = session.attached_window
    window.split_window(vertical=False)
    pane = window.attached_pane
    pane.send_keys("mymysql "+account)
    pane.send_keys("use "+database+";")
    window.select_pane("-R")


def _is_account_exist(account):
    configFile = os.environ['HOME']+"/dotfile/mysql_config.json"
    with open(configFile) as f:
        result = json.load(f)
        accounts= result['accounts']
        accounts = [account['nickName'] for account in accounts]
        print(accounts)
        print(account)
    return  account not in accounts 

def _panecheck():
    window = session.attached_window
    panes = window.panes
    if(len(panes)>2):
        return True
    return False

def _send_message(stmt):
    output = subprocess.Popen("tmux list-panes | grep \"active\" | cut -d':' -f1",shell=True,stdout=subprocess.PIPE)
    output=output.stdout.read()
    if (output[0] == 49):
        os.system("tmux send-keys -t 2 '" + stmt + "'")
    else:
        os.system("tmux send-keys -t 1 '" + stmt + "'")
