"""A CLI tool to interface with Philips Hue lights."""

import argparse
import configparser
from enum import Enum
import os
from pathlib import Path
import sys
import time

import prettyprinter
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.layout.processors import HighlightMatchingBracketProcessor
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import style_from_pygments_cls
from pygments.lexers import Python3Lexer
from pygments.styles.friendly import FriendlyStyle
from pygments.styles.monokai import MonokaiStyle
from pygments_style_monokailight.monokailight import MonokaiLightStyle
import requests
import qhue

from philips_hue.color import mired, rgb_to_xybri


try:
    from IPython.core import ultratb
    sys.excepthook = ultratb.FormattedTB()
except ImportError:
    pass


class BGColor(Enum):
    """Represents our state of knowledge about the terminal background color."""
    UNKNOWN = 0
    DARK = -1
    LIGHT = 1


def get_bg_color():
    """Returns :data:`BGColor.UNKNOWN` if the terminal background color could
    not be determined; otherwise, :data:`BGColor.LIGHT` if the terminal has a
    light background and :data:`BGColor.DARK` if it has a dark background."""
    colorfgbg = os.environ.get('COLORFGBG', '')
    try:
        fg, bg = map(int, colorfgbg.split(';', 1))
    except ValueError:
        return BGColor.UNKNOWN
    if bg > fg:
        return BGColor.LIGHT
    if fg > bg:
        return BGColor.DARK
    return BGColor.UNKNOWN


PYGMENTS_STYLE_MAP = {BGColor.LIGHT: MonokaiLightStyle,
                      BGColor.DARK: MonokaiStyle,
                      BGColor.UNKNOWN: FriendlyStyle}
PYGMENTS_STYLE = PYGMENTS_STYLE_MAP[get_bg_color()]

term_width = prettyprinter.utils.get_terminal_width()
prettyprinter.set_default_config(width=term_width - 1,
                                 ribbon_width=term_width - 9)
prettyprinter.set_default_style(PYGMENTS_STYLE)


def sgr(*args):
    """Creates a Select Graphic Rendition escape sequence. See
    https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters.
    """
    return '\x1b[{}m'.format(';'.join(map(str, args)))


def setup(config):
    resp = requests.get('https://discovery.meethue.com')
    print('Detected Philips Hue Bridges:')
    prettyprinter.cpprint(resp.json())
    session = PromptSession()
    location = session.prompt('Enter the Bridge IP address: ')
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
    my_globals = {'bridge': bridge,
                  'mired': mired,
                  'rgb_to_xybri': rgb_to_xybri}
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

    print(f'Connecting to {bridge_location}...')
    try:
        bridge = qhue.Bridge(bridge_location, bridge_username)
        num_lights = len(bridge.lights())
        print(f'Connected to {bridge_location}. {num_lights} lights found.')
    except requests.ConnectionError as err:
        print(f'{sgr(1, 31)}{err.__class__.__name__}{sgr(0)}: {err}')
        sys.exit(1)

    session = PromptSession('> ',
                            lexer=PygmentsLexer(Python3Lexer),
                            style=style_from_pygments_cls(PYGMENTS_STYLE),
                            auto_suggest=AutoSuggestFromHistory(),
                            input_processors=[HighlightMatchingBracketProcessor('()[]{}')],
                            history=FileHistory(Path.home() / '.philipshue.hist'))
    while True:
        try:
            cmd = session.prompt()
            start = time.perf_counter()
            out = exec_cmd(cmd, bridge=bridge)
            time_taken = time.perf_counter() - start
            prettyprinter.cpprint(out)
            print(f'Time taken: {sgr(1, 34)}{time_taken*1000:.3f} ms{sgr(0)}')
        except KeyboardInterrupt:
            pass
        except EOFError:
            break
        except requests.ConnectionError as err:
            print(f'{sgr(1, 31)}{err.__class__.__name__}{sgr(0)}: {err}')
            sys.exit(1)
        except Exception as err:
            print(f'{sgr(1, 31)}{err.__class__.__name__}{sgr(0)}: {err}')
