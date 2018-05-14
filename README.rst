philips-hue
===========

A CLI tool to interface with Philips Hue lights. It is an interactive interface to Quentin Stafford-Fraser's excellent minimal API `QHue <https://github.com/quentinsf/qhue>`_.

Usage
-----

Installation:

.. code:: bash

  python3 setup.py install

This will install a script under the name ``philipshue``. On first run, philips-hue will attempt to register a username with your Bridge. It will then write the bridge IP and its username to a configuration file ``$HOME/.philipshue.ini``.

philips-hue is basically an `IPython <https://ipython.org>`_-inspired read-eval-print loop. It turns commands entered on the prompt into QHue calls by (a) prepending ``bridge.`` to every command, and (b) calling the result if it is callable. Consequently most of the examples in the QHue README are applicable to philips-hue.

Examples:

- Entering ``lights`` at the prompt returns information on all of the lights. Entering ``lights[1]`` returns information on the first light only.

- ``lights[1].state(ct=200)`` sets the first light to a color temperature of 5000K (200 `mireds <https://en.wikipedia.org/wiki/Mired>`_).

- ``groups[0].action(bri=100, hue=10000, transitiontime=10)`` sets all the lights to a brightness of 100 and a hue of 10000. The lights fade to these values over a period of one second.

- ``bridge`` returns the entire bridge datastore.
