"""A CLI tool to interface with Philips Hue lights."""

import argparse
import configparser
from pathlib import Path
import pprint
import sys
import time

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import style_from_pygments_cls
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import Python3Lexer
import qhue
import requests

from philips_hue.color import rgb_to_xybri
from philips_hue.friendly_mod import FriendlyStyle


try:
    from IPython.core import ultratb
    sys.excepthook = ultratb.FormattedTB()
except ImportError:
    pass


class PrettyPrinter:
    def __init__(self, style='default'):
        self.fmtr = Terminal256Formatter(style=style)

    def pformat(self, s):
        pp = pprint.pformat(s)
        return highlight(pp, Python3Lexer(), self.fmtr)

    def pprint(self, s):
        print(self.pformat(s), end='')

PP = PrettyPrinter(style=FriendlyStyle)


def sgr(*args):
    return '\033[{}m'.format(';'.join(str(i) for i in args))


def setup(config):
    resp = requests.get('https://www.meethue.com/api/nupnp')
    print('Detected Philips Hue Bridges:')
    PP.pprint(resp.json())
    location = prompt('Enter the Bridge IP address: ')
    username = qhue.create_new_username(location)
    cp = configparser.ConfigParser()
    cp.read(config)
    cf = cp['DEFAULT']
    cf['bridge_location'] = location
    cf['bridge_username'] = username
    with open(config, 'w') as configfile:
        cp.write(configfile)


def exec_cmd(cmd, bridge):
    if not cmd.startswith('bridge'):
        cmd = 'bridge.' + cmd
    my_globals = {'bridge': bridge, 'rgb_to_xybri': rgb_to_xybri}
    result = eval(cmd, my_globals)
    try:
        result = result()
    except TypeError:
        pass
    return result


def main():
    """The main function."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--config', default=str(Path.home() / '.philipshue.ini'),
                    help='the config file location')
    args = ap.parse_args()

    while True:
        try:
            cp = configparser.ConfigParser()
            cp.read(args.config)
            cf = cp['DEFAULT']
            bridge_location = cf['bridge_location']
            bridge_username = cf['bridge_username']
        except KeyError:
            setup(args.config)
            continue
        break

    bridge = qhue.Bridge(bridge_location, bridge_username)
    history = FileHistory(Path.home() / '.philipshue.hist')
    session = PromptSession(history=history)
    while True:
        try:
            cmd = session.prompt('>>> ', lexer=PygmentsLexer(Python3Lexer),
                                 style=style_from_pygments_cls(FriendlyStyle),
                                 auto_suggest=AutoSuggestFromHistory())
            start = time.perf_counter()
            out = exec_cmd(cmd, bridge=bridge)
            time_taken = time.perf_counter() - start
            PP.pprint(out)
            print(f'Time taken: {sgr(1, 34)}{time_taken*1000:.3f} ms{sgr(0)}')
        except KeyboardInterrupt:
            pass
        except EOFError:
            break
        except Exception as err:
            print(f'{sgr(1, 31)}{err.__class__.__name__}{sgr(0)}: {err}')
