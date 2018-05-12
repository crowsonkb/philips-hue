"""A CLI tool to interface with Philips Hue lights."""

import argparse
import configparser
import pprint
import time

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import Terminal256Formatter
import qhue


class PrettyPrinter:
    def __init__(self, style='default'):
        self.lexer = Python3Lexer()
        self.fmtr = Terminal256Formatter(style=style)

    def pformat(self, s):
        pp = pprint.pformat(s)
        return highlight(pp, self.lexer, self.fmtr)

    def pprint(self, s):
        print(self.pformat(s))


def sgr(*args):
    return '\033[{}m'.format(';'.join(str(i) for i in args))


def setup(config):
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
    if cmd:
        cmd = 'bridge.' + cmd
    else:
        cmd = 'bridge()'
    if not cmd.endswith(')'):
        cmd = cmd + '()'
    my_globals = {'bridge': bridge}
    return eval(cmd, my_globals)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--config', default='philipshue.ini',
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

    b = qhue.Bridge(bridge_location, bridge_username)
    pp = PrettyPrinter()
    history = InMemoryHistory()
    while True:
        try:
            cmd = prompt('> ', history=history)
            start = time.perf_counter()
            out = exec_cmd(cmd, bridge=b)
            time_taken = time.perf_counter() - start
            pp.pprint(out)
            print(f'Time taken: {sgr(1, 34)}{time_taken*1000:.3f} ms{sgr(0)}')
        except (SyntaxError, qhue.QhueException) as err:
            print(f'{sgr(1, 31)}{err.__class__.__name__}{sgr(0)}: {err}')
            continue
        except (EOFError, KeyboardInterrupt):
            break
