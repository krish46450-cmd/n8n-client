# Dump Analyzer - Electron Desktop App

## Development

To run the app in development mode:

```bash
cd Client_App
npm install
npm run dev
```

## Building

### Windows Executable (.exe)
```bash
npm run build:win
```

### macOS Application (.dmg)
```bash
npm run build:mac
```

### Linux AppImage
```bash
npm run build:linux
```

### All Platforms
```bash
npm run build
```

Built applications will be in the `dist/` directory.

## Features

- Self-contained desktop application with embedded Flask server
- Native file dialogs for dump files and images
- Cross-platform support (Windows, macOS, Linux)
- Auto-start Flask backend on launch
- Clean shutdown handling

## Requirements

- Node.js 18+ and npm
- Python 3.8+ with all requirements installed
- All Python dependencies from requirements.txt

## Icons

To customize the app icon, replace:
- `static/icon.ico` (Windows)
- `static/icon.icns` (macOS)
- `static/icon.png` (Linux)

## Troubleshooting

If the app fails to start:
1. Ensure Python is in your PATH
2. Check that all Python dependencies are installed
3. Verify Flask app runs standalone with `python app.py`
4. Check Electron console for errors (dev mode)
