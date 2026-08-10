# steampunk-ui

A Claude Code skill that makes an AI agent design steampunk interfaces which look like
**working instruments** rather than Victorian cosplay.

There are a lot of good taste skills now. Almost all of them teach the same aesthetic:
neutral zinc, one desaturated accent, generous whitespace, spring physics. This one goes
somewhere else entirely, and it is opinionated about it.

> **Brass, not gold. Oxidation, not damage. It is an instrument, not a costume. No gear emoji.**

## The problem it solves twice

Ask a language model for a steampunk interface and you get **cosplay**: gear emoji,
blackletter headings, brass gradients on everything, riveted buttons, and a pressure gauge
with nothing behind it. It looks like a Halloween costume and it is unusable for real work.

So you write a restraint doctrine banning all of that, and you get the second failure,
which is **inertness**: a competent, legible, perfectly accessible brown page with no
light, no metal and no mechanism in it. Correct and dead.

The skill's central rule is the test that separates the two:

> **Does this ornament depict a mechanism that actually exists here? If yes, draw it.
> If it depicts a theme, delete it.**

Rivets down a panel edge depict a plate bolted to a frame, so draw them. Rivets on a button
depict nothing, so delete them. A cog that turns only while work is in flight is a state
indicator. A cog that turns forever is decoration. A needle bound to disk free space is a
readout; a dial that wobbles on a timer is a lie told in brass.

## What is in it

- **A palette that passes.** Every ink and signal token clears WCAG AA against all four
  surfaces, not merely against the page ground. That distinction matters: a token that
  passes on the ground and fails on a panel header is exactly where your labels live.
  `tools/contrast.py` checks it and exits non-zero, so it drops into CI.
- **A three-tier signal hierarchy.** Copper is data, brass is structure, polished brass is
  attention. No overlap, and no `--gold` token, because "brass, not gold" is meant literally.
- **Status colour from real oxidation.** Verdigris is copper carbonate, rust is iron oxide,
  ember is hot iron. They harmonise because they are what these metals actually do, rather
  than `#22c55e` and `#ef4444` imported from a framework.
- **Drawn metal.** The four-stop specular gradient that makes a nameplate read as brass
  rather than beige, CSS rivets, a lit top edge and a soft ambient sink instead of drop
  shadows, and lamp light falling across the page.
- **A real analogue gauge.** Bezel, lit face, ticks, composition arcs, a bone needle on a
  spindle, and the `transform-origin: 50% 94.3%` that stops it wobbling off its pivot.
- **Motion with mass.** Continuous values settle and never overshoot. Discrete events, like
  a verdict being stamped, are allowed to land with impact. Continuous animation must be
  bound to continuous state.
- **A diegetic vocabulary.** The section that actually produces "alive", and it costs
  nothing: intake, the hold, the ledger, pipes, stamps, levers. Every noun belongs to one
  imagined machine, error paths and empty states included.
- **The chrome nobody remembers.** Themed scrollbars, selection colour, accent-color,
  copyable code chips. A stock blue-grey scrollbar down the side of a brass panel undoes a
  great deal of careful work, and it is the most common leak in the whole aesthetic.
- **An honesty rule.** No instrument may display a value that is not real. No decorative
  gauges, no `Math.random()` in a chart, and absent data renders as `NO SIGNAL` rather than
  as zero or a healthy green dash. A missing reading that looks like a good reading is the
  worst bug this aesthetic can ship.

Four sanctioned variants (Foundry, Soot, Blueprint, Verdigris), a terminal and ratatui
annex, and copy-pasteable component CSS.

## Reference render

`example/index.html` is a complete instrument panel in the aesthetic, self-contained, with
no webfonts and no CDN. The palette switcher in its header cycles all four variants.

It obeys its own honesty rule, which is the point of it: the capacity gauge is bound to
`navigator.storage.estimate()`, a genuinely real figure from your browser. If the browser
declines to give one, the panel says `NO SIGNAL` and the needle holds its last position
rather than sweeping to zero, because a needle at zero is a reading. The cog turns only
while that reading is in flight. Nothing on the page is randomised.

## Install

```sh
git clone git@github.com:cargopete/steampunk-ui.git
cd steampunk-ui && ./install.sh
```

That symlinks the directory into `~/.claude/skills/steampunk-ui`, making it available in
every project on the machine. To scope it to one project instead, symlink or copy it into
that project's `.claude/skills/`.

Then ask for it by name, or just describe what you want. The description fires on
steampunk, brass, copper, patina, industrial-Victorian, oil-lamp, foundry and
salvaged-machinery.

## Layout

| Path | What it is |
|---|---|
| `SKILL.md` | The skill. Doctrine and the ornament test, bans, palette, typography, geometry, light and drawn metal, the analogue instrument, motion, naming the machine, components, the honesty rule, checklist. |
| `reference/tokens.css` | The canonical token set, commented, plus the three variant overrides. |
| `reference/components.md` | Working CSS and SVG: riveted plates, nameplate, gauge, readouts, pipes, stamps, levers, cog, ledger rows, empty states. |
| `reference/variants.md` | When to use each variant, how to derive a new one, and where the palette came from. |
| `reference/terminal.md` | ratatui `Theme` struct, the computed 256-colour fallback, alacritty config, CLI output rules. |
| `tools/contrast.py` | Palette validator. Every token against every surface, exits non-zero on failure. |
| `example/index.html` | The reference render. |

## Where the palette came from

Reconciled, not invented, from six steampunk interfaces built independently of each other:
an indexer dashboard in Rust and HTML, a ratatui feed reader, an alacritty config rebased
warm off Gruvbox, the VS Code SteamPunk theme, a tailnet drop-box, and a field-station SPA.
Five of the six had independently landed on a warm near-black ground within a few points of
each other, and on aged-parchment text within about six.

Three things were changed rather than averaged, all on evidence. One source's label colour
scored 3.24:1 against its own background at 10px, so it was lifted while holding its hue.
One source's status green was a desaturated web green with no warmth in it, the only token
across all five that visibly left the palette, so it became verdigris. And the whole thing
was brightened: the first cut averaged the sources and came out inert, so the values from
the liveliest of the five won instead. Restraint is a rule about how many colours you use,
not about how dim they are. `reference/variants.md` documents all three.

## Validating a palette

```sh
python3 tools/contrast.py                                # all four shipped variants
python3 tools/contrast.py --variant blueprint            # one of them
python3 tools/contrast.py --derive '#1a1410' '#c87533'   # one you are deriving
```

`--derive` also warns if your ground is too light, or is not warm. A cool grey next to brass
reads as dirt rather than as metal, and that single mistake undoes everything else.

## Prior art

The structural conventions owe a good deal to the taste-skill lineage
([Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)) and the aesthetic skills
that followed it. The aesthetic itself, the palette, the ornament test, the oxidation
semantics and the honesty rule are this repo's own.

## Licence

MIT. See `LICENSE`.
