"""
Character encodings supported by GMT.

Currently, Adobe Symbol, Adobe ZapfDingbats, Adobe ISOLatin1+ and ISO-8859-x (x can be
1-11, 13-16) encodings are supported. Adobe Standard encoding is not supported.

The corresponding Unicode characters in each Adobe character encoding are generated from
the mapping tables and conversion scripts in the
`GMT-octal-codes repository <https://github.com/seisman/GMT-octal-codes>`__. Refer to
that repository for details.

Some code points are undefined and are assigned with the replacement character
(``\ufffd``).

References
----------

- GMT-octal-codes: https://github.com/seisman/GMT-octal-codes
- GMT documentation: https://docs.generic-mapping-tools.org/dev/reference/octal-codes.html
- Adobe Postscript Language Reference: https://www.adobe.com/jp/print/postscript/pdfs/PLRM.pdf
- Adobe ISOLatin1+: https://en.wikipedia.org/wiki/PostScript_Latin_1_Encoding
- Adobe Symbol: https://en.wikipedia.org/wiki/Symbol_(typeface)
- Adobe ZapfDingbats: https://en.wikipedia.org/wiki/Zapf_Dingbats
- Adobe Glyph List: https://github.com/adobe-type-tools/agl-aglfn
- ISO-8859: https://en.wikipedia.org/wiki/ISO/IEC_8859
"""

import codecs

# Dictionary of character mappings for different encodings.
charset: dict = {}

# Adobe ISOLatin1+ charset.
charset["ISOLatin1+"] = dict(
    zip(
        range(0o030, 0o400),
        "\ufffd\u2022\u2026\u2122\u2014\u2013\ufb01\u017e"
        "\u0020\u0021\u0022\u0023\u0024\u0025\u0026\u2019"
        "\u0028\u0029\u002a\u002b\u002c\u2212\u002e\u002f"
        "\u0030\u0031\u0032\u0033\u0034\u0035\u0036\u0037"
        "\u0038\u0039\u003a\u003b\u003c\u003d\u003e\u003f"
        "\u0040\u0041\u0042\u0043\u0044\u0045\u0046\u0047"
        "\u0048\u0049\u004a\u004b\u004c\u004d\u004e\u004f"
        "\u0050\u0051\u0052\u0053\u0054\u0055\u0056\u0057"
        "\u0058\u0059\u005a\u005b\u005c\u005d\u005e\u005f"
        "\u2018\u0061\u0062\u0063\u0064\u0065\u0066\u0067"
        "\u0068\u0069\u006a\u006b\u006c\u006d\u006e\u006f"
        "\u0070\u0071\u0072\u0073\u0074\u0075\u0076\u0077"
        "\u0078\u0079\u007a\u007b\u007c\u007d\u007e\u0161"
        "\u0152\u2020\u2021\u0141\u2044\u2039\u0160\u203a"
        "\u0153\u0178\u017d\u0142\u2030\u201e\u201c\u201d"
        "\u0131\u0060\u00b4\u02c6\u02dc\u00af\u02d8\u02d9"
        "\u00a8\u201a\u02da\u00b8\u0027\u02dd\u02db\u02c7"
        "\u0020\u00a1\u00a2\u00a3\u00a4\u00a5\u00a6\u00a7"
        "\u00a8\u00a9\u00aa\u00ab\u00ac\u002d\u00ae\u00af"
        "\u00b0\u00b1\u00b2\u00b3\u00b4\u00b5\u00b6\u00b7"
        "\u00b8\u00b9\u00ba\u00bb\u00bc\u00bd\u00be\u00bf"
        "\u00c0\u00c1\u00c2\u00c3\u00c4\u00c5\u00c6\u00c7"
        "\u00c8\u00c9\u00ca\u00cb\u00cc\u00cd\u00ce\u00cf"
        "\u00d0\u00d1\u00d2\u00d3\u00d4\u00d5\u00d6\u00d7"
        "\u00d8\u00d9\u00da\u00db\u00dc\u00dd\u00de\u00df"
        "\u00e0\u00e1\u00e2\u00e3\u00e4\u00e5\u00e6\u00e7"
        "\u00e8\u00e9\u00ea\u00eb\u00ec\u00ed\u00ee\u00ef"
        "\u00f0\u00f1\u00f2\u00f3\u00f4\u00f5\u00f6\u00f7"
        "\u00f8\u00f9\u00fa\u00fb\u00fc\u00fd\u00fe\u00ff",
        strict=False,
    )
)

# Adobe Symbol charset.
charset["Symbol"] = dict(
    zip(
        [*range(0o040, 0o200), *range(0o240, 0o400)],
        "\u0020\u0021\u2200\u0023\u2203\u0025\u0026\u220b"
        "\u0028\u0029\u2217\u002b\u002c\u2212\u002e\u002f"
        "\u0030\u0031\u0032\u0033\u0034\u0035\u0036\u0037"
        "\u0038\u0039\u003a\u003b\u003c\u003d\u003e\u003f"
        "\u2245\u0391\u0392\u03a7\u2206\u0395\u03a6\u0393"
        "\u0397\u0399\u03d1\u039a\u039b\u039c\u039d\u039f"
        "\u03a0\u0398\u03a1\u03a3\u03a4\u03a5\u03c2\u2126"
        "\u039e\u03a8\u0396\u005b\u2234\u005d\u22a5\u005f"
        "\uf8e5\u03b1\u03b2\u03c7\u03b4\u03b5\u03c6\u03b3"
        "\u03b7\u03b9\u03d5\u03ba\u03bb\u03bc\u03bd\u03bf"
        "\u03c0\u03b8\u03c1\u03c3\u03c4\u03c5\u03d6\u03c9"
        "\u03be\u03c8\u03b6\u007b\u007c\u007d\u223c\ufffd"
        "\u20ac\u03d2\u2032\u2264\u2215\u221e\u0192\u2663"
        "\u2666\u2665\u2660\u2194\u2190\u2191\u2192\u2193"
        "\u00b0\u00b1\u2033\u2265\u00d7\u221d\u2202\u2022"
        "\u00f7\u2260\u2261\u2248\u2026\u23d0\u23af\u21b5"
        "\u2135\u2111\u211c\u2118\u2297\u2295\u2205\u2229"
        "\u222a\u2283\u2287\u2284\u2282\u2286\u2208\u2209"
        "\u2220\u2207\u00ae\u00a9\u2122\u220f\u221a\u22c5"
        "\u00ac\u2227\u2228\u21d4\u21d0\u21d1\u21d2\u21d3"
        "\u25ca\u2329\u00ae\u00a9\u2122\u2211\u239b\u239c"
        "\u239d\u23a1\u23a2\u23a3\u23a7\u23a8\u23a9\u23aa"
        "\ufffd\u232a\u222b\u2320\u23ae\u2321\u239e\u239f"
        "\u23a0\u23a4\u23a5\u23a6\u23ab\u23ac\u23ad\ufffd",
        strict=False,
    )
)

# Adobe ZapfDingbats charset.
charset["ZapfDingbats"] = dict(
    zip(
        [*range(0o040, 0o220), *range(0o240, 0o400)],
        "\u0020\u2701\u2702\u2703\u2704\u260e\u2706\u2707"
        "\u2708\u2709\u261b\u261e\u270c\u270d\u270e\u270f"
        "\u2710\u2711\u2712\u2713\u2714\u2715\u2716\u2717"
        "\u2718\u2719\u271a\u271b\u271c\u271d\u271e\u271f"
        "\u2720\u2721\u2722\u2723\u2724\u2725\u2726\u2727"
        "\u2605\u2729\u272a\u272b\u272c\u272d\u272e\u272f"
        "\u2730\u2731\u2732\u2733\u2734\u2735\u2736\u2737"
        "\u2738\u2739\u273a\u273b\u273c\u273d\u273e\u273f"
        "\u2740\u2741\u2742\u2743\u2744\u2745\u2746\u2747"
        "\u2748\u2749\u274a\u274b\u25cf\u274d\u25a0\u274f"
        "\u2750\u2751\u2752\u25b2\u25bc\u25c6\u2756\u25d7"
        "\u2758\u2759\u275a\u275b\u275c\u275d\u275e\ufffd"
        "\u2768\u2769\u276a\u276b\u276c\u276d\u276e\u276f"
        "\u2770\u2771\u2772\u2773\u2774\u2775\ufffd\ufffd"
        "\ufffd\u2761\u2762\u2763\u2764\u2765\u2766\u2767"
        "\u2663\u2666\u2665\u2660\u2460\u2461\u2462\u2463"
        "\u2464\u2465\u2466\u2467\u2468\u2469\u2776\u2777"
        "\u2778\u2779\u277a\u277b\u277c\u277d\u277e\u277f"
        "\u2780\u2781\u2782\u2783\u2784\u2785\u2786\u2787"
        "\u2788\u2789\u278a\u278b\u278c\u278d\u278e\u278f"
        "\u2790\u2791\u2792\u2793\u2794\u2192\u2194\u2195"
        "\u2798\u2799\u279a\u279b\u279c\u279d\u279e\u279f"
        "\u27a0\u27a1\u27a2\u27a3\u27a4\u27a5\u27a6\u27a7"
        "\u27a8\u27a9\u27aa\u27ab\u27ac\u27ad\u27ae\u27af"
        "\ufffd\u27b1\u27b2\u27b3\u27b4\u27b5\u27b6\u27b7"
        "\u27b8\u27b9\u27ba\u27bb\u27bc\u27bd\u27be\ufffd",
        strict=False,
    )
)

# ISO-8859-x charsets and x can be 1-11, 13-16.
for i in range(1, 17):
    if i == 12:  # ISO-8859-12 was abandoned.
        continue
    charset[f"ISO-8859-{i}"] = {
        code: codecs.decode(bytes([code]), f"iso8859_{i}", errors="replace")
        for code in [*range(0o040, 0o200), *range(0o240, 0o400)]
    }
