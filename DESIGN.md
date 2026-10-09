---
name: Reprise
description: An engineer's reference card for one question, told along a single logarithmic ruler of time.
colors:
  ground: "#f6f7f8"
  ground-recessed: "#eceef1"
  ink: "#0f1720"
  ink-secondary: "#465160"
  ink-tertiary: "#687280"
  rule: "#d5dae0"
  rule-strong: "#b9c0c9"
  tier-hbm: "#104281"
  tier-dram: "#256abf"
  tier-ssd: "#4f93e5"
  tier-hdd: "#8fbcf1"
  recompute-amber: "#c27700"
  recompute-amber-ink: "#8a5300"
  recompute-field: "#f4e2bd"
  verdict-good: "#147a52"
  verdict-good-bg: "#dcefe6"
  verdict-bad: "#b3392a"
  verdict-bad-bg: "#f6dedb"
  selection: "#cfe0f7"
  dark-ground: "#0c1016"
  dark-ground-recessed: "#141a22"
  dark-ink: "#e9eef3"
  dark-ink-secondary: "#b2bcc8"
  dark-ink-tertiary: "#8b96a3"
  dark-rule: "#262e39"
  dark-rule-strong: "#3a4552"
  dark-tier-hbm: "#b7d3f6"
  dark-tier-dram: "#7fb0ee"
  dark-tier-ssd: "#4a8be0"
  dark-tier-hdd: "#2b62ad"
  dark-recompute-amber: "#f0a73a"
  dark-recompute-amber-ink: "#f5c27a"
  dark-recompute-field: "#3a2c14"
  dark-verdict-good: "#5ccf98"
  dark-verdict-good-bg: "#12301f"
  dark-verdict-bad: "#ff8a7a"
  dark-verdict-bad-bg: "#3a1915"
  dark-selection: "#24426b"
typography:
  display:
    fontFamily: "Red Hat Display, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(32px, 5.4vw, 64px)"
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Red Hat Display, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(24px, 2.6vw, 32px)"
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Red Hat Display, ui-sans-serif, system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: 700
  wordmark:
    fontFamily: "Red Hat Display, ui-sans-serif, system-ui, sans-serif"
    fontSize: "20px"
    fontWeight: 900
    lineHeight: 1
    letterSpacing: "-0.01em"
  lede:
    fontFamily: "Red Hat Text, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(17px, 1.7vw, 20px)"
    fontWeight: 400
    lineHeight: 1.5
  body:
    fontFamily: "Red Hat Text, ui-sans-serif, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Red Hat Text, ui-sans-serif, system-ui, sans-serif"
    fontSize: "13.5px"
    fontWeight: 600
  numeral:
    fontFamily: "Red Hat Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "13px"
    fontWeight: 500
    fontFeature: "\"tnum\""
  table-head:
    fontFamily: "Red Hat Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "12px"
    fontWeight: 600
    letterSpacing: "0.03em"
rounded:
  hairline: "2px"
  tag: "3px"
  chip: "4px"
  readout: "6px"
  pill: "999px"
spacing:
  page-inline: "clamp(16px, 4vw, 48px)"
  page-max: "1240px"
  chapter-block: "clamp(40px, 6vw, 72px)"
  chapter-gap: "clamp(20px, 4vw, 56px)"
  lane-row: "30px"
  axis: "46px"
  cell: "11px 10px"
components:
  segmented-control:
    backgroundColor: "{colors.ground}"
    rounded: "{rounded.pill}"
    padding: "3px"
  segmented-option:
    textColor: "{colors.ink-secondary}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "7px 14px"
  segmented-option-pressed:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ground}"
  select-pill:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "7px 30px 7px 14px"
  verdict-holds:
    backgroundColor: "{colors.verdict-good-bg}"
    textColor: "{colors.verdict-good}"
    rounded: "{rounded.chip}"
    padding: "2px 7px"
  verdict-limits:
    backgroundColor: "{colors.recompute-field}"
    textColor: "{colors.recompute-amber-ink}"
    rounded: "{rounded.chip}"
    padding: "2px 7px"
  verdict-fails:
    backgroundColor: "{colors.verdict-bad-bg}"
    textColor: "{colors.verdict-bad}"
    rounded: "{rounded.chip}"
    padding: "2px 7px"
  wear-flag-ok:
    backgroundColor: "{colors.verdict-good-bg}"
    textColor: "{colors.verdict-good}"
    rounded: "{rounded.chip}"
    padding: "2px 7px"
  wear-flag-over:
    backgroundColor: "{colors.verdict-bad-bg}"
    textColor: "{colors.verdict-bad}"
    rounded: "{rounded.chip}"
    padding: "2px 7px"
  table-header:
    textColor: "{colors.ink-tertiary}"
    typography: "{typography.table-head}"
    padding: "0 10px 10px"
  table-row-current:
    backgroundColor: "{colors.ground-recessed}"
  ruler-readout:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ground}"
    rounded: "{rounded.readout}"
    padding: "7px 10px"
---

# Design System: Reprise

## Overview

**Creative North Star: "The Reference Card"**

Reprise reads like an engineer's laminated reference card: a cool white ground, deep ink rules and ticks, numerals set in mono, and a single logarithmic ruler of time that every duration on the page is measured against. Structure comes from rules, rulers and whitespace, never from boxes. The page is dense where the evidence is (ruler lanes, tables, charts) and quiet everywhere else.

Colour is functional, not decorative. Storage tiers share one blue ramp running hot (dark, fast, GPU memory) to cold (pale, slow, hard drives); recomputing is the only amber thing on the page, so the reader can see at a glance which side of the recompute band each tier lands on. Green and red appear only as verdicts. Dark mode inverts the ramp so "hot" stays the most prominent tier against a near-black ground.

The world explicitly refuses the KPI-tile dashboard grid: no cards, no stat tiles, no drop shadows on content.

**Key Characteristics:**
- One shared log time ruler (10 µs to 10 s) with major decade ticks and 2–9 minor ticks.
- Tiers encoded in one blue ramp, hot to cold; recompute is the single amber field.
- Chapters are two-column ruled sections (4fr text / 8fr figure) separated by 1px rules.
- Mono for every measured number; Red Hat Display for headings, Red Hat Text for prose.
- Flat colour everywhere; the cursor readout is the one floating surface.

## Colors

A cool, near-neutral ground and ink, one blue ramp for tiers, one amber for recomputing, and verdict green and red held in reserve.

### Primary
- **Tier Ramp, Hot to Cold** (tier-hbm, tier-dram, tier-ssd, tier-hdd): GPU memory, server memory, NVMe SSD, hard drives, in that order, from heaviest to faintest against the ground. Used for ruler dots, stacked share bars and legend keys. Server-memory blue (tier-dram) doubles as the focus-ring colour and the "reuse" marker in comparison charts.

### Secondary
- **Recompute Amber** (recompute-amber): the recompute band's edges, recompute markers and the dashed "cached but faster to recompute" outline. **Recompute Amber Ink** (recompute-amber-ink) carries amber text; **Recompute Field** (recompute-field) fills the band and the "With limits" chip.

### Tertiary
- **Verdict Green / Red** (verdict-good, verdict-bad, with their -bg tints): only for verdicts and SSD-wear flags ("within rating" / "over rating"), and red for a tier's "slower than recomputing" sub-label.

### Neutral
- **Cool Paper** (ground): page background, and the knock-out halo around markers.
- **Recessed Paper** (ground-recessed): current and hovered table rows.
- **Deep Ink** (ink): headings, the axis rule, table header rule, footer rule, pressed segment, readout surface, and policy markers.
- **Slate Ink** (ink-secondary) and **Grey Ink** (ink-tertiary): lede and supporting prose; captions, axis labels, sub-values, table headers.
- **Hairline** (rule) and **Strong Hairline** (rule-strong): chapter dividers and row rules; control borders, dotted lane guides, link underlines.

### Named Rules
**The One Amber Rule.** Amber means recomputing and nothing else. A second amber meaning breaks the page's core comparison.

**The Ramp Order Rule.** Tier colour follows physical distance: hotter tier, more saturated weight (darker in light mode, lighter in dark mode). Never assign tier colours out of ramp order.

**The Label-Beside-Colour Rule.** A tier or policy colour never stands alone: every dot carries a side label, every bar a row label and legend. The cold end of the ramp is too light to be the only cue.

## Typography

**Display Font:** Red Hat Display (with ui-sans-serif, system-ui)
**Body Font:** Red Hat Text (with ui-sans-serif, system-ui)
**Label/Mono Font:** Red Hat Mono (with ui-monospace, SFMono-Regular, Menlo)

**Character:** One superfamily in three cuts: Display for tight, heavy headings, Text for readable prose, Mono for anything that was measured. It reads like a well-set spec sheet.

### Hierarchy
- **Display** (700, clamp 32–64px, 1.02, -0.03em): the page question only; max 18ch, balanced.
- **Headline** (700, clamp 24–32px, 1.12, -0.02em): chapter titles, balanced.
- **Title** (700, 18px): fact headings inside the method chapter.
- **Wordmark** (900, 20px): "Reprise" in the masthead, with a 14px Text descriptor in ink-tertiary.
- **Lede** (400, clamp 17–20px, 1.5): the one-sentence answer, max 62ch; bold spans in ink at 600.
- **Body** (400, 16px, 1.6): chapter leads at max 46ch (70ch on full-width chapters); findings at 15.5px, max 78ch; captions at 13–14px in ink-tertiary.
- **Label** (600, 13.5px Text): lane tags, track labels, chart row labels.
- **Numeral** (500, 12–14px Mono, tabular): axis labels, timings, table values, percentages.
- **Table Head** (600, 12px Mono, uppercase, 0.03em): column headings.

### Named Rules
**The Measured-in-Mono Rule.** Every number that came out of the simulation is set in Red Hat Mono with tabular figures. Prose numbers inside sentences may stay in Text, bolded.

## Layout

A single 1240px column with fluid inline padding (16–48px). The first viewport stacks masthead (wordmark left, two text links right, 1px rule under), the question, the answer, one row of controls, then the full-width ruler.

The ruler is a vertical stack around one 2px ink axis: a block lane above (one 30px row per tier: dot at its true log position, label on whichever side has room, a dotted guide), the axis with decade labels, and a request lane below (one row per caching policy). The recompute band is a full-height amber field spanning both lanes. Below 560px, odd decade labels drop, rows grow to 44px and sub-values wrap under their labels.

Chapters below are two-column grids (minmax 4fr text / 8fr figure), separated by a 1px rule with 40–72px block padding. A chapter whose figure needs width (the matrix) goes single-column. Below 860px every chapter stacks. Method facts sit in a two-column grid (28px / 40px gap) that stacks on narrow screens. The footer is closed by a 2px ink rule.

## Elevation & Depth

Flat. Depth comes from rule weight (1px hairline, 2px ink) and the recessed-paper row tint, not shadows. Markers use a 3px ground-coloured halo (`box-shadow: 0 0 0 3px var(--bg)`) to knock out the rules beneath them; this is a cutout, not elevation.

### Shadow Vocabulary
- **Readout lift** (`box-shadow: 0 6px 18px rgba(15,23,32,.18)`): the cursor readout only, the one element that floats over the ruler.

### Named Rules
**The Rules-Not-Boxes Rule.** Group with rules and whitespace. No cards, panels or tiles around content.

## Shapes

Mostly square. Rules and ticks are hard lines; table cells and chapters have no corners at all. Rounding is small and functional: 2px on chart bars, 3px on lane tags and the focus ring, 4px on chips and flags, 6px on the readout. Controls are the only fully round shapes (999px pills), and markers are 14px circles. Dashed and dotted strokes carry meaning: dashed for limits and "could have reused", dotted for lane guides.

## Components

### Segmented Control and Select
Quiet pills that only gain weight when chosen.
- **Shape:** fully round (999px), 1px strong-hairline border, 3px inner padding.
- **Options:** 14px Text 500 in ink-secondary; hover to ink. Pressed option fills Deep Ink with ground text (`aria-pressed`). 0.2s background/colour transition.
- **Select:** same pill and border, a CSS-drawn chevron in ink-secondary, a Text label in ink-tertiary beside it.
- **Focus:** 2px tier-dram outline, 3px offset, site-wide.

### Verdict Chips
- **Style:** 11.5px Mono 600, uppercase, 0.04em, 2px 7px padding, 4px radius, tint background with matching ink.
- **Variants:** Holds (green), With limits (amber field / amber ink), Doesn't hold (red). They lead each finding line; the bold claim follows.

### Wear Flags
Table-cell values in 12px Mono 600 on the same green/red tints and 4px radius: green when drive-writes per day are within rating, red when over.

### Tables
- 14px Text, values right-aligned in tabular Mono, first column left-aligned and flush.
- Header: 12px Mono uppercase in ink-tertiary over a **2px ink rule**; rows divided by 1px hairlines, 11px 10px cells.
- Selectable rows tint to recessed paper on hover and when current; Enter/Space selects. Low-priority columns hide under 560px.

### The Time Ruler (signature)
One logarithmic axis, 10 µs to 10 s, shared by both ruler lanes in the first viewport. 2px ink baseline; 14px major ticks per decade, 7px grey minor ticks; Mono decade labels. Tier and policy rows place a 14px dot at the true position with a 13.5px Text label and Mono sub-value on the roomier side. Recompute uses an amber marker; the theoretical limit is a hollow ghost dot. Markers slide 0.7s on `cubic-bezier(.16,1,.3,1)` when workload or cluster changes.

### Cursor Readout
A 1px dashed ink-secondary line follows the pointer (tap pins it, arrow keys step a tenth of a decade). The readout is an ink tooltip, 12.5px Text with the time in Mono, max 300px, clamped inside the ruler.

### Charts
Inline SVG on the same ground: hairline gridlines (dashed for minor), Mono axis labels, Text row labels, Mono values at bar ends. Recompute-versus-reuse rows are amber dot to dram-blue dot with an ink-secondary arrow. Each chart carries a square-swatch legend (12px, 3px radius).

### Navigation
Masthead text links in 14px ink-secondary, underline in strong hairline that darkens to currentColor on hover; hidden under 560px.

## Do's and Don'ts

### Do:
- **Do** place first-viewport durations on the one shared log ruler, at their true position.
- **Do** keep tiers in the hot-to-cold blue ramp and recompute in amber, in both themes.
- **Do** label every coloured mark in text beside it.
- **Do** set measured numbers in Red Hat Mono with tabular figures.
- **Do** separate chapters with a 1px rule and close tables and the page with a 2px ink rule.
- **Do** honour `prefers-reduced-motion` by removing all transitions.

### Don't:
- **Don't** build KPI tiles, cards or boxed panels; structure is rules and whitespace.
- **Don't** use amber for anything but recomputing, or green and red for anything but verdicts and wear.
- **Don't** give a second element the readout's shadow; content stays flat.
- **Don't** draw a duration on a linear scale; a zoomed chart may narrow the log range (the cached-share chart runs 10 ms to 5 s) but stays logarithmic.
