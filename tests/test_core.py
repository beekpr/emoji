# -*- coding: UTF-8 -*-


"""
Unittests for emoji.core
"""


from __future__ import unicode_literals

import emoji
from nose.tools import assert_raises


def test_emojize_name_only():
    for name in emoji.EMOJI_UNICODE.keys():
        actual = emoji.emojize(name, False)
        expected = emoji.EMOJI_UNICODE[name]
        assert expected == actual, "%s != %s" % (expected, actual)


def test_emojize_complicated_string():
    # A bunch of emoji's with UTF-8 strings to make sure the regex expression is functioning
    name_code = {
        ':flag_for_Ceuta_&_Melilla:': u'\U0001F1EA \U0001F1E6',
        ':flag_for_St._Barthélemy:': u'\U0001F1E7 \U0001F1F1',
        ':flag_for_Côte_d’Ivoire:': u'\U0001F1E8 \U0001F1EE',
        ':flag_for_Åland_Islands:': u'\U0001F1E6 \U0001F1FD',
        ':flag_for_São_Tomé_&_Príncipe:': u'\U0001F1F8 \U0001F1F9',
        ':flag_for_Curaçao:': u'\U0001F1E8 \U0001F1FC'
    }
    string = ' complicated! '.join(list(name_code.keys()))
    actual = emoji.emojize(string, False)
    expected = string
    for name, code in name_code.items():
        expected = expected.replace(name, code)
    expected = emoji.emojize(actual, False)
    assert expected == actual, "%s != %s" % (expected, actual)


def test_emojize_invalid_emoji():
    string = '__---___--Invalid__--__-Name'
    assert emoji.emojize(string, False) == string


def test_alias():
    # When use_aliases=False aliases should be passed through untouched
    assert emoji.emojize(':camel:', use_aliases=False) == ':camel:'
    assert emoji.emojize(':camel:', use_aliases=True) == emoji.EMOJI_ALIAS_UNICODE[':camel:']

def test_invalid_alias():
    # Invalid aliases should be passed through untouched
    assert emoji.emojize(':tester:', use_aliases=True) == ':tester:'

def test_smile_emoji():
    txt = u'(<some text> :smile:)'
    assert emoji.emojize(emoji.demojize(emoji.emojize(txt, use_aliases=True), use_shortcuts=True)) == emoji.emojize(txt, use_aliases=True)

def test_smile_emoji2():
    txt = u'(test asdad :smile:)'
    assert emoji.demojize(txt, use_shortcuts=True) == u'(test asdad :smile:)'

def test_demojize_name_only():
    for name in emoji.EMOJI_UNICODE.keys():
        oneway = emoji.emojize(name, False)
        roundtrip = emoji.demojize(oneway)
        assert name == roundtrip, "%s != %s" % (name, roundtrip)

def test_shortcut_translation():
    for shortcut in emoji.shortcuts.SHORTCUTS.keys():
        actual = emoji.demojize(shortcut, use_shortcuts=True)
        assert actual!=shortcut
        expected = emoji.shortcuts.SHORTCUTS[shortcut]
        assert expected == actual, "%s != %s" % (expected, actual)

def test_shortcuts():
    assert emoji.demojize(u'\U0001F376 :S :S :S', no_space=True, use_shortcuts=True) == u':sake_bottle_and_cup: :confounded: :confounded: :confounded:'


def test_demojize_name_only_no_space():
    for name in emoji.EMOJI_UNICODE.keys():
        oneway = emoji.emojize(name, False, True)
        roundtrip = emoji.demojize(oneway, True)
        assert name == roundtrip, "%s != %s" % (name, roundtrip)

def test_demojize_complicated_string():
    constructed = u"testing :baby::emoji_modifier_fitzpatrick_type-3: with :eyes: :eyes::eyes: modifiers :baby::emoji_modifier_fitzpatrick_type-5: to symbols ヒㇿ"
    emojid = emoji.emojize(constructed)
    destructed = emoji.demojize(emojid)
    assert constructed == destructed, "%s != %s" % (constructed, destructed)

def test_demojize_complicated_string_nospace():
    constructed = u"testing :baby::emoji_modifier_fitzpatrick_type-3: with :eyes: :eyes::eyes: modifiers :baby::emoji_modifier_fitzpatrick_type-5: to symbols ヒㇿ"
    emojid = emoji.emojize(constructed, no_space=True)
    destructed = emoji.demojize(emojid, no_space=True)
    assert constructed == destructed, "%s != %s" % (constructed, destructed)