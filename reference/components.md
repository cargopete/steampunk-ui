# Component recipes

Working CSS and SVG for the shapes named in `SKILL.md`. Everything assumes
`reference/tokens.css` is loaded. No literal hex appears in a component; if you find
yourself typing one, the token set is missing something and the token set is what should
change.

---

## The riveted plate

The universal container, and the thing most steampunk attempts get wrong by making it a
flat brown box.

```css
.plate {
  position: relative;
  background: var(--plate);
  border: 1px solid var(--seam);
  border-radius: var(--radius);
  /* Light along the top edge, ambient occlusion beneath. Not a drop shadow:
     note the -22px spread, which keeps it almost entirely under the element. */
  box-shadow: var(--lit), var(--sink);
}

/* Rivets, drawn rather than imported. Panel edges only: a rivet holds a plate
   to a frame, it does not decorate a button. */
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

/* Label strip: what this compartment is, and its headline reading. */
.plate-label {
  display: flex; justify-content: space-between; align-items: center; gap: 12px;
  padding: 12px 26px 0;
  font-size: var(--size-label);
  letter-spacing: var(--track-plate);
  text-transform: uppercase;
  color: var(--ink-faint);
}

.plate-body { padding: var(--pad-plate); }
```

The horizontal padding is `26px` rather than something tidier because the rivet strips
occupy the first and last 15px of the plate. Text that runs under a rivet looks like a
mistake, because it is one.

---

## The nameplate

One per page. This is engraving, and you engrave the machine's name, not its menu.

```css
h1.nameplate {
  margin: 0;
  font-family: var(--font-plate);
  font-size: 30px; font-weight: 600;
  letter-spacing: .12em; text-transform: uppercase;
  background: var(--brass-plate);
  -webkit-background-clip: text; background-clip: text;
  color: transparent;
  /* Sits IN the plate rather than on it. */
  text-shadow: 0 1px 0 rgb(0 0 0 / .55);
}
```

Use a hair space rather than a hyphen in a hyphenated name (`Storage&#8202;-&#8202;Neo`),
because at `.12em` tracking a plain hyphen collides with the letterforms either side.

---

## The gauge

The flagship. An SVG dial with a brass bezel, a lit face, ticks, composition arcs and a
bone needle on a spindle.

```html
<svg id="gauge" viewBox="0 0 200 200" aria-hidden="true">
  <defs>
    <linearGradient id="bez" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#e6cf8a"/>
      <stop offset=".45" stop-color="#c9a227"/>
      <stop offset=".62" stop-color="#8f7220"/>
      <stop offset="1"   stop-color="#d8bd6a"/>
    </linearGradient>
    <!-- Lit from above, like everything else on the bench. -->
    <radialGradient id="face" cx="50%" cy="38%" r="72%">
      <stop offset="0" stop-color="#2b251c"/>
      <stop offset="1" stop-color="#171310"/>
    </radialGradient>
  </defs>

  <circle cx="100" cy="100" r="94" fill="url(#bez)"/>              <!-- bezel   -->
  <circle cx="100" cy="100" r="84" fill="url(#face)" stroke="#3a3227"/>
  <g id="ticks"></g>
  <path id="arcUsed" fill="none" stroke="#4d4231" stroke-width="7" stroke-linecap="round"/>
  <path id="arcMine" fill="none" stroke="#c9a227" stroke-width="7" stroke-linecap="round"/>

  <!-- Bone, not red. Red is reserved for things that have actually gone wrong,
       and a permanently red needle spends that signal on nothing. -->
  <polygon id="needle" class="needle" points="100,34 96.6,104 103.4,104" fill="#e8dfcd"/>
  <circle cx="100" cy="100" r="9" fill="url(#bez)" stroke="#241c05"/>
  <circle cx="100" cy="100" r="3" fill="#241c05"/>

  <text x="100" y="150" text-anchor="middle" font-family="ui-monospace,monospace"
        font-size="9" letter-spacing="2.4" fill="#9d8f75">FREE</text>
</svg>
```

```css
/* The polygon spans y=34..104 and the hub sits at y=100, so the pivot is 94.3%
   down its own box. Anything else and the needle wobbles off the spindle,
   which nobody can name and everybody notices. */
.needle {
  transform-box: fill-box;
  transform-origin: 50% 94.3%;
  transition: transform var(--dur-sweep) var(--ease);
}
#gauge { width: 168px; height: 168px; flex: none; }
```

```js
const A0 = -125, A1 = 125;   // a real instrument sweeps ~250 degrees, not 360

const pol = (cx, cy, r, deg) => {
  const a = (deg - 90) * Math.PI / 180;
  return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
};

function arc(r, from, to) {
  const [x0, y0] = pol(100, 100, r, from), [x1, y1] = pol(100, 100, r, to);
  return `M${x0.toFixed(2)},${y0.toFixed(2)} A${r},${r} 0 ${to - from > 180 ? 1 : 0} 1 ${x1.toFixed(2)},${y1.toFixed(2)}`;
}

// Eleven ticks, majors every fifth.
(function ticks() {
  const g = document.getElementById('ticks');
  for (let i = 0; i <= 10; i++) {
    const deg = A0 + (A1 - A0) * i / 10;
    const major = i % 5 === 0;
    const [x0, y0] = pol(100, 100, major ? 62 : 68, deg);
    const [x1, y1] = pol(100, 100, 74, deg);
    const l = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    l.setAttribute('x1', x0.toFixed(2)); l.setAttribute('y1', y0.toFixed(2));
    l.setAttribute('x2', x1.toFixed(2)); l.setAttribute('y2', y1.toFixed(2));
    l.setAttribute('stroke', major ? '#f0d891' : '#9d8f75');
    l.setAttribute('stroke-width', major ? '2.2' : '1.2');
    g.appendChild(l);
  }
})();

// frac and mineFrac come from a real reading. If the source did not answer,
// do NOT call this with 0: leave the needle where it is and show NO SIGNAL.
function setGauge(frac, mineFrac) {
  const span = A1 - A0;
  document.getElementById('needle').style.transform =
    `rotate(${(A0 + span * frac).toFixed(2)}deg)`;
  document.getElementById('arcUsed')
    .setAttribute('d', arc(74, A0, A0 + span * Math.max(1 - frac, 0.004)));
  document.getElementById('arcMine')
    .setAttribute('d', arc(74, A0, A0 + span * Math.max(mineFrac, 0.004)));
}
```

The `Math.max(x, 0.004)` floor is not cosmetic. A zero-length arc with
`stroke-linecap: round` renders as nothing at all in some engines and as a stray dot in
others, so the floor keeps a genuine zero looking like a genuine zero.

Since the dial is `aria-hidden`, the numeric readout beside it carries the accessible
value. A screen reader should never have to interpret a needle.

---

## Readout

```css
.readout {
  font-family: var(--font-mono);
  font-size: var(--size-value);
  line-height: 1.05;
  color: var(--brass-hi);
  font-variant-numeric: tabular-nums;
}
.readout small {
  display: block; margin-top: 5px;
  font-size: 12px; letter-spacing: var(--track-label);
  text-transform: uppercase; color: var(--ink-faint);
}

.subreads { margin-top: 15px; padding-top: 11px; border-top: 1px solid var(--seam); display: grid; gap: 5px; }
.rd { display: flex; justify-content: space-between; gap: 14px; font-size: 12px; }
.rd span { color: var(--ink-faint); letter-spacing: .07em; }
.rd b { font-family: var(--font-mono); font-weight: 500; color: var(--ink-dim); font-variant-numeric: tabular-nums; }
.rd b.ours { color: var(--brass); }
```

---

## Pipe

A channel cut into the plate, filling with pressure. The inset shadow is what makes it a
channel rather than a stripe.

```css
.pipe {
  height: 5px; margin-top: 8px;
  border-radius: var(--radius-inner); overflow: hidden;
  background: var(--void);
  box-shadow: inset 0 1px 2px rgb(0 0 0 / .75);
}
.pipe i {
  display: block; height: 100%; width: 0;
  background: linear-gradient(90deg, var(--brass-lo), var(--brass));
  transition: width var(--dur-state) var(--ease);
}

/* Working: a sliding gradient, because the state is genuinely continuous. */
.st-working .pipe i {
  background: linear-gradient(90deg, var(--copper), var(--brass-hi), var(--copper));
  background-size: 200% 100%;
  animation: slide 1.15s linear infinite;
}
@keyframes slide { to { background-position: -200% 0; } }

.st-good .pipe i { background: linear-gradient(90deg, #3f6f57, var(--verdigris)); }
.st-bad  .pipe i { background: linear-gradient(90deg, #7d3226, var(--rust)); }
```

---

## Stamp

A verdict struck onto the row. Transparent background: colour carries the meaning, and a
filled pill is a plastic convention.

```css
.stamp {
  font-family: var(--font-mono);
  font-size: var(--size-label);
  letter-spacing: .16em; text-transform: uppercase;
  padding: 2px 7px; white-space: nowrap;
  border: 1px solid currentColor; border-radius: var(--radius-inner);
}

.s-verified { color: var(--verdigris); animation: thud .45s var(--ease) both; }
.s-stored   { color: var(--brass); }
.s-working  { color: var(--copper); }
.s-bad      { color: var(--rust); animation: thud .45s var(--ease) both; }

/* A stamp slams down. It settles FROM overshoot into rest; it does not spring
   past its target. See SKILL.md section 7. */
@keyframes thud {
  0%   { transform: scale(1.5) rotate(-5deg); opacity: 0; }
  100% { transform: none; opacity: 1; }
}
```

Only terminal verdicts get the thud. A stamp that animates every time the list re-renders
turns a control panel into a slot machine.

---

## Status lamp

Two kinds of lamp, and conflating them is a real mistake. Ask what the lamp is *for*.

**A liveness lamp** answers "is this thing running". Physically it is powered by the thing
it reports on, so a dead service has an unlit lamp. It glows when live, and it breathes
slowly to show the reading is fresh rather than stale.

**An alarm lamp** answers "has something gone wrong". Physically it is powered by the
alarm circuit, so it lights *because* of the fault, and it flashes to draw the eye.

```css
.lamp { display:inline-block; width:8px; height:8px; border-radius:50%; flex-shrink:0; }

/* Liveness: lit, glowing, breathing. */
.lamp-live { background: var(--verdigris); box-shadow: 0 0 10px var(--verdigris);
             animation: breathe 2s ease-in-out infinite; }
/* Degraded: lit, steady, no glow. */
.lamp-warn { background: var(--ember); }
/* Dead: unlit. A failed liveness lamp is a DARK lamp. */
.lamp-dead { background: var(--rust); }
/* Alarm: lit BY the fault, and it flashes. Use where the fault is actionable. */
.lamp-alarm { background: var(--rust); box-shadow: 0 0 7px var(--rust);
              animation: alarm 1.4s ease-in-out infinite; }
/* Never heard from. Not lit at all. See the honesty rule. */
.lamp-none { background: var(--seam-lit); }

@keyframes breathe { 0%,100% { opacity:1; box-shadow:0 0 10px var(--verdigris); } 50% { opacity:.4; box-shadow:none; } }
@keyframes alarm   { 0%,100% { opacity:1; } 50% { opacity:.35; } }

@media (prefers-reduced-motion: reduce) { .lamp-live, .lamp-alarm { animation: none; } }
```

Pick one convention per product. A board where some rows use a dead lamp and others an
alarm lamp for the same condition is worse than either.

---

## Lamp pill

For a roster: twenty statuses scanned at once, where you need a shape rather than a word.
The stamp is for a verdict on a named row; this is for a wall of them.

```css
.pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 3px 8px 3px 6px;
  border: 1px solid var(--seam); border-radius: var(--radius-inner);
  font-size: 11px; letter-spacing: .1em; text-transform: uppercase;
  color: var(--ink-dim);
  transition: border-color var(--dur-state), color var(--dur-state);
}
.pill:hover { border-color: var(--brass); color: var(--ink); }

/* Fill mixed with --inset, never with the surface, so the pill reads as
   stamped INTO the plate. Mixing with the surface lightens the backdrop and
   drops copper, rust and verdigris below AA; this keeps every token at 4.6+. */
.pill-ok   { color: var(--verdigris); background: color-mix(in srgb, var(--verdigris) var(--fill), var(--inset)); border-color: color-mix(in srgb, var(--verdigris) 30%, var(--inset)); }
.pill-warn { color: var(--ember);     background: color-mix(in srgb, var(--ember)     var(--fill), var(--inset)); border-color: color-mix(in srgb, var(--ember)     30%, var(--inset)); }
.pill-bad  { color: var(--rust);      background: color-mix(in srgb, var(--rust)      var(--fill), var(--inset)); border-color: color-mix(in srgb, var(--rust)      30%, var(--inset)); }
.pill-none { color: var(--ink-faint); background: var(--inset); }
```

`--fill` is `18%`. Raising it looks bolder and quietly breaks contrast, which is why it is
a token rather than a number you type into each rule.

---

## Overprint

A document-level verdict, rather than a row-level one. `DRAFT`, `SUPERSEDED`, `UNVERIFIED`,
`NOT FOR CIRCULATION`. One per document.

```css
.overprint {
  position: absolute; top: 14px; right: 18px;
  transform: rotate(-8deg);
  padding: 5px 10px 3px;
  border: 2px solid currentColor; border-radius: 4px;
  color: var(--rust);
  text-align: center; text-transform: uppercase;
  opacity: .82;
  /* screen blend so it reads as ink sitting ON the page rather than a box
     floating above it. This is the detail that sells it. */
  mix-blend-mode: screen;
  pointer-events: none;
}
.overprint b { display:block; font-size:15px; font-weight:700; letter-spacing:.14em; line-height:1; }
.overprint s { display:block; font-size:9px;  letter-spacing:.22em; text-decoration:none; }
```

```html
<div class="overprint" role="note">
  <s>station 18100</s><b>unverified</b><s>10 aug 2026</s>
</div>
```

---

## Chrome

The default scrollbar is the most common leak in the whole aesthetic.

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

input, textarea, select { accent-color: var(--brass); }

/* A chip meant to be copied should select in one click. */
code.chip {
  background: var(--inset); border: 1px solid var(--seam);
  border-radius: var(--radius-inner); padding: 3px 8px;
  color: var(--brass); user-select: all;
}
```

---

## Hazard tape

Only where the hazard is real: the edge of a destructive zone, a panel that writes to
production, a section holding irreversible controls.

```css
.hazard {
  height: 4px; flex-shrink: 0; opacity: .65;
  background: repeating-linear-gradient(-45deg, var(--ember) 0 12px, #1a1408 12px 24px);
}
```

One per screen at most. A hazard stripe used because it looks industrial is decoration, and
it spends a warning on nothing.

---

## Section heading marker

```css
.b-h {
  display: flex; align-items: center; gap: 10px;
  margin: 30px 0 12px; padding-bottom: 6px;
  border-bottom: 1px solid var(--seam);
  color: var(--brass);
  font-size: 15px; font-weight: 600;
  letter-spacing: .12em; text-transform: uppercase;
}
/* A lit rivet head, square-on. Cheaper than an icon and it never goes stale. */
.b-h::before {
  content: ''; width: 9px; height: 9px; flex-shrink: 0;
  background: var(--brass); transform: rotate(45deg);
  box-shadow: 0 0 6px rgb(201 162 39 / .5);
}
```

A panel header can take the same treatment as a vertical bar instead:
`::before { position:absolute; left:0; top:8px; bottom:8px; width:3px; background:var(--brass); opacity:.55 }`.

---

## Lever and switches

```css
button {
  font: inherit; font-size: 12.5px; letter-spacing: .04em; cursor: pointer;
  color: var(--ink);
  background: linear-gradient(180deg, var(--iron-3), var(--iron-2));
  border: 1px solid var(--seam-lit); border-radius: var(--radius-inner);
  padding: 8px 15px;
  box-shadow: inset 0 1px 0 rgb(240 216 145 / .09);
  transition: transform .12s var(--ease), border-color var(--dur-state),
              color var(--dur-state), background var(--dur-state);
}
button:hover  { border-color: var(--brass); color: var(--brass-hi); }
button:active { transform: translateY(1px) scale(.985); }   /* it depresses */
button:focus-visible { outline: 2px solid var(--brass); outline-offset: 2px; }

/* The primary action. One per panel at most. */
button.lever {
  background: var(--brass-plate);
  color: #241c05;
  border-color: var(--brass-lo);
  font-weight: 700;
  /* Struck into the metal rather than printed on it. */
  text-shadow: 0 1px 0 rgb(255 255 255 / .28);
}
button.lever:hover { color: #1a1404; filter: brightness(1.07); }

label.sw {
  display: inline-flex; gap: 8px; align-items: center; cursor: pointer;
  color: var(--ink-faint); font-size: 11.5px; letter-spacing: .05em;
}
label.sw input { accent-color: var(--brass); }
```

Switch labels are written as instructions to the machine in lower case:
`checksum every delivery`, `leave macOS clutter behind`. Not `Enable checksum validation`.

---

## The cog

Honest continuous motion: it turns if and only if work is in flight.

```css
.cog {
  animation: spin 9s linear infinite;
  animation-play-state: paused;
  opacity: .5;
  transition: opacity .4s;
}
body.working .cog { animation-play-state: running; opacity: 1; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (prefers-reduced-motion: reduce) { .cog { animation: none !important; } }
```

Nine seconds. A cog spinning at UI speed reads as a loading spinner; a cog spinning slowly
reads as heavy machinery under load.

---

## Ledger row

```css
.row { padding: 11px 0; border-top: 1px solid var(--seam); }
.row:first-child { border-top: none; }
.rowtop { display: flex; gap: 12px; align-items: baseline; }
.rname { flex: 1; min-width: 0; font-family: var(--font-mono); font-size: 12.5px;
         overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.rmeta { font-family: var(--font-mono); font-size: 11.5px; color: var(--ink-faint);
         white-space: nowrap; font-variant-numeric: tabular-nums; }
.why  { margin-top: 6px; font-size: 11.5px; color: var(--rust); font-family: var(--font-mono); }
.hash { margin-top: 6px; font-size: 11px; color: var(--ink-faint);
        font-family: var(--font-mono); word-break: break-all; }
```

`.why` carries the reason in the machine's own words, and it is where the diegetic
vocabulary earns its keep or falls apart. `checksums disagree, the copy on the far side was
deleted, send it again` is the machine talking. A stack trace is not.

---

## Empty state

Composed, not apologetic.

```css
.empty { text-align: center; padding: 26px 10px; color: var(--ink-faint); }
.empty svg { opacity: .35; }
.empty p { margin: 10px 0 0; font-size: 12.5px; letter-spacing: .05em; }
```

```html
<div class="empty">
  <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="#c9a227" stroke-width="1.2">
    <path d="M3 8.5 12 4l9 4.5v7L12 20l-9-4.5v-7Z"/><path d="m3 8.5 9 4.5 9-4.5M12 13v7"/>
  </svg>
  <p>Nothing stowed here yet. Drop something into the intake above.</p>
</div>
```

Thin stroke (`1.2`), brass, and one sentence naming the next action in the machine's
vocabulary. Never an illustration, never an apology, never "No data found".

---

## Absent data

```css
.no-signal {
  color: var(--ink-faint);
  font-size: var(--size-micro);
  letter-spacing: var(--track-label);
  text-transform: uppercase;
}
```

Never `0`. Never a bare dash. Never verdigris. If the probe did not answer, the panel says
so in words, and any gauge attached to it keeps its last needle position rather than
sweeping to zero, because a needle at zero is a reading.

---

## Load-in cascade

```css
.rise {
  opacity: 0; transform: translateY(10px);
  animation: rise .6s var(--ease) forwards;
  animation-delay: calc(var(--i, 0) * 80ms);
}
@keyframes rise { to { opacity: 1; transform: none; } }

@media (prefers-reduced-motion: reduce) {
  .rise { animation: none; opacity: 1; transform: none; }
  .needle { transition: none; }
}
```

Cap the index (`Math.min(idx, 8)`) when applying it to list rows, or a two hundred row
ledger takes sixteen seconds to finish arriving.
