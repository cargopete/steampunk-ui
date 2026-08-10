# Terminal and TUI annex

The same tokens, applied to ratatui, ANSI 256 and terminal emulator themes. Nothing about
the doctrine changes: brass not gold, oxidation not damage, an instrument not a costume,
and no gear emoji. Terminals make the last one easier to obey.

What terminals cannot give you is section 5 of the skill: there are no gradients, no lit
edges and no lamp light. That means the two remaining levers, **colour hierarchy** and
**diegetic vocabulary** (section 8), have to carry the whole load. A TUI in this aesthetic
lives or dies on whether its panel titles say `INTAKE` and `THE HOLD` rather than `Files`
and `Log`.

---

## Truecolour

If the terminal reports truecolour (`COLORTERM=truecolor` or `24bit`), use the hex values
from `reference/tokens.css` unchanged. Everything was tuned for 24-bit and degrades from
there, not toward it.

---

## The 256-colour fallback

Nearest xterm-256 indices, computed rather than eyeballed, and restricted to the **colour
cube (16 to 231)** rather than the full set. That restriction is deliberate: an unrestricted
nearest-match sends `--ink` to index 253, which is a perfectly neutral `#dadada`, and
`--ink-dim` to a pinkish 138. Both are technically closer in distance and both throw away
the warmth the aesthetic rests on. Holding the hue and accepting a little luminance drift
is the right trade here.

| Token | Hex | Index | Renders as |
|---|---|---|---|
| `ink` | `#e8dfcd` | **187** | `#d7d7af` |
| `ink-dim` | `#a2937a` | **144** | `#afaf87` |
| `ink-faint` | `#9d8f75` | **144** | `#afaf87` |
| `copper` | `#cd7c48` | **173** | `#d7875f` |
| `brass` | `#c9a227` | **178** | `#d7af00` |
| `brass-hi` | `#f0d891` | **222** | `#ffd787` |
| `verdigris` | `#5f9e7d` | **72** | `#5faf87` |
| `ember` | `#e8922a` | **172** | `#d78700` |
| `rust` | `#e86951` | **209** | `#ff875f` |
| `oxide` (Blueprint) | `#7cbcd6` | **110** | `#87afd7` |

**`ink-dim` and `ink-faint` collapse onto the same index.** They are only 0.25 of a
contrast ratio apart in truecolour, so this is honest rather than a rounding failure. In a
256-colour TUI, pick one of them and use `Modifier::DIM` for the other rather than
inventing a distinction the terminal cannot render.

### Do not set a background in 256-colour mode

The surfaces map to 233 to 235, which are on the **greyscale ramp** and therefore perfectly
neutral. The cube has no warm near-black at all: its darkest warm entries are fully
saturated maroons. So the fallback either throws away the warmth or goes maroon, and both
are worse than nothing.

Inherit the user's background and set foregrounds only. Parchment on the user's own black
still reads correctly; a neutral grey panel behind brass reads as dirt.

### Never use the 16 ANSI names

`Color::Yellow` is whatever the user's theme decided yellow is, and half the popular themes
make it lime. Your brass will arrive as somebody else's highlighter. Index or truecolour,
always.

---

## ratatui

```rust
//! Palette. Brass, not gold. Oxidation, not damage. Restraint above all.
//! Truecolour values; see the 256 table above for the fallback.

use ratatui::style::{Color, Modifier, Style};

pub struct Theme {
    pub void:      Color,
    pub iron:      Color,
    pub seam:      Color,
    pub ink:       Color,
    pub ink_dim:   Color,
    pub ink_faint: Color,
    pub copper:    Color,
    pub brass:     Color,
    pub brass_hi:  Color,
    pub verdigris: Color,
    pub ember:     Color,
    pub rust:      Color,
}

pub const THEME: Theme = Theme {
    void:      Color::Rgb( 20,  17,  13),  // #14110d  soot and lamp-oil
    iron:      Color::Rgb( 28,  24,  19),  // #1c1813  panels
    seam:      Color::Rgb( 77,  66,  49),  // #4d4231  frames and separators
    ink:       Color::Rgb(232, 223, 205),  // #e8dfcd  body text
    ink_dim:   Color::Rgb(162, 147, 122),  // #a2937a  secondary
    ink_faint: Color::Rgb(157, 143, 117),  // #9d8f75  labels, keybindings
    copper:    Color::Rgb(205, 124,  72),  // #cd7c48  DATA
    brass:     Color::Rgb(201, 162,  39),  // #c9a227  STRUCTURE
    brass_hi:  Color::Rgb(240, 216, 145),  // #f0d891  ATTENTION, sparingly
    verdigris: Color::Rgb( 95, 158, 125),  // #5f9e7d  healthy
    ember:     Color::Rgb(232, 146,  42),  // #e8922a  degraded
    rust:      Color::Rgb(232, 105,  81),  // #e86951  failed
};

impl Theme {
    pub fn body(&self)  -> Style { Style::new().fg(self.ink) }
    pub fn label(&self) -> Style { Style::new().fg(self.ink_faint).add_modifier(Modifier::BOLD) }
    pub fn data(&self)  -> Style { Style::new().fg(self.copper) }
    pub fn frame(&self) -> Style { Style::new().fg(self.seam) }
    pub fn dim(&self)   -> Style { Style::new().fg(self.ink_dim).add_modifier(Modifier::DIM) }

    /// The active row. Inverted onto copper, the one place in the system where
    /// a metal is used as a background.
    pub fn selected(&self) -> Style {
        Style::new().fg(self.void).bg(self.copper).add_modifier(Modifier::BOLD)
    }
}
```

`body()` and friends deliberately do **not** set a background, so the theme works over the
user's terminal without fighting it. Set `void` only when drawing a genuinely opaque panel
over other content.

---

## The gauge, in text

A terminal cannot draw a needle, but it can draw a dial, and the honesty rule applies
identically. Block-shaded bars are fine as real gauges and are not fine as decoration.

```
 CAPACITY  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒░░░░░░░░  61.2%
           └ held here      └ other      └ free
```

Use `▓` for your own consumption, `▒` for other, `░` for free, in `brass`, `ink_dim` and
`seam` respectively. One glyph per two percent at a width of 50 is a readable resolution.
If the source did not answer, print `NO SIGNAL` in `ink_faint` across the bar's width
rather than an empty track, because an empty track is a reading of zero.

---

## Box drawing

Frames are hairlines here too. Use the light set, `│ ─ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`, in `seam`.

Heavy or double box drawing (`┃ ━ ╔ ═`) is the terminal equivalent of a 4px border and
reads as loud rather than sturdy. Reserve it for a single structural separation per screen,
if at all.

No ASCII art logos and no figlet banners. The terminal equivalent of the nameplate is a
single line of tracked uppercase in `brass_hi`, which is quieter and considerably better.

---

## Alacritty

```toml
[colors.primary]
background = "#14110d"   # soot and lamp-oil, never olive, never charcoal
foreground = "#e8dfcd"   # aged parchment

[colors.cursor]
cursor = "#f0d891"       # polished brass, the one thing that should catch your eye
text   = "#14110d"

[colors.normal]
black   = "#3a3227"      # the seam, not the background: an unusable black wastes a slot
red     = "#c1503c"
green   = "#4d8266"
yellow  = "#c9a227"      # brass, notably below a stock #d79921
blue    = "#5b91a8"
magenta = "#a4633a"
cyan    = "#5f9e7d"
white   = "#a2937a"

[colors.bright]
black   = "#4d4231"
red     = "#e86951"      # rust
green   = "#5f9e7d"      # verdigris
yellow  = "#f0d891"      # brass-hi
blue    = "#7cbcd6"      # oxide
magenta = "#cd7c48"      # copper
cyan    = "#7fbb9b"
white   = "#e8dfcd"      # ink
```

Two deliberate choices. `normal.black` is the seam colour rather than the background,
because a black matching the background is a slot you can never see. And `yellow` sits well
below the usual `#d79921`, since the point is antique brass rather than a highlighter.

The natural font pairing is **Monaspace Xenon**, a slab-serif monospace and therefore the
Victorian-industrial register with none of the cosplay. `JetBrains Mono` and
`IBM Plex Mono` are the fallbacks.

---

## CLI output

- Colour is a signal, not a wrapper. Uncoloured ink is the default and most lines should be it.
- Honour `NO_COLOR`, and check `isatty` before emitting any escape. A brass escape sequence
  in a log file helps nobody.
- Status prefixes carry the oxidation semantics: `ok` in verdigris, `warn` in ember, `fail`
  in rust. No symbols, no emoji, no `[✓]`.
- Column headers uppercase in `ink_faint`. Values in `copper`. The one figure that matters
  in `brass_hi`, once per screen.
- Name the machine here too. A CLI that prints `intake`, `the hold` and `consignment` in its
  own subcommands is doing the same work as a gradient does on the web, for free.
- Absent readings print `NO SIGNAL` in `ink_faint`. Not `0`, not `-`, and never anything
  mistakable for a healthy value.
