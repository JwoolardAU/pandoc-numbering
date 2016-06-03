# This Python file uses the following encoding: utf-8

from unittest import TestCase
from pandocfilters import Para, Str, Space, Span, Strong, RawInline, Emph, Header

import json

import pandoc_numbering

from helper import init, createMetaList, createMetaMap, createMetaInlines, createListStr, createMetaString, createMetaBool

def getMeta1():
    return {
        'pandoc-numbering': createMetaList([
            createMetaMap({
                'category': createMetaInlines('exercise'),
                'sectioning': createMetaInlines('-.+.')
            })
        ])
    }

def getMeta2():
    return {
        'pandoc-numbering': createMetaList([
            createMetaMap({
                'category': createMetaInlines('exercise'),
                'first': createMetaString('2'),
                'last': createMetaString('2'),
            })
        ])
    }

def getMeta3():
    return {
        'pandoc-numbering': createMetaList([
            createMetaMap({
                'category': createMetaInlines('exercise'),
                'first': createMetaString('a'),
                'last': createMetaString('b'),
            })
        ])
    }

def getMeta4():
    return {
        'pandoc-numbering': createMetaList([
            createMetaMap({
                'category': createMetaInlines('exercise'),
                'classes': createMetaList([createMetaInlines('my-class')])
            })
        ])
    }

def getMeta5():
    return {
        'pandoc-numbering': createMetaList([
            createMetaMap({
                'category': createMetaInlines('exercise'),
                'format': createMetaBool(False)
            })
        ])
    }

def test_numbering():
    init()

    src = Para(createListStr('Exercise #'))
    dest = Para([
        Span(
            [u'exercise:1', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

def test_numbering_prefix_single():
    init()

    src = Para(createListStr('Exercise #ex:'))
    dest = Para([
        Span(
            [u'ex:1', ['pandoc-numbering-text', 'ex'], []],
            [Strong(createListStr('Exercise 1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

    src = Para(createListStr('Exercise #'))
    dest = Para([
        Span(
            [u'exercise:1', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

def test_numbering_latex():
    init()

    src = Para(createListStr('Exercise #'))
    dest = Para([
        RawInline(u'tex', u'\\phantomsection\\addcontentsline{exercise}{exercise}{\\protect\\numberline {1}{\\ignorespaces Exercise}}'),
        Span(
            [u'exercise:1', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], 'latex', {}) == dest

    init()

    src = Para(createListStr('Exercise (The title) #'))
    dest = Para([
        RawInline(u'tex', u'\\phantomsection\\addcontentsline{exercise}{exercise}{\\protect\\numberline {1}{\\ignorespaces The title}}'),
        Span(
            [u'exercise:1', ['pandoc-numbering-text', 'exercise'], []],
            [
                Strong(createListStr('Exercise 1')),
                Space(),
                Emph(createListStr('(') + createListStr('The title') + createListStr(')'))
            ]
       )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], 'latex', {}) == dest

def test_numbering_double():
    init()

    src = Para(createListStr('Exercise #'))
    pandoc_numbering.numbering(src['t'], src['c'], '', {})

    src = Para(createListStr('Exercise #'))
    dest = Para([
        Span(
            [u'exercise:2', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 2'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

def test_numbering_title():
    init()

    src = Para(createListStr('Exercise (The title) #'))
    dest = Para([
        Span(
            [u'exercise:1', ['pandoc-numbering-text', 'exercise'], []],
            [
                Strong(createListStr('Exercise 1')),
                Space(),
                Emph(createListStr('(') + createListStr('The title') + createListStr(')'))
            ]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

def test_numbering_level():
    init()

    src = Para(createListStr('Exercise +.+.#'))
    dest = Para([
        Span(
            [u'exercise:0.0.1', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 0.0.1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

    src = Header(1, [u'first-chapter', [], []], createListStr('First chapter'))
    pandoc_numbering.numbering(src['t'], src['c'], '', {})

    src = Header(2, [u'first-section', [], []], createListStr('First section'))
    pandoc_numbering.numbering(src['t'], src['c'], '', {})

    src = Para(createListStr('Exercise +.+.#'))
    dest = Para([
        Span(
            [u'exercise:1.1.1', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 1.1.1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

    src = Para(createListStr('Exercise +.+.#'))
    dest = Para([
        Span(
            [u'exercise:1.1.2', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 1.1.2'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

    src = Header(2, [u'second-section', [], []], createListStr('Second section'))
    pandoc_numbering.numbering(src['t'], src['c'], '', {})

    src = Para(createListStr('Exercise +.+.#'))
    dest = Para([
        Span(
            [u'exercise:1.2.1', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 1.2.1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

def test_numbering_unnumbered():
    init()

    src = Header(1, [u'unnumbered-chapter', [u'unnumbered'], []], createListStr('Unnumbered chapter'))
    pandoc_numbering.numbering(src['t'], src['c'], '', {})

    src = Para(createListStr('Exercise +.#'))
    dest = Para([
        Span(
            [u'exercise:0.1', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 0.1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

def test_numbering_hidden():
    init()

    src = Header(1, [u'first-chapter', [], []], createListStr('First chapter'))
    pandoc_numbering.numbering(src['t'], src['c'], '', {})

    src = Para(createListStr('Exercise -.#exercise:one'))
    dest = Para([
        Span(
            [u'exercise:one', ['pandoc-numbering-text', 'exercise'], []],
            [
                Strong(createListStr('Exercise 1'))
            ]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

    src = Para(createListStr('Exercise -.#'))
    dest = Para([
        Span(
            [u'exercise:1.2', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 2'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

    src = Header(1, [u'second-chapter', [], []], createListStr('Second chapter'))
    pandoc_numbering.numbering(src['t'], src['c'], '', {})

    src = Para(createListStr('Exercise -.#'))
    dest = Para([
        Span(
            [u'exercise:2.1', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

    src = Para(createListStr('Exercise +.#'))
    dest = Para([
        Span(
            [u'exercise:2.2', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 2.2'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

    src = Para([Str(u'Exercise'), Space(), Str(u'#')])
    dest = Para([
        Span(
            [u'exercise:1', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', {}) == dest

def test_numbering_sharp_sharp():
    init()

    src = Para(createListStr('Exercise ##'))
    dest = Para(createListStr('Exercise #'))
    pandoc_numbering.numbering(src['t'], src['c'], '', {})

    assert src == dest

def sectioning(meta):
    src = Header(1, [u'first-chapter', [], []], createListStr('First chapter'))
    pandoc_numbering.numbering(src['t'], src['c'], '', meta)

    src = Header(1, [u'second-chapter', [], []], createListStr('Second chapter'))
    pandoc_numbering.numbering(src['t'], src['c'], '', meta)

    src = Header(2, [u'first-section', [], []], createListStr('First section'))
    pandoc_numbering.numbering(src['t'], src['c'], '', meta)

    src = Header(2, [u'second-section', [], []], createListStr('Second section'))
    pandoc_numbering.numbering(src['t'], src['c'], '', meta)

def test_numbering_sectioning_string():
    init()

    meta = getMeta1()

    sectioning(meta)

    src = Para(createListStr('Exercise #'))
    dest = Para([
        Span(
            [u'exercise:2.2.1', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 2.1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', meta) == dest

def test_numbering_sectioning_map():
    init()

    meta = getMeta2()

    sectioning(meta)

    src = Para([Str(u'Exercise'), Space(), Str(u'#')])
    dest = Para([
        Span(
            [u'exercise:2.2.1', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 2.1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', meta) == dest

def test_numbering_sectioning_map_error():
    init()

    meta = getMeta3()

    sectioning(meta)

    src = Para(createListStr('Exercise #'))
    dest = Para([
        Span(
            [u'exercise:1', ['pandoc-numbering-text', 'exercise'], []],
            [Strong(createListStr('Exercise 1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', meta) == dest

def test_classes():
    init()

    meta = getMeta4()

    src = Para(createListStr('Exercise #'))
    dest = Para([
        Span(
            [u'exercise:1', ['pandoc-numbering-text', 'my-class'], []],
            [Strong(createListStr('Exercise 1'))]
        )
    ])

    assert pandoc_numbering.numbering(src['t'], src['c'], '', meta) == dest

def test_format():
    init()

    meta = getMeta5()

    src = Para(createListStr('Exercise #'))
    dest = json.loads(json.dumps(Para([
        Span(
            [u'exercise:1', ['pandoc-numbering-text', 'exercice'], []],
            [
                Span(['', ['description'], []], createListStr('Exercise')),
                Span(['', ['number'], []], createListStr('1')),
                Span(['', ['title'], []], [])
            ]
        )
    ])))

    json.loads(json.dumps(pandoc_numbering.numbering(src['t'], src['c'], '', meta))) == dest

