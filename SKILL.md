---
name: steampunk-ui
description: Steampunk interface design that reads as a working instrument rather than Victorian cosplay. Warm lamp-lit grounds, a copper/brass signal hierarchy, status colours derived from real oxidation, drawn metal and analogue gauges, monospace typography, and a diegetic vocabulary where every noun belongs to one imagined machine. Use when asked for a steampunk, brass, copper, patina, industrial-Victorian, oil-lamp, foundry or salvaged-machinery aesthetic, or when building dashboards, CLIs, TUIs and data-dense tools that should feel like recovered equipment somebody keeps in good order.
---

# Steampunk UI

## 0. The doctrine

Four sentences. Everything below is enforcement.

> **Brass, not gold. Oxidation, not damage. It is an instrument, not a costume. No gear emoji.**

The mental image is a piece of recovered industrial equipment that somebody cleaned, kept
working, and grew fond of. It is scuffed because it has been used, not because a filter
was applied to it.

"Brass, not gold" is meant literally, including in the token file. Gold is not a working
metal, and a `--gold` token is the first step back toward cosplay. What reads as gold in a
good steampunk interface is polished brass catching light.

### The ornament test

This is the load-bearing rule of the whole skill, and it replaces a blanket ban on
ornament that produces something worse: a competent, legible, completely dead brown page.

> **Does this ornament depict a mechanism that actually exists here? If yes, draw it.
> If it depicts a theme, delete it.**

Worked through:

| Element | Verdict | Why |
|---|---|---|
| Rivets down a panel edge | **Draw it** | Depicts a plate that is bolted to a frame. |
| Rivets scattered on a button | Delete | Depicts nothing. Buttons are not bolted on. |
| A cog that turns only while work is in flight | **Draw it** | It is a state indicator with a real binding. |
| A cog that turns forever in the corner | Delete | A machine at rest is still. |
| A needle gauge bound to disk free space | **Draw it** | It is a readout. |
| A pressure dial that wobbles on a timer | Delete | It is a lie told in brass. |
| A brass gradient on a nameplate | **Draw it** | Depicts a machined plate catching light. |
| A brass gradient on every heading | Delete | Depicts a theme. |
| A serif nameplate at the top of the page | **Draw it** | Engraving is serif. |
| Serif body copy | Delete | Nothing engraves a paragraph. |

The failure mode is cosplay, and it is the only failure mode that matters. But the
*second* failure mode, and the one you will hit if you read section 1 too eagerly, is
inertness. A steampunk interface with no drawn metal, no light and no mechanism is not
restrained. It is just brown.

---

## 1. Absolute bans

These fail the ornament test in every context, so they need no judgement call.

**Ornament**
- Gear, cog, steam, monocle, top-hat or clock **emoji**. Any emoji at all. (A *drawn* SVG
  cog bound to real state is fine. See the test above.)
- Imported textures: cracked leather, riveted plate photographs, parchment scrolls, wood
  grain, brass sheet JPEGs. Metal here is *drawn in CSS and SVG*, always.
- Corner flourishes, filigree, scrollwork, laurel frames, ornamental dividers.
- Any instrument not bound to a real value. See section 10. This is the strict one.

**Typography**
- Blackletter and faux-Victorian display faces: Cinzel, Pirata One, Uncial Antiqua,
  IM Fell, MedievalSharp, Almendra. The single loudest cosplay tell.
- Serif anywhere except an engraved nameplate.
- Inter, Roboto, Open Sans, Helvetica, Arial. Not banned for being generic, banned for
  being humanist-neutral and carrying no industrial character at all.

**Colour**
- `filter: sepia()`, or any global brown overlay used as a shortcut for "aged".
- Pure black `#000000` or pure white `#ffffff`.
- Neutral greys. Every grey must carry warmth. A cool grey beside brass reads as dirt.
- Imported semantic colours: `#22c55e`, `#ef4444`, Tailwind `green-500`, Bootstrap
  `success`. Status comes from oxidation.

**Depth**
- Hard drop shadows. `shadow-md`, `shadow-lg`, anything with a visible dark edge.
  Depth here is a lit top edge plus a very soft, far-offset sink. See section 5.
- Faux-3D bevels: a matched light-top/dark-bottom border pair on a small control. That is
  a Windows 95 button, not a machined part.

---

## 2. The palette

Reconciled from five independently built steampunk interfaces, then tuned so **every ink
and signal token clears WCAG AA against all four surfaces**, not just the page ground.
Full token set with comments in `reference/tokens.css`. Validate with `tools/contrast.py`.

### Surfaces

Soot and lamp-oil. Four planes rather than three, because buttons and inset controls need
somewhere to sit that is not the panel they are on.

| Token | Value | Job |
|---|---|---|
| `--inset` | `#0a0804` | **Below** the page: wells, pipe tracks, code chips, scrollbar troughs. |
| `--void` | `#14110d` | Page. |
| `--iron` | `#1c1813` | Panels. |
| `--iron-2` | `#241f18` | Panel headers, table header rows. |
| `--iron-3` | `#2e2820` | Buttons, raised controls, hover. |
| `--seam` | `#3a3227` | Hairlines, internal dividers. |
| `--seam-lit` | `#4d4231` | Structural borders, control outlines. |

The planes sit 1.07 to 1.12 apart. Deliberate: they must be *visible* as separate planes,
not *accessible* as text pairs. Push them apart and it stops reading as one machined object.

### Ink

| Token | Value | Min | Job |
|---|---|---|---|
| `--ink` | `#e8dfcd` | 11.02 | Body text. |
| `--ink-dim` | `#a2937a` | 4.85 | Secondary, metadata. |
| `--ink-faint` | `#9d8f75` | 4.60 | Labels, units, captions. |

### Signal metals

Three tiers, three jobs, no overlap. This is what stops the palette reading as a brown mess.

| Token | Value | Min | Job |
|---|---|---|---|
| `--copper` | `#cd7c48` | 4.56 | **Data.** Values, hashes, identifiers, links. |
| `--brass` | `#c9a227` | 6.03 | **Structure.** Labels, framing, the accent. |
| `--brass-hi` | `#f0d891` | 10.37 | **Attention.** Active, live, the one figure that matters. |
| `--brass-lo` | `#7d6318` | n/a | **Not a text colour.** Gradient stops and engraved edges only. |

`--brass-hi` is scarce. Past roughly five percent of visible surface, nothing is emphasised.

### Oxidation (status)

Status colour is not imported. It is what these metals do when they corrode, which is why
it harmonises with no tuning.

| Token | Value | Min | Meaning | Chemistry |
|---|---|---|---|---|
| `--verdigris` | `#5f9e7d` | 4.63 | Healthy, verified, live | Copper carbonate |
| `--ember` | `#e8922a` | 5.95 | Warning, degraded, working | Hot iron |
| `--rust` | `#e86951` | 4.56 | Error, failed, corrupt | Iron oxide |

Verdigris is not a green. It is a desaturated blue-green. The instinct to reach for a
brighter, more legible green is the instinct to leave the palette. If it is unreadable, the
type is too small.

There is an optional fourth, `--olive` `#8fab45` (5.61), and exactly one reason to reach for
it: when you need verdigris to mean **information** (links, `GET`, a neutral note) and
therefore need a separate **go**. In a three-state system it is one hue too many. Leave it
out unless the interface genuinely has both an informational and a success register.

Status **fills**, for the pill variant in section 9, are mixed with `--inset` rather than
with the surface the pill sits on, at 18 percent. That reads as stamped into the plate
rather than raised on it, and it is also the only version that holds AA: mixing with the
surface lightens the backdrop and drops copper, rust and verdigris below 4.5 on `--iron-3`.

---

## 3. Typography

Monospace is the **body** face, not an accent. This is the largest departure from
conventional UI advice and it is what holds the aesthetic together: an instrument panel is
set in the face the machine can print.

- **Body, data, UI:** `Monaspace Xenon`, then `JetBrains Mono`, `IBM Plex Mono`,
  `ui-monospace`. Monaspace Xenon leads because it is a slab-serif monospace, precisely the
  Victorian-industrial register with none of the cosplay.
- **The nameplate:** `Georgia`, `Iowan Old Style`, serif. Uppercase, `.12em` tracking,
  filled with `--brass-plate` via `background-clip: text`, with
  `text-shadow: 0 1px 0 rgb(0 0 0 / .55)` so it sits *in* the plate rather than on it.
  **One per page.** This is engraving, and you engrave the machine's name, not its menu.
- **Signage:** a condensed industrial grotesque (`Oswald`, `Archivo Narrow`) if you need a
  third voice. Usually you do not.

Mechanics:

- Panel labels and column headers: uppercase, `10px`, `letter-spacing: .18em` to `.24em`,
  colour `--ink-faint`. Wide tracking does a stencil's work.
- Body and data: `13px`, `line-height: 1.6`.
- Numbers always monospace, right-aligned in tables, `font-variant-numeric: tabular-nums`
  so digits do not shift as values tick.
- Headings get weight and tracking, not size. A `30px` readout in `--brass-hi` outranks a
  `48px` heading, and the interface stays dense.

---

## 4. Geometry

- **`border-radius: 3px` on a plate, `2px` on anything inside it.** Machined, not moulded.
  Never `rounded-full` on a container.
- **Hairlines carry structure.** `1px solid var(--seam)`.
- **Visible compartmentalisation.** Every panel has a label strip, a border and a body.
  Data lives inside a labelled compartment, the way it does on real equipment.
- **Asymmetric grids.** `grid-template-columns: 0.86fr 1.28fr` beats `1fr 1fr`. A control
  panel is laid out by what each instrument needs, not by a designer's love of halves.
- **Density is the point.** `13px` body, `9px` cell padding, `18px` panel gaps.
- **Bimodal type scale.** Tiny tracked labels against large monospace readouts, with almost
  nothing between. That gap is where the instrument-panel feel lives.

---

## 5. Light and drawn metal

This is the section that separates a live interface from an inert one, and the thing that
gets left out most often. There are no hard shadows here, but there is a great deal of light.

### Lamp light on the bench

Two large, fixed radial gradients off the top corners, at 7 to 9 percent. Without this the
page is flat and no amount of correct colour will save it.

```css
body {
  background:
    radial-gradient(1200px 620px at 12% -8%,  rgb(201 162 39 / .09), transparent 62%),
    radial-gradient( 900px 520px at 108% 12%, rgb(205 124 72 / .07), transparent 58%),
    var(--void);
  background-attachment: fixed;
}
```

### The lit edge and the sink

Every plate gets a hairline of light along its top edge and a very soft, far-offset
ambient sink beneath. Note the `-22px` spread: the shadow is enormous, diffuse and almost
entirely below the element, which is occlusion rather than a drop shadow.

```css
.panel {
  background: var(--plate);
  border: 1px solid var(--seam);
  border-radius: var(--radius);
  box-shadow: inset 0 1px 0 rgb(240 216 145 / .07),   /* lit edge */
              0 18px 34px -22px rgb(0 0 0 / .85);      /* sink     */
}
```

### The brass plate

Four stops, not three. Bright, body, a dark rolloff at 62 percent, then a returning
highlight. That rolloff is a specular curve and it is the difference between a sheet of
brass and a beige smear.

```css
--brass-plate: linear-gradient(176deg, #e6cf8a 0%, #c9a227 38%, #8f7220 62%, #d8bd6a 100%);
```

Used for exactly two things: the nameplate (via `background-clip: text`) and the primary
action, which is a **lever**: brass plate background, near-black text `#241c05`, border
`--brass-lo`, and `text-shadow: 0 1px 0 rgb(255 255 255 / .28)` so the label reads as
struck into the metal.

### Rivets

Drawn, never imported. A repeating radial gradient down the inside edges of a plate, at
half opacity, on `::before` and `::after`.

```css
.riveted::before, .riveted::after {
  content: ''; position: absolute; top: 9px; bottom: 9px; width: 7px;
  pointer-events: none; opacity: .5;
  background-image: radial-gradient(circle at 50% 50%,
    var(--brass-hi) 0 1px, var(--brass-lo) 1.4px, transparent 2.4px);
  background-size: 7px 30px;
  background-repeat: repeat-y;
}
.riveted::before { left: 8px; }
.riveted::after  { right: 8px; }
```

Panel edges only. A rivet holds a plate to a frame; it does not decorate a button.

### Vignette and grain

Lamp light is only half the lighting, and the other half gets forgotten. You also need
**dark added at the edges**, otherwise a lit page just looks uniformly beige. Both go on a
single fixed overlay above the content, not on the body background.

```css
.atmosphere {
  position: fixed; inset: 0; pointer-events: none; z-index: 9998;
  background:
    radial-gradient(120% 80%  at 50% -10%, rgb(217 137 43 / .06), transparent 60%),
    radial-gradient(140% 120% at 50% 120%, rgb(0 0 0 / .55),      transparent 55%);
}
/* Grain. mix-blend-mode: overlay rather than flat opacity, so it bites into
   the lit areas and leaves the shadows alone, which is how grain behaves. */
.atmosphere::after {
  content: ''; position: absolute; inset: 0;
  opacity: .05; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,...feTurbulence...");
}
```

Never on a scrolling container.

### Chrome

The default scrollbar is the single most common leak. A stock blue-grey macOS or Windows
scrollbar running down the side of a brass panel undoes a great deal of careful work, and
almost nobody remembers to style it.

```css
* { scrollbar-width: thin; scrollbar-color: var(--seam-lit) transparent; }
*::-webkit-scrollbar       { width: 10px; height: 10px; }
*::-webkit-scrollbar-track { background: var(--inset); }
*::-webkit-scrollbar-thumb {
  background: var(--seam-lit);
  border: 2px solid var(--inset);   /* insets the thumb into its trough */
  border-radius: 6px;
}
*::-webkit-scrollbar-thumb:hover { background: var(--brass-lo); }

::selection { background: rgb(201 162 39 / .25); color: var(--ink); }
```

Also worth doing, and cheap: `accent-color: var(--brass)` on checkboxes and radios, and
`user-select: all` on any code chip meant to be copied.

### Hazard tape

Permitted, conditionally, and it passes the ornament test only when it marks a genuine
boundary: the edge of a destructive zone, a section that writes to production, a panel
holding irreversible controls.

```css
.hazard {
  height: 4px; flex-shrink: 0; opacity: .65;
  background: repeating-linear-gradient(-45deg, var(--ember) 0 12px, #1a1408 12px 24px);
}
```

A hazard stripe across the top of a page because it looks industrial is decoration, and it
also spends a warning on nothing. One per screen, at most, and only where the hazard is real.

---

## 6. The analogue instrument

A steampunk interface that has no gauge is not really trying. This is the flagship
component and the single largest contributor to feeling alive. Full SVG in
`reference/components.md`; the anatomy is:

1. **Bezel.** An outer circle filled with the brass plate gradient.
2. **Face.** An inner circle with a `radialGradient` centred at `50% 38%`, dark at the
   edge, lifting toward the top. The face is lit from above, like everything else.
3. **Ticks.** Eleven, generated in a loop over the sweep. Majors every fifth, longer and
   in `--brass-hi`; minors shorter and in `--ink-faint`.
4. **Arcs.** One or two stroked arcs on the same radius showing the composition of the
   reading, drawn with a polar helper. This is where a gauge beats a number.
5. **Needle.** A three-point polygon, in **bone `--ink`, never red.** Red is reserved for
   things that have actually gone wrong, and a permanently red needle spends that signal
   on nothing.
6. **Spindle.** A brass hub circle over the needle's pivot, with a dark centre.

The one detail that decides whether it looks machined or broken:

```css
.needle { transform-box: fill-box; transform-origin: 50% 94.3%; transition: transform 1.5s var(--ease); }
```

The polygon spans y=34 to y=104 and the hub sits at y=100, so the pivot is 94.3 percent
down the needle's own box. Get this wrong and the needle visibly wobbles off its spindle,
which is the sort of thing nobody can name but everybody notices.

A sweep of `-125°` to `+125°` reads as a real instrument. A full 360 does not.

---

## 7. Motion

Brass has inertia and friction. The distinction that matters:

**Continuous values settle. They never overshoot.**
A needle crossing its dial, a pipe filling, a figure changing. Use
`cubic-bezier(.16, 1, .3, 1)`, which decelerates hard and stops. No springs, no bounce.
An overshooting readout is the fastest way to make heavy metal read as plastic.
`250ms` for state, `600ms` for a value settling, `1500ms` for a needle.

**Discrete events may arrive with impact.**
A verdict being stamped is a physical event and it is allowed to land like one:

```css
@keyframes thud { 0% { transform: scale(1.5) rotate(-5deg); opacity: 0; } 100% { transform: none; opacity: 1; } }
```

Note it settles *from* overshoot into rest, rather than springing past its target. A stamp
slams down. It does not boing.

**Continuous animation must be bound to continuous state.**

```css
.cog { animation: spin 9s linear infinite; animation-play-state: paused; opacity: .5; }
body.working .cog { animation-play-state: running; opacity: 1; }
```

That cog is honest: it turns if and only if work is in flight. Ambient motion for its own
sake is banned, because a machine at rest is still.

Animate `transform` and `opacity` only. Honour `prefers-reduced-motion` by killing every
animation and the needle transition with it.

---

## 8. Name the machine

**This is where "alive" actually comes from, and it costs nothing.** Colour and gradients
get you a handsome dead page. What makes an interface feel like a machine is that every
noun in it belongs to the same imagined machine.

Pick the machine before you write any copy. A receiving bay. A signal station. A foundry
floor. A ship's hold. Then name everything from inside it, consistently, including empty
states and error text.

| Generic | Diegetic |
|---|---|
| Upload area | **Intake** |
| File list | **The hold** |
| History | **Delivery ledger** |
| Progress bar | **Pipe** (filling with pressure) |
| Status badge | **Stamp** (verified, stored, corrupt) |
| Primary button | **Lever** |
| Settings | **Switches** |
| "No files yet" | "Nothing stowed here yet. Drop something into the intake above." |
| "Upload complete" | "Delivered" |
| "Processing" | "In transit" |
| "Saved to /data" | "Deposits settle in /data" |

Two rules that keep this from turning into whimsy:

- **The metaphor must survive the error path.** If "corrupt" reads as
  `checksums disagree, the copy on the far side was deleted, send it again`, the machine is
  real. If the happy path is nautical and the errors are stack traces, it is a skin.
- **Never sacrifice precision for flavour.** "In transit" is better than "Uploading"
  because it is equally precise and more specific to the machine. "Sending your parcel on
  its merry way" is worse than both. If the diegetic word is vaguer than the plain one,
  use the plain one.

---

## 9. Components

Working CSS and SVG in `reference/components.md`. The shapes:

**Riveted plate.** The universal container. `--plate` gradient, `1px solid --seam`, lit
edge and sink, drawn rivets down both inside edges, a label strip in `10px` tracked
`--ink-faint` with a right-aligned reading, then a body.

**Gauge.** Section 6.

**Readout.** `30px` monospace in `--brass-hi`, with a small tracked uppercase caption
beneath, and a rule-separated stack of secondary readings under that.

**Pipe.** A `5px` inset track with `box-shadow: inset 0 1px 2px rgb(0 0 0 / .75)` so it
reads as a channel cut into the plate, and a fill that transitions its width. Working state
gets a sliding gradient; verified goes verdigris; failed goes rust.

**Stamp.** `10px` uppercase, `.16em` tracking, `1px solid currentColor`, `2px` radius,
transparent background. Colour carries the verdict. Arrives with a thud. This is for a
verdict **on a row**, where the row's own name is what you are scanning.

**Lamp pill.** The variant for a **roster**, where you are scanning twenty statuses at once
and need a shape rather than a word. Same geometry, but with a tinted fill and a lamp dot.
The fill is mixed with `--inset`, never with the surface, so it reads as stamped into the
plate: `background: color-mix(in srgb, var(--verdigris) 18%, var(--inset))`. Mixing with
the surface instead lightens the backdrop and pushes copper, rust and verdigris below AA.

**Overprint.** A document-level verdict, not a row-level one: `DRAFT`, `SUPERSEDED`,
`UNVERIFIED`. Absolutely positioned in a corner, `transform: rotate(-8deg)`, `2px` border in
the status colour, `opacity: .82`, `mix-blend-mode: screen`, `pointer-events: none`, and
three stacked lines of tracked uppercase at descending sizes. One per document.

**Lever.** The primary action, in brass plate. One per panel at most.

**Status lamp.** Two kinds, and conflating them is a real mistake. A **liveness** lamp is
powered by the thing it reports on, so it glows and breathes when live and is **dark** when
dead. An **alarm** lamp is powered by the alarm circuit, so it lights *because* of the fault
and flashes to draw the eye. Pick one convention per product.

**Ledger row.** Name, stamp and metadata on one baseline, pipe beneath, then optional
reason and digest lines in `--ink-faint`.

**Chrome.** Scrollbars, selection, accent-color, copyable code chips. The default scrollbar
is the single most common leak in the whole aesthetic and almost nobody remembers it.

**Hazard tape.** A 4px `-45deg` stripe at `.65` opacity, marking a genuine boundary only.

**Section marker.** A 9px square rotated 45 degrees with a soft glow, which is a lit rivet
head seen square-on. Cheaper than an icon and it never goes stale.

**Empty state.** Composed, not apologetic: a thin-stroke SVG at `.35` opacity and one
sentence in the machine's own vocabulary.

---

## 10. The honesty rule

**No instrument may display a value that is not real.**

This is what separates the aesthetic from set dressing, and it is not negotiable. A
pressure gauge bound to disk free space is welcome. A pressure gauge that wobbles on a
timer to look busy is a lie told in brass, and it makes every honest readout beside it
untrustworthy.

- No decorative gauges, sparklines, oscilloscopes or needles without a bound source.
- No `Math.random()` in a chart, ever, including in a demo. Ship real sample data.
- Continuous animation only where state is continuous. The cog stops when the work stops.
- Placeholder figures must be plausible and specific: `47.2%`, `18 412 GRT`, `epoch 2 841`.
  Never `99.99%`, `50%`, `1,234`.
- **Absent means absent.** A missing reading renders as an explicit `NO SIGNAL` in
  `--ink-faint`. Never as zero, never as a dash that could pass for a value, and never in
  verdigris. A missing reading that looks like a good reading is the worst bug this
  aesthetic can ship.
- Loading is its own state with its own treatment, not a zero held briefly.
- **Reporting a verdict is part of the verdict.** If the check passed but the result could
  not be recorded, the row does not get to claim "verified". Say what you actually know.

---

## 11. Variants

Foundry is the default. Soot, Blueprint and Verdigris, plus the derivation rule, are in
`reference/variants.md`. Never mix two in one product.

---

## 12. Terminal and TUI

Same tokens on ratatui, ANSI 256 and terminal themes. `reference/terminal.md` has the
ratatui `Theme` struct, the computed 256 fallback and an alacritty config.

Two rules that matter more than the table. **Never use the 16 ANSI colour names**: the
user's theme redefines them and your brass arrives as somebody else's highlighter. And in
256-colour mode, **do not set a background at all**: the cube has no warm near-black, so
the surfaces fall onto the neutral greyscale ramp and throw away the warmth the whole
aesthetic rests on. Inherit the user's background, set foregrounds only.

---

## 13. Before you call it done

**Not cosplay**
- [ ] Zero emoji, zero blackletter, zero imported textures, zero flourishes.
- [ ] Every ornament passes the test in section 0: it depicts a mechanism that exists.
- [ ] One nameplate, one lever per panel, `--brass-hi` under five percent of the surface.

**Not inert**
- [ ] There is lamp light on the page, and a vignette darkening the edges. Not a flat fill.
- [ ] Plates have a lit top edge and a soft sink, not a hard shadow and not nothing.
- [ ] There is at least one drawn instrument, and its needle is bone rather than red.
- [ ] Every noun belongs to one named machine, error paths and empty states included.
- [ ] **Scrollbars are themed.** Selection colour too. Scroll a panel and look at it.

**Honest**
- [ ] Every gauge, pipe and cog is bound to a real value or a real state.
- [ ] Absent data renders as `NO SIGNAL`, not as zero and not as green.
- [ ] No `Math.random()` anywhere, demo included.

**Sound**
- [ ] Every colour comes from the token file. No literal hex in a component.
- [ ] `tools/contrast.py` reports no token below AA on any surface.
- [ ] Continuous values settle without overshoot; only discrete events land with impact.
- [ ] `prefers-reduced-motion` kills the animations and the needle transition.
- [ ] Squint at it. You should see a lit instrument panel, not a brown web page and not a
      theme park.
