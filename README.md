# Password Generator (CustomTkinter)

Desktop Python app to generate strong passwords with a modern UI and Spanish/English language support.

## Requirements

- Python 3.10+
- uv (recommended) or pip
- Local virtual environment in `venv/`

## Run Locally (always in venv)

```bash
source venv/bin/activate
uv sync
python main.py
```

## Build a Local Executable (multi-platform)

Build must run on each target OS:

- Linux -> Linux binary
- macOS -> macOS app/binary
- Windows -> `.exe`

Command:

```bash
source venv/bin/activate
uv sync --extra build
uv run pyinstaller --noconfirm --onefile --windowed --name password-generator main.py
```

Output is generated in `dist/`.

## Build Locally for Ubuntu 22.04 with Docker

If you want a Linux binary compatible from Ubuntu 22.04 onward, use the local script:

```bash
./scripts/build_ubuntu22_local.sh
```

The executable is generated at:

- `dist/ubuntu22/password-generator-ubuntu22`

## GitHub Actions

The workflow in `.github/workflows/build.yml` builds automatically on:

- ubuntu-22.04
- windows-latest
- macos-latest

Each build uploads a downloadable artifact with the executable.

Linux note:
The Linux binary is built on Ubuntu 22.04 to maximize compatibility for Ubuntu 22.04+ systems.
