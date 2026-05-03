# 🧩 Tiler

A flexible, no-nonsense CLI tool to turn a folder of PNGs into clean, publication-ready image layouts.

Tiler supports multiple layout strategies—from strict grids to adaptive rows and dense masonry packing—while preserving aspect ratios and giving you control over ordering, styling, and output behavior.

---

## ✨ Features

- 🟦 **Grid layout** (uniform, clean)
- 📐 **Adaptive layout** (justified rows, like Google Images)
- 🧱 **Packed layout** (masonry / Pinterest-style)
- 🧬 Preserves original aspect ratios (no distortion)
- 🎨 Custom **background color** (`--background`)
- 🧩 Optional **borders between tiles** (`--border`, `--border-color`)
- 🏷️ Optional **captions** (`--caption`, `--caption-location`)
- 🔀 Shuffle or sort images (`name`, `aspect`, `area`, `random`)
- 📁 Recursive folder support
- 🕒 Automatic timestamped outputs (safe by default)
- ⚠️ Overwrite protection (with optional `--force`)

---

## 📦 Installation

```bash
pip install pillow
```

Clone the repo:

```bash
git clone https://github.com/yourusername/tiler.git
cd tiler
chmod +x tile.py
```

---

## 🚀 Usage

### Basic

```bash
python tile.py
```

---

### Input / Output

```bash
python tile.py -i input_folder -o output.png
```

---

## 🎨 Styling

### Background Color

```bash
python tile.py --background 0,0,0
python tile.py --background 255,255,255
python tile.py --background "#222222"
```

---

### Borders

```bash
python tile.py --border 2 --border-color 0,0,0
```

---

### Captions

```bash
python tile.py --caption "My Dataset" --caption-location top
```

Options:
- `top`
- `center`
- `below`

---

## 📐 Layout Modes

### Grid (default)

```bash
python tile.py --mode grid
```

### Adaptive

```bash
python tile.py --mode adaptive --max_width 1600
```

### Packed

```bash
python tile.py --mode packed --columns 5
```

---

## 🔀 Ordering

```bash
python tile.py --shuffle
python tile.py --sort aspect
python tile.py --sort area
```

---

## 📁 Recursive

```bash
python tile.py -i dataset/ --recursive
```

---

## ⚙️ Output Behavior

```bash
python tile.py --no-timestamp
python tile.py --force
```

---

## 🧠 When to Use What

- **Grid** → clean figures, papers
- **Adaptive** → balanced visual rows
- **Packed** → dense datasets

---

## 📊 Examples

```bash
# Dense dataset overview
python tile.py -i data/ --recursive --mode packed --columns 6

# Clean paper figure
python tile.py --mode adaptive --sort aspect --max_width 1800

# Styled output
python tile.py --border 2 --border-color 0,0,0 --background 240,240,240

# With caption
python tile.py --caption "Experiment Results" --caption-location top
```

---

## 🛠 Roadmap

- [ ] Per-image captions (filenames)
- [ ] Font control (size, typeface)
- [ ] JPG / mixed format support
- [ ] Saliency-aware cropping
- [ ] SVG/HTML export

---

## 🤝 Contributing

PRs welcome.

---

## 📄 License

MIT License

---

## 🧪 Origin

Built for quickly turning folders of experimental outputs into