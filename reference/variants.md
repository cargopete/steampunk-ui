# Variants

Four sanctioned palettes and the rule for deriving a fifth. All four are validated by
`tools/contrast.py`; every ink and signal token clears WCAG AA against all four of that
variant's surfaces.

**Never mix two variants in one product.** Pick one at the start and commit. Half a screen
in Foundry and half in Blueprint does not read as range, it reads as a bug.

---

## Foundry (default)

The full copper, brass and polished-brass ramp on soot and lamp-oil. Use this unless there
is a specific reason not to.

Copper is data, brass is structure, `--brass-hi` is attention. Oxidation carries status.

**For:** dashboards, indexers, admin panels, monitoring, transfer tools, anything with more
than about twenty discrete facts on screen at once. This is the variant the doctrine was
written around.

**Against:** marketing pages and anything image-led, where the density that makes Foundry
work has nothing to be dense about.

---

## Soot

```css
--void:   #0d0b08;
--iron:   #14110d;
--iron-2: #1c1813;
--iron-3: #241f18;
--copper: #c9a227;   /* collapsed into brass */
```

Copper dropped, the whole surface ramp pushed a plane deeper. Two tiers instead of three,
so the hierarchy simplifies to structure and attention. Closer to a printed listing than to
an instrument panel.

**For:** CLI output, log viewers, diff views, anything text-dominant where a third accent
just adds noise to a wall of characters.

**Against:** dashboards. Losing copper removes the layer that separates a value from its
label, and readouts go flat.

---

## Blueprint

```css
--oxide: #7cbcd6;
--brass: #7cbcd6;    /* structure goes cool, data stays warm */
--brass-plate: linear-gradient(176deg, #b9dfec 0%, #7cbcd6 38%, #43809a 62%, #9dcfe2 100%);
```

Oxidised teal as a cool counterpoint against the warm rust. The only variant with two hue
families, and it exists because a single-hue palette cannot separate three kinds of
information when one of them is spatial.

The split is **structure cool, data warm.** Edges, axes, grid lines, connectors and
container outlines take oxide. Nodes, values, labels and readouts stay copper and
`--brass-hi`. A viewer can then tell the wiring from the readings at a glance, which in a
topology map is the entire job.

Note the plate gradient is restated. A cool structure with a warm nameplate is the one
mixture that genuinely does read as a mistake.

**For:** schematics, topology and network maps, dependency graphs, architecture diagrams,
flow charts, anything where structure is drawn rather than implied.

**Against:** tables and cards. With no spatial layer to colour, the teal has no job and
simply reads as a palette that could not make up its mind.

---

## Verdigris

```css
--copper:    #5f9e7d;
--brass:     #7fbb9b;
--brass-hi:  #c3e3d2;
--verdigris: #c9a227;   /* healthy re-reads as brass once green is structural */
```

Oxidation-forward. Green promoted to the primary accent, the warm metals demoted to
support. Weathered rather than polished: a machine left outdoors rather than one kept in
the workshop.

Note the swap in the status row. Once green carries structure it can no longer also mean
healthy, so healthy becomes brass. Reusing green for both is how you get a dashboard where
everything looks fine because everything is the same colour.

**For:** marketing surfaces, landing pages, documentation sites, anything narrative.

**Against:** instruments. This is the one variant that is a mood rather than an information
design, and it should never run a control panel.

---

## Deriving a fifth

Only when a project has a genuine identity constraint, such as an existing brand colour
that must appear. Not because the default feels samey; samey across a fleet of tools is the
point.

1. **The ground must be warm and dark.** Red channel leads, then green, then blue, with
   luminance under about `0.05`. A cool grey beside brass reads as dirt rather than metal,
   and that single mistake undoes everything else.
2. **Four surfaces, roughly 1.05 to 1.15 apart.** Visible as separate planes, never
   accessible as text pairs. Push them further and it stops reading as one machined object.
3. **Three signal tiers, distinct jobs.** Whatever the hues, you need one for data, one for
   structure, one for attention. Two flattens every readout; four means nothing is emphasised.
4. **Restate the plate gradient.** Four stops, with the dark rolloff at 62 percent. A
   variant that changes the accent but keeps the old brass plate will have a nameplate that
   belongs to a different machine.
5. **Status from oxidation, not from the web.** Whatever metal you introduce, ask what it
   looks like corroded. Never `#22c55e` and `#ef4444`.
6. **Every ink and signal token clears AA against all four surfaces.** Not just the page
   ground, which is the mistake that makes panel-header labels unreadable.

Then check it:

```sh
python3 tools/contrast.py --derive '#1a1410' '#c87533'
```

which validates the accent and warns if the ground is too light or insufficiently warm. Add
the variant to the `VARIANTS` dict in that file and run the full check before shipping, so
the next person to touch the palette finds out immediately if they broke it.

---

## Where the canonical palette came from

Foundry is reconciled, not invented, from six steampunk interfaces built independently of
one another:

| Source | Ground | Text | Primary signal |
|---|---|---|---|
| An indexer dashboard, Rust serving HTML | `#080501` | `#d4c49a` | copper `#c4922a` |
| A ratatui feed reader | `#1a1410` | `#d4b896` | copper `#c87533`, verdigris `#4a6b5a` |
| An alacritty config, Gruvbox rebased warm | `#1c1710` | `#d5b078` | antique gold `#c89b3c` |
| The VS Code SteamPunk theme | `#202124` | `#eeeeee` | rust `#d1675a`, oxide teal `#68aec9` |
| A tailnet drop-box, Rust serving HTML | `#14110d` | `#e8dfcd` | brass `#c9a227`, verdigris `#5f9e7d` |
| A field-station SPA, ~1.7k lines of CSS | `#0e0b06` | `#f6ecd4` | amber `#d9892b`, olive `#88a23f` |

Five of the six landed on a warm near-black ground within a few points of each other and on
aged-parchment text within about six, with no coordination at all. That agreement is what
the default encodes.

Three things were changed rather than averaged, and all three on evidence.

**Labels were lifted.** The original label token `#7d6035` scores 3.24:1 against its own
ground, which is a fail at any size and a bad one at the 10px it was used at. It became
`--ink-faint` `#9d8f75`, 4.60:1 worst case. Hue held, value channel moved.

**The status green was replaced.** One source used `#7eb87e`, a desaturated web green with
no warmth in it, and it was the one token across all five that visibly left the palette.
Verdigris is copper carbonate and it belongs.

**The whole palette was brightened.** The first cut of Foundry averaged the sources and came
out inert: ink at 10.96:1 against its ground and brass at 6.61. The drop-box, which is by
some margin the most alive of the five, runs ink at 14.22 and brass at 7.78. Its values won.
Restraint is a rule about *how many* colours you use, not about how dim they are, and
confusing the two produces a page that is correct and dead.

Three sources contributed something the others could not, and all three were kept rather
than averaged away:

- **The VS Code theme** is the outlier on every axis: neutral ground, white text, and the
  only cool accent in the set. That cool accent became Blueprint rather than being folded
  into the default.
- **The drop-box** contributed almost everything in section 5 and section 8 of the skill:
  the four-stop plate gradient, drawn rivets, the lit edge and ambient sink, lamp light on
  the page, the analogue gauge with its needle pivot, and the diegetic vocabulary. The first
  cut of this skill banned most of that as cosplay, which was wrong. It is the difference
  between a restrained interface and an inert one.
- **The field station** contributed the chrome and the edge cases: themed scrollbars, the
  vignette that darkens the edges (as against the lamps that light the middle), grain on an
  `overlay` blend rather than flat opacity, hazard tape, the rotated overprint stamp, the
  `--inset` plane below the page, and the diamond section marker. It also forced a genuine
  correction to the lamp doctrine, because it flashes its *error* lamp where the drop-box
  leaves a failure dark. Both are right, for different lamps, and the skill now says so.

The field station also splits `--verdigris` (information, links, `GET`) from an olive
`--ok`, which is why `--olive` exists as an optional fourth status hue. Its own error colour
`#bd4a2c` scores 2.90:1 on our raised plane and its tinted error pill only 3.51:1, so the
tinting method was replaced rather than copied: fills mix with `--inset` instead of with the
surface, which keeps every token above 4.6 and reads as stamped into the plate besides.
