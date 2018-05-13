# -*- coding: utf-8 -*-
"""
    pygments.styles.friendly
    ~~~~~~~~~~~~~~~~~~~~~~~~

    A modern style based on the VIM pyte theme.

    :copyright: Copyright 2006-2017 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace


class FriendlyStyle(Style):
    """
    A modern style based on the VIM pyte theme.
    """

    background_color = "#f0f0f0"
    default_style = ""

    styles = {
        Whitespace:                "#bbbbbb",
        Comment:                   "italic #3da5bc",
        Comment.Preproc:           "noitalic #008200",
        Comment.Special:           "noitalic bg:#ffeded",

        Keyword:                   "bold #008200",
        Keyword.Pseudo:            "nobold",
        Keyword.Type:              "nobold #b40000",

        Operator:                  "#666666",
        Operator.Word:             "bold #008200",

        Name.Builtin:              "#008200",
        Name.Function:             "#0800b2",
        Name.Class:                "bold #0090d7",
        Name.Namespace:            "bold #0090d7",
        Name.Exception:            "#008200",
        Name.Variable:             "#ce3ff7",
        Name.Constant:             "#28b1eb",
        Name.Label:                "bold #0800a1",
        Name.Entity:               "bold #e63f1b",
        Name.Attribute:            "#1d71b8",
        Name.Tag:                  "bold #0009a0",
        Name.Decorator:            "bold #555555",

        String:                    "#1d71b8",
        String.Doc:                "italic",
        String.Interpol:           "italic #59a2e8",
        String.Escape:             "bold #1d71b8",
        String.Regex:              "#0056a7",
        String.Symbol:             "#4b8a00",
        String.Other:              "#e95d00",
        Number:                    "#00a968",

        Generic.Heading:           "bold #0000c0",
        Generic.Subheading:        "bold #ab00ac",
        Generic.Deleted:           "#db0000",
        Generic.Inserted:          "#00c300",
        Generic.Error:             "#ff0000",
        Generic.Emph:              "italic",
        Generic.Strong:            "bold",
        Generic.Prompt:            "bold #e95d00",
        Generic.Output:            "#888888",
        Generic.Traceback:         "#0000ff",

        Error:                     "border:#ff0000"
    }

