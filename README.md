# ABC Solfège Tool

A single-file HTML educational tool that renders ABC notation music with movable-do solfège syllables and Kodály hand sign glyphs positioned above the staff.

![Demo Screenshot](docs/screenshot.png)

## Features

- **Movable-Do Solfège**: Automatically displays solfège syllables (Do, Re, Mi, etc.) above each note
- **Kodály Hand Signs**: Shows SMuFL glyphs representing hand positions for each scale degree
- **Multi-Level Transposition**: View the same melody with different tonic notes (e.g., "Do on C", "Do on D", "Do on F")
- **Color-Coded Notes**: Each scale degree is highlighted with a distinct color
- **Lyrics Support**: Original ABC lyrics remain below the staff
- **Zero Dependencies**: Single HTML file - just open in a browser

## Quick Start

1. Download `solfege_viewer_v9.html`
2. Open it in any modern web browser
3. Paste your ABC notation into the text area
4. Click "Render Single Level" or "Render Multi-Level"

Example ABC notation (included by default):
```abc
X:1
T:Twinkle Twinkle
M:4/4
L:1/4
K:C
C C G G | A A G2 |
F F E E | D D C2 |
w: Twin- kle, twin- kle, lit- tle star,
w: How I won- der what you are.
```

## Technology

Built with [ABCjs 6.4.3](https://paulrosen.github.io/abcjs/) for music notation rendering. All solfège and Kodály annotations are custom SVG overlays positioned above the staff using intelligent system clustering.

### Architecture
- **Single-file design**: No build process, no installation required
- **Leverages ABCjs features**: Uses built-in rendering, class annotations, and responsive sizing
- **Custom overlays only**: Only builds custom code for solfège/Kodály positioning—everything else uses ABCjs

## Controls

- **Zoom**: Adjust the display size (0.5x - 3x)
- **Show Kodály signs**: Toggle hand sign glyphs on/off
- **Render Single Level**: Shows music in one key
- **Render Multi-Level**: Shows the same melody transposed to C, D, and F

## Music Theory

### Movable-Do System
In movable-do solfège, the tonic (first scale degree) is always "Do" regardless of the key. For example:
- In C major: C=Do, D=Re, E=Mi, F=Fa, G=So, A=La, B=Ti
- In D major: D=Do, E=Re, F#=Mi, G=Fa, A=So, B=La, C#=Ti

### Kodály Hand Signs
Each scale degree has a distinctive hand position:
- **Do**: Fist at waist
- **Re**: Hand angled upward
- **Mi**: Flat hand, palm down
- **Fa**: Thumb down
- **So**: Flat hand waving
- **La**: Hanging hand
- **Ti**: Pointed finger upward

## Known Limitations

- **Scaling/Responsiveness**: Currently uses CSS transform which scales the container instead of the music itself. Future versions will use ABCjs native `scale` parameter for proper reflowing to multiple systems.
- **Chromatic Notes**: Basic support for Di, Ri, Fi with placeholders. Full chromatic solfège coming soon.

## Planned Features

- Full chromatic solfège syllables
- Fixed-do option (C always = Do)
- Hybrid solfège (fixed-do with chromatic alterations)
- Toggle for colored noteheads
- Audio playback using ABCjs synth

## Contributing

This is an educational tool designed for music teachers and students. Contributions welcome!

See `.github/copilot-instructions.md` for development guidance.

## License

MIT License - feel free to use in your music education projects!

## Credits

- Built with [ABCjs](https://paulrosen.github.io/abcjs/) by Paul Rosen
- Kodály glyphs from [SMuFL](https://www.smufl.org/) (Bravura font)
- Movable-do solfège system from the Kodály Method
