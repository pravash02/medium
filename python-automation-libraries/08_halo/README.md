# 08 — Halo: Terminal Spinners for Long-Running Tasks

Halo adds elegant terminal spinners to automation scripts — giving
users visual feedback during long operations instead of a frozen terminal.

## Run the Examples

```bash
python basic_spinner.py
python pipeline_with_spinner.py
```

## Key Concepts

- `Halo(text="...", spinner="dots")` — creates a spinner instance
- Use as context manager: `with Halo(...):` — auto-stops on exit
- `.succeed(text)` — stops spinner with ✔ green checkmark
- `.fail(text)` — stops spinner with ✖ red X
- `.warn(text)` — stops spinner with ⚠ yellow warning
- `.info(text)` — stops spinner with ℹ blue info

## Available Spinners

Over 60 built-in styles. Popular ones:
`dots`, `dots2`, `arc`, `star`, `bounce`, `pipe`, `simpleDots`,
`line`, `growHorizontal`, `weather`, `clock`

Preview all: https://jsfiddle.net/sindresorhus/2eLtsbey/embedded/result/
