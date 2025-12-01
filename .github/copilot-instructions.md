# ABC Solfège Tool - AI Coding Agent Guide

## Project Overview
A single-file HTML educational tool that renders ABC notation music with movable-do solfège syllables and Kodály hand sign glyphs positioned **above** the staff (lyrics remain below). Supports multi-level transposition to show the same melody with different tonic notes.

## Architecture

### Single-File Design
- **File:** `solfege_viewer_v9.html` - Self-contained HTML with embedded CSS and JavaScript
- **External dependency:** ABCjs 6.4.3 (CDN-loaded) for music notation rendering
- **No build process:** Open HTML directly in browser, all code inline
- **Philosophy:** Leverage ABCjs built-in features; only build custom code for solfège/Kodály overlays

### Core Data Flow
1. Parse ABC notation → Extract pitch letters (currently regex; consider `ABCJS.parseOnly()` instead)
2. Apply transposition → Convert pitch letters to pitch classes (consider `ABCJS.strTranspose()` for ABC-to-ABC)
3. Calculate movable-do → Map transposed pitches to solfège syllables relative to new tonic
4. Render with ABCjs → Get SVG with semantic classes via `add_classes: true`
5. Cluster into systems → Group notes vertically (THRESHOLD=25px) to determine staff lines
6. Overlay annotations → Place solfège/Kodály above each system's top notehead

### Key Components

**Music Theory Engine** (lines 116-203)
- `ORIGINAL_TONIC_PC = 0` - Reference tonic (C) for movable-do calculations
- `pitchClassToSolfege()` - Maps chromatic semitones to syllables (Do=0, Re=2, Mi=4, etc.)
- `buildSolfegeSequence()` - Transposes pitch letters and generates solfège array

**System Clustering** (lines 205-267)
- `computeSystemBaselines()` - Detects multi-line staves by vertical spacing
- Returns `{ noteIndexToCluster, baselines }` with solfège/Kodály y-coordinates
- **Critical:** Baselines calculated from `minTop - offset` to position above staff

**Overlay Rendering** (lines 269-323)
- Colors noteheads with `DEGREE_COLORS` (Do=#ff3b30 red, Re=#ff9500 orange, etc.)
- Places `text.solfege-text` at `baseline.solfege` (top - 26px)
- Places `text.kodaly-text` at `baseline.kodaly` (top - 10px) using SMuFL glyphs
- **Pattern:** Always remove old overlays before re-rendering

## Development Patterns

### Leverage ABCjs Built-in Features First
**Before building custom solutions, check ABCjs documentation for:**
- **Transposition:** ABCjs 6.1+ has `ABCJS.strTranspose()` for key changes - consider using instead of manual pitch class math
- **Click listeners:** `clickListener` param in `renderAbc()` provides note element callbacks - avoid manual SVG event binding
- **Scaling:** ABCjs supports `scale` in engraver params - currently using CSS transform instead (evaluate if ABCjs native is better)
- **Parsing:** `ABCJS.parseOnly()` returns structured tune objects - may simplify pitch extraction vs regex parsing
- **Class targeting:** `add_classes: true` adds semantic classes to SVG elements - use these for styling vs manual attribute setting

**Current custom implementations to potentially replace:**
- `extractPitchLettersFromAbc()` - Could use `ABCJS.parseOnly()` tune object structure
- Manual transposition in `buildSolfegeSequence()` - Evaluate `ABCJS.strTranspose()` integration
- Direct SVG manipulation for note selection - Consider `clickListener` callback pattern

### Adding New Features
When modifying rendering behavior:
1. **First:** Search ABCjs docs/examples for relevant built-in features
2. Update config constants if needed (`DEGREE_COLORS`, `KODALY_GLYPHS`, `SCALE_LEVELS`)
3. Modify `overlaySolfegeAndKodaly()` for positioning logic
4. Test with both single-level and multi-level render modes

### ABCjs Integration Points
- **Note selectors:** Try `g.abcjs-note` first, fallback to `g.abcjs-n` (version-dependent)
- **renderAbc signature:** 4-argument `ABCJS.renderAbc(targetId, abc, {visualOptions}, {engraverParams})`
- **Engraver params currently used:** `responsive: "resize"`, `add_classes: true`, `staffwidth: 820`
- **Engraver params available but unused:** `scale` (for sizing music), `wrap` (for line breaking)
- **SVG retrieval:** `tuneObjs[0].svg` or `querySelector("svg")` as fallback
- **Return value:** Array of tune objects with `.svg` property and parsed music data
- **Re-rendering:** Call `renderAbc()` again when params change (e.g., scale adjustment)

### Styling Conventions
- **BROKEN:** Currently scales with CSS transform on `#levels-scale-wrapper` - should use ABCjs `scale` param instead
- Font: Bravura Text/Bravura for Kodály glyphs (SMuFL-compatible)
- Text positioning: `text-anchor: middle`, `dominant-baseline: auto` for centering
- Leverage ABCjs classes (`.abcjs-note`, `.abcjs-staff`, etc.) for CSS selectors

## Known Issues & Opportunities

### CRITICAL: Scaling/Responsiveness Problem
**Current broken behavior:**
- Zoom slider uses CSS `transform: scale()` on wrapper div
- **Problem 1:** Scales the entire canvas (container gets bigger/smaller), not the music itself
- **Problem 2:** When scaled up, content overflows viewport instead of reflowing to more staves
- **Root cause:** CSS transform doesn't trigger ABCjs layout recalculation

**ABCjs native solutions to investigate:**
- `scale` parameter in engraver params - changes actual note/staff sizes (currently unused)
- `staffwidth` parameter - controls when music wraps to new systems (currently fixed at 820)
- `responsive: "resize"` - may need to be combined with container width changes
- ABCjs may automatically reflow to multiple systems based on available width

**Correct approach:**
1. Remove CSS transform scaling entirely
2. Use ABCjs `scale` param in engraver params to change music size
3. Adjust container width or use responsive settings to trigger automatic reflowing
4. Re-run `renderAbc()` when scale changes (don't just apply CSS)
5. Recalculate solfège/Kodály overlays after re-render

### Planned Features (Not Yet Implemented)
**Future enhancements to consider:**
- **Chromatic solfège:** Extend `pitchClassToSolfege()` to support full chromatic syllables (currently has basic Di/Ri/Fi placeholders)
- **Fixed-do option:** Add toggle to switch between movable-do (current) and fixed-do (C always = Do regardless of key)
- **Hybrid solfège option:** Fixed-do with chromatic alterations (e.g., C=Do, C#=Di, Db=Ra) - combines fixed-do base with movable-do chromatic inflections
- **Color toggle:** Make `DEGREE_COLORS` configurable via UI checkbox (show/hide colored noteheads)
- **Playback:** Leverage ABCjs built-in `synth` for audio playback (see ABCjs audio documentation)

**Implementation notes:**
- For playback: Use `ABCJS.synth.CreateSynth()` and `renderAbc()` with `oneSvgPerLine` option for timing coordination
- For fixed-do: Modify `buildSolfegeSequence()` to skip tonic calculation, map pitch classes directly to syllables
- For hybrid solfège: Map natural notes to fixed syllables (C=Do, D=Re, etc.) but use chromatic alterations (Di/Ra/Ri/Me/etc.) for accidentals
- For chromatic: Expand `pitchClassToSolfege()` switch statement with all 12 chromatic syllables
- All toggles should trigger re-render, not just CSS changes

## Testing & Debugging

**Quick Test in Browser:**
```bash
open solfege_viewer_v9.html
```

**Key Test Cases:**
- Multi-system songs (e.g., 3+ lines) - verify system clustering
- Chromatic notes (Di, Ri, Fi) - check syllable mapping
- Toggle Kodály - ensure removal/addition doesn't break layout
- **Zoom at different sizes** - music should resize AND reflow to new systems when needed

**Common Issues:**
- Overlays not appearing: Check note group selector (inspect ABCjs version output)
- Wrong vertical position: Verify `computeSystemBaselines()` THRESHOLD value
- Missing glyphs: Ensure Bravura font loaded (check browser console)
- **Content overflows viewport:** Using CSS transform instead of ABCjs scale param

## Domain Knowledge

**Movable-Do System:**
- Tonic always becomes "Do" regardless of key
- Example: "Do on D (+2)" transposes C→D, so original C becomes Re, D becomes Do

**Kodály Hand Signs:**
- Unicode codepoints from SMuFL (U+EC40 to U+EC46)
- Each scale degree has distinct glyph representing hand position

**ABC Notation Parsing:**
- Header lines start with `[A-Za-z]:` (skip these)
- Lyric lines start with `w:` (skip these)
- Parse only pitch letters from remaining content
- Ignore `z` (rests) when building solfège sequence
