# -*- coding: UTF-8 -*-


"""
emoji.core
~~~~~~~~~~

Core components for emoji.

"""


import re
import sys

from . import unicode_codes
from . import shortcuts

PY2 = sys.version_info[0] is 2

_EMOJI_REGEXP = None
_EMOJI_REGEXP_NOSPACE = None
_EMOJI_SHORTCODE_REGEXP = None
_SHORTCUT_REGEXP = None

USE_ALIASES = False

NO_SPACE = False
USE_SHORTCUTS = False


def emojize(string, use_aliases=USE_ALIASES, no_space=NO_SPACE):

    """Replace emoji names in a string with unicode codes.

    :param string: String contains emoji names.
    :param use_aliases: (optional) Enable emoji aliases.  See ``emoji.UNICODE_EMOJI_ALIAS``.
    :param no_space: (optional) Remove space characters for multi-character emojis.

        >>> import emoji
        >>> print(emoji.emojize("Python is fun :thumbsup:", use_aliases=True))
        Python is fun 👍
        >>> print(emoji.emojize("Python is fun :thumbs_up_sign:"))
        Python is fun 👍
    """

    def replace(match):
        if use_aliases:
            val = unicode_codes.EMOJI_ALIAS_UNICODE.get(match.group(1), None)
        else:
            val = unicode_codes.EMOJI_UNICODE.get(match.group(1), None)
        if val:
            if no_space:
                return val.replace(u' ', u'')
            return val
        return match.group(1)

    return get_emoji_shortcode_regex().sub(replace, string)


def demojize(string, no_space=NO_SPACE, use_shortcuts=USE_SHORTCUTS, max_length=None):

    """Replace unicode emoji in a string with emoji shortcodes. Useful for storage.

    :param string: String contains unicode characters. MUST BE UNICODE.
    :param no_space: (optional) No space between characters in multi-character emojis.
    :param use_shortcuts: (optional) Replace shortcuts with emoji shortcodes.

        >>> import emoji
        >>> print(emoji.emojize("Python is fun :thumbs_up_sign:"))
        Python is fun 👍
        >>> print(emoji.demojize(u"Python is fun 👍"))
        Python is fun :thumbs_up_sign:
        >>> print(emoji.demojize("Unicode is tricky 😯".decode('utf-8')))
        Unicode is tricky :hushed_face:
    """

    if use_shortcuts:
        string = replace_shortcuts(string)

    UNICODE_EMOJI = unicode_codes.UNICODE_EMOJI_NO_SPACE if no_space else unicode_codes.UNICODE_EMOJI

    def replace(match):
        return UNICODE_EMOJI.get(match.group(0), match.group(0))

    # Decode shortcuts
    string = get_emoji_regexp(no_space).sub(replace, string)
    
    if max_length:
        safe_length = _get_safe_length(string, max_length)
        string = string[0:safe_length]

    return string


def replace_shortcuts(string):
    def replace(match):
        return shortcuts.SHORTCUTS.get(match.group(1), match.group(1))
    return get_shortcut_regexp().sub(replace, u' ' + string)[1:]


def _get_safe_length(text, max_length):
        previous = 0
        for m in get_emoji_shortcode_regex().finditer(text):
            if m.start() + len(m.group()) > max_length:
                return m.start() if "emoji_modifier_fitzpatrick" not in m.group() else previous
            previous = m.start()
        return max_length


def get_emoji_regexp(no_space=NO_SPACE):

    """Returns compiled regular expression that matches emojis defined in
    ``emoji.UNICODE_EMOJI_ALIAS``. The regular expression is only compiled once.
    """

    global _EMOJI_REGEXP
    global _EMOJI_REGEXP_NOSPACE
    # Build emoji regexp once
    if (_EMOJI_REGEXP_NOSPACE if no_space else _EMOJI_REGEXP) is None:
        # Sort emojis by length to make sure mulit-character emojis are
        # matched first
        if no_space:
            values = [v.replace(' ', '') for v in unicode_codes.EMOJI_UNICODE.values()]
        else:
            values = unicode_codes.EMOJI_UNICODE.values()
        emojis = sorted(values, key=len,
                        reverse=True)
        pattern = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'
        regexp = re.compile(pattern)
        if no_space:
            _EMOJI_REGEXP_NOSPACE = regexp
        else:
            _EMOJI_REGEXP = regexp
    return _EMOJI_REGEXP_NOSPACE if no_space else _EMOJI_REGEXP


def get_emoji_shortcode_regex():
    
    global _EMOJI_SHORTCODE_REGEXP
    if _EMOJI_SHORTCODE_REGEXP is None:
        pattern = u'(:[a-zA-Z0-9\+\-_&.ô’Åéãíç]+:)'
        _EMOJI_SHORTCODE_REGEXP = re.compile(pattern)
    return _EMOJI_SHORTCODE_REGEXP


def get_shortcut_regexp():

    """Returns compiled regular expression that matches shortcuts defined in
    ``shortcuts.SHORTCUTS``. The regular expression is only compiled once.
    """

    global _SHORTCUT_REGEXP
    # Build shortcut regexp once
    if _SHORTCUT_REGEXP is None:
        values = shortcuts.SHORTCUTS.keys()
        values = sorted(values, key=len, reverse=True)
        pattern = u'(?<=\s)(' + u'|'.join(re.escape(u) for u in values) + u')((?=(\s|\)|\.))|$)'
        _SHORTCUT_REGEXP = re.compile(pattern)
    return _SHORTCUT_REGEXP
