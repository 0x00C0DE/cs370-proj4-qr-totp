# cs370-proj4-qr-totp
CS370 project 4

This program is a Python implementation of a QR-based TOTP enrollment flow similar to Google Authenticator. It generates a QR code containing a fresh random shared secret and can also generate the matching 6-digit TOTP using that same saved secret.

## Requirements

- Python 3
- `pyqrcode`

## Setup

Create and activate a virtual environment if you want an isolated Python environment.

```bash
python -m venv env
```

Windows PowerShell:

```powershell
.\env\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source env/bin/activate
```

Install the QR dependency:

```bash
pip install pyqrcode
```

## Usage

Generate a QR code with your own issuer, username, and email:

```bash
python leebrad-MP4.py --generate-qr --issuer "ExampleApp" --username "alice" --email "alice@example.com"
```

What this does:

- Creates a new random shared secret
- Saves that secret in `totp_secret.txt`
- Writes the QR code SVG to `uri_qrcode.svg`

Generate the current OTP from the saved secret:

```bash
python leebrad-MP4.py --get-otp
```

## Notes

- Run `--generate-qr` first so the script has a saved secret to use.
- Each time you run `--generate-qr`, a brand-new secret is created.
- If you generate a new QR code, the old OTP values are no longer valid because the shared secret has changed.
- The generated `totp_secret.txt` file should be treated as sensitive data and should not be shared.

## Output Files

- `uri_qrcode.svg`: the generated QR code image
- `totp_secret.txt`: the locally saved shared secret used for OTP generation
