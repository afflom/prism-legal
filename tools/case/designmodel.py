"""WCAG 2.2 AA design system for PrismLegal Public-Benefit Legal Platform, expressed as LexLean declarations
in `src/Presentation.lex.tex` and verified in integer arithmetic by the Lean 4 kernel."""

from .semantic import (
    BOOL,
    NAT,
    STR,
    add,
    all_members,
    b,
    beq,
    ble,
    blt,
    call,
    definition,
    distinct_strings,
    eq_string,
    field_of_each,
    holds,
    if_,
    list_t,
    lookup_field,
    lst,
    match_list,
    n,
    named,
    proj,
    record,
    s,
    structure,
    var,
)

SCALE = 10_000_000_000
HALF = 500_000_000  # 0.05 in units of 10^10


def srgb_channel(c):
    """Linearised sRGB channel scaled by 10^6 (IEC 61966-2-1, WCAG 2.2 relative luminance)."""
    v = c / 255.0
    lin = v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return round(lin * 1_000_000)


SRGB_TABLE = [srgb_channel(c) for c in range(256)]


def parse_hex(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def luminance(hex_color):
    r, g, b_ch = parse_hex(hex_color)
    return 2126 * SRGB_TABLE[r] + 7152 * SRGB_TABLE[g] + 722 * SRGB_TABLE[b_ch]


def contrast_tenths(a, c):
    la, lc = luminance(a), luminance(c)
    hi, lo = (la, lc) if la >= lc else (lc, la)
    return (10 * (hi + HALF)) // (lo + HALF)


PALETTE = [
    ("bg", "#f8fafc", "#0b1120", "Page canvas background"),
    ("surface", "#ffffff", "#111827", "Card and header surface"),
    ("surface-alt", "#f1f5f9", "#1e293b", "Secondary control and table header surface"),
    ("ink", "#0f172a", "#f1f5f9", "Primary body and testimony text"),
    ("muted", "#334155", "#cbd5e1", "Secondary labels and metadata"),
    ("accent", "#1e3a8a", "#93c5fd", "Primary courtroom links and active controls"),
    ("stipulated", "#14532d", "#86efac", "Stipulated facts and Opening-aligned pivots"),
    ("warning", "#7c2d12", "#fdba74", "Contested claims and FRCP 26(e) & Rule 16.2 warnings"),
    ("danger", "#7f1d1d", "#fca5a5", "Cross-examination trap warnings"),
    ("border", "#475569", "#64748b", "Interactive control and focus boundary"),
]

PAIRS = [
    ("ink", "bg", "text", "Primary text on page canvas"),
    ("ink", "surface", "text", "Primary text on card surface"),
    ("ink", "surface-alt", "text", "Primary text on secondary surface"),
    ("muted", "bg", "text", "Secondary text on page canvas"),
    ("muted", "surface", "text", "Secondary text on card surface"),
    ("accent", "bg", "text", "Courtroom link on page canvas"),
    ("accent", "surface", "text", "Courtroom link on card surface"),
    ("stipulated", "bg", "text", "Stipulated badge ink on page canvas"),
    ("stipulated", "surface", "text", "Stipulated badge ink on card surface"),
    ("warning", "bg", "text", "Warning ink on page canvas"),
    ("warning", "surface", "text", "Warning ink on card surface"),
    ("danger", "bg", "text", "Trap warning ink on page canvas"),
    ("danger", "surface", "text", "Trap warning ink on card surface"),
    ("border", "bg", "ui", "Control border on page canvas"),
    ("border", "surface", "ui", "Control border on card surface"),
]

MINIMUM_TENTHS = {"text": 45, "ui": 30}

TYPE_SCALE = [
    {"id": "xs", "milliRem": 780, "lineHeightCenti": 140, "role": "Badges and exhibit pill codes"},
    {"id": "sm", "milliRem": 880, "lineHeightCenti": 145, "role": "Table metadata and secondary captions"},
    {"id": "base", "milliRem": 1000, "lineHeightCenti": 155, "role": "Body copy and witness examination points"},
    {"id": "lg", "milliRem": 1140, "lineHeightCenti": 145, "role": "Card headings and verbatim Opening quotes"},
    {"id": "xl", "milliRem": 1350, "lineHeightCenti": 130, "role": "Panel titles and KPI values"},
    {"id": "2xl", "milliRem": 1650, "lineHeightCenti": 120, "role": "Courtroom banner heading"},
]

SPACING = [
    {"id": "1", "px": 4},
    {"id": "2", "px": 8},
    {"id": "3", "px": 12},
    {"id": "4", "px": 16},
    {"id": "5", "px": 24},
    {"id": "6", "px": 32},
    {"id": "7", "px": 48},
]

MOTION = {"durationMs": 150, "reducedDurationMs": 0, "focusRingPx": 3, "minTargetPx": 24}


def tokens():
    rows = []
    for name, light_hex, dark_hex, purpose in PALETTE:
        for theme, hx in (("light", light_hex), ("dark", dark_hex)):
            r, g, b_ch = parse_hex(hx)
            rows.append(
                {
                    "id": name,
                    "theme": theme,
                    "hex": hx,
                    "r": r,
                    "g": g,
                    "b": b_ch,
                    "luminance": luminance(hx),
                    "purpose": purpose,
                }
            )
    return rows


def contrast_pairs():
    return [
        {
            "foreground": fg,
            "background": bg,
            "kind": kind,
            "minimumTenths": MINIMUM_TENTHS[kind],
            "purpose": purpose,
        }
        for fg, bg, kind, purpose in PAIRS
    ]


def declarations():
    tk_t = named("Token")
    cp_t = named("ContrastPair")
    ts_t = named("TypeStep")
    sp_t = named("SpaceStep")
    mo_t = named("Motion")
    mul = lambda a, c: {"kind": "primitive", "operation": "multiply", "result": NAT, "arguments": [a, c]}

    used_bytes = sorted({ch for _, l_hex, d_hex, _ in PALETTE for hx in (l_hex, d_hex) for ch in parse_hex(hx)})

    def srgb_body(idx=0):
        if idx >= len(used_bytes):
            return n(0)
        b_val = used_bytes[idx]
        return if_(beq(var("c"), n(b_val)), n(SRGB_TABLE[b_val]), srgb_body(idx + 1))

    tk_rows = tokens()
    cp_rows = contrast_pairs()
    ts = var("ts")
    fg_lum = call("tokenLuminance", proj(var("head"), "foreground"), var("theme"), ts)
    bg_lum = call("tokenLuminance", proj(var("head"), "background"), var("theme"), ts)

    return [
        structure(
            "Token",
            [
                ("id", STR),
                ("theme", STR),
                ("hex", STR),
                ("r", NAT),
                ("g", NAT),
                ("b", NAT),
                ("luminance", NAT),
                ("purpose", STR),
            ],
        ),
        structure(
            "ContrastPair",
            [
                ("foreground", STR),
                ("background", STR),
                ("kind", STR),
                ("minimumTenths", NAT),
                ("purpose", STR),
            ],
        ),
        structure("TypeStep", [("id", STR), ("milliRem", NAT), ("lineHeightCenti", NAT), ("role", STR)]),
        structure("SpaceStep", [("id", STR), ("px", NAT)]),
        structure("Motion", [("durationMs", NAT), ("reducedDurationMs", NAT), ("focusRingPx", NAT), ("minTargetPx", NAT)]),
        definition(
            "designTokens",
            list_t(tk_t),
            lst(
                [
                    record(
                        "Token",
                        id=s(t["id"]),
                        theme=s(t["theme"]),
                        hex=s(t["hex"]),
                        r=n(t["r"]),
                        g=n(t["g"]),
                        b=n(t["b"]),
                        luminance=n(t["luminance"]),
                        purpose=s(t["purpose"]),
                    )
                    for t in tk_rows
                ],
                tk_t,
            ),
        ),
        definition(
            "contrastPairs",
            list_t(cp_t),
            lst(
                [
                    record(
                        "ContrastPair",
                        foreground=s(p["foreground"]),
                        background=s(p["background"]),
                        kind=s(p["kind"]),
                        minimumTenths=n(p["minimumTenths"]),
                        purpose=s(p["purpose"]),
                    )
                    for p in cp_rows
                ],
                cp_t,
            ),
        ),
        definition(
            "typeScale",
            list_t(ts_t),
            lst(
                [
                    record(
                        "TypeStep",
                        id=s(x["id"]),
                        milliRem=n(x["milliRem"]),
                        lineHeightCenti=n(x["lineHeightCenti"]),
                        role=s(x["role"]),
                    )
                    for x in TYPE_SCALE
                ],
                ts_t,
            ),
        ),
        definition(
            "spacingScale",
            list_t(sp_t),
            lst([record("SpaceStep", id=s(x["id"]), px=n(x["px"])) for x in SPACING], sp_t),
        ),
        definition(
            "motion",
            mo_t,
            record(
                "Motion",
                durationMs=n(MOTION["durationMs"]),
                reducedDurationMs=n(MOTION["reducedDurationMs"]),
                focusRingPx=n(MOTION["focusRingPx"]),
                minTargetPx=n(MOTION["minTargetPx"]),
            ),
        ),
        definition("srgbLinear", NAT, srgb_body(), parameters=[("c", NAT)]),
        definition(
            "relativeLuminance",
            NAT,
            add(
                add(mul(n(2126), call("srgbLinear", var("r"))), mul(n(7152), call("srgbLinear", var("g")))),
                mul(n(722), call("srgbLinear", var("b"))),
            ),
            parameters=[("r", NAT), ("g", NAT), ("b", NAT)],
        ),
        definition(
            "luminancesMatch",
            BOOL,
            match_list(
                var("xs"),
                b(True),
                "head",
                "tail",
                if_(
                    beq(
                        proj(var("head"), "luminance"),
                        call(
                            "relativeLuminance",
                            proj(var("head"), "r"),
                            proj(var("head"), "g"),
                            proj(var("head"), "b"),
                        ),
                    ),
                    call("luminancesMatch", var("tail")),
                    b(False),
                ),
            ),
            parameters=[("xs", list_t(tk_t))],
            recursive="xs",
        ),
        definition(
            "tokensOfTheme",
            list_t(tk_t),
            match_list(
                var("xs"),
                {"kind": "nil", "element": tk_t},
                "head",
                "tail",
                if_(
                    eq_string(var("theme"), proj(var("head"), "theme")),
                    {"kind": "cons", "head": var("head"), "tail": call("tokensOfTheme", var("theme"), var("tail"))},
                    call("tokensOfTheme", var("theme"), var("tail")),
                ),
            ),
            parameters=[("theme", STR), ("xs", list_t(tk_t))],
            recursive="xs",
        ),
        field_of_each("tokenIds", tk_t, "id"),
        field_of_each("pairForegrounds", cp_t, "foreground"),
        field_of_each("pairBackgrounds", cp_t, "background"),
        field_of_each("typeMilliRems", ts_t, "milliRem", result=NAT),
        field_of_each("spacePxs", sp_t, "px", result=NAT),
        lookup_field("typeMilliRem", ts_t, "id", "milliRem", NAT, n(0)),
        definition(
            "tokenLuminance",
            NAT,
            match_list(
                var("xs"),
                n(0),
                "head",
                "tail",
                if_(
                    eq_string(var("tokenId"), proj(var("head"), "id")),
                    if_(
                        eq_string(var("theme"), proj(var("head"), "theme")),
                        proj(var("head"), "luminance"),
                        call("tokenLuminance", var("tokenId"), var("theme"), var("tail")),
                    ),
                    call("tokenLuminance", var("tokenId"), var("theme"), var("tail")),
                ),
            ),
            parameters=[("tokenId", STR), ("theme", STR), ("xs", list_t(tk_t))],
            recursive="xs",
        ),
        definition(
            "meetsContrast",
            BOOL,
            if_(
                ble(var("lc"), var("la")),
                ble(mul(var("minimumTenths"), add(var("lc"), n(HALF))), mul(n(10), add(var("la"), n(HALF)))),
                ble(mul(var("minimumTenths"), add(var("la"), n(HALF))), mul(n(10), add(var("lc"), n(HALF)))),
            ),
            parameters=[("la", NAT), ("lc", NAT), ("minimumTenths", NAT)],
        ),
        definition(
            "pairsMeetContrast",
            BOOL,
            match_list(
                var("ps"),
                b(True),
                "head",
                "tail",
                if_(
                    call("meetsContrast", fg_lum, bg_lum, proj(var("head"), "minimumTenths")),
                    call("pairsMeetContrast", var("tail"), var("theme"), ts),
                    b(False),
                ),
            ),
            parameters=[("ps", list_t(cp_t)), ("theme", STR), ("ts", list_t(tk_t))],
            recursive="ps",
        ),
        definition(
            "strictlyIncreasing",
            BOOL,
            match_list(
                var("xs"),
                b(True),
                "head",
                "tail",
                if_(blt(var("previous"), var("head")), call("strictlyIncreasing", var("tail"), var("head")), b(False)),
            ),
            parameters=[("xs", list_t(NAT)), ("previous", NAT)],
            recursive="xs",
        ),
        holds(
            "lightTokenIdsDistinct",
            call("distinctStrings", call("tokenIds", call("tokensOfTheme", s("light"), call("designTokens")))),
        ),
        holds(
            "darkTokenIdsDistinct",
            call("distinctStrings", call("tokenIds", call("tokensOfTheme", s("dark"), call("designTokens")))),
        ),
        holds(
            "themesHaveSameTokens",
            call(
                "sameMembers",
                call("tokenIds", call("tokensOfTheme", s("light"), call("designTokens"))),
                call("tokenIds", call("tokensOfTheme", s("dark"), call("designTokens"))),
            ),
        ),
        holds(
            "pairsReferenceTokens",
            call(
                "allMembers",
                call("pairForegrounds", call("contrastPairs")),
                call("tokenIds", call("tokensOfTheme", s("light"), call("designTokens"))),
            ),
        ),
        holds(
            "pairBackgroundsReferenceTokens",
            call(
                "allMembers",
                call("pairBackgrounds", call("contrastPairs")),
                call("tokenIds", call("tokensOfTheme", s("light"), call("designTokens"))),
            ),
        ),
        holds("tokenLuminancesComputed", call("luminancesMatch", call("designTokens"))),
        holds(
            "everyPairMeetsContrastLight",
            call("pairsMeetContrast", call("contrastPairs"), s("light"), call("designTokens")),
        ),
        holds(
            "everyPairMeetsContrastDark",
            call("pairsMeetContrast", call("contrastPairs"), s("dark"), call("designTokens")),
        ),
        holds("typeScaleIncreasing", call("strictlyIncreasing", call("typeMilliRems", call("typeScale")), n(0))),
        holds("spacingIncreasing", call("strictlyIncreasing", call("spacePxs", call("spacingScale")), n(0))),
        holds("bodyTextAtLeastOneRem", ble(n(1000), call("typeMilliRem", s("base"), call("typeScale")))),
        holds("focusRingAtLeast2px", ble(n(2), proj(call("motion"), "focusRingPx"))),
        holds("targetSizeAtLeast24px", ble(n(24), proj(call("motion"), "minTargetPx"))),
        holds("reducedMotionZero", beq(proj(call("motion"), "reducedDurationMs"), n(0))),
    ]
