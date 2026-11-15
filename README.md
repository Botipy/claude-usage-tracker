# Claude Usage Tracker

A small Windows system tray icon showing your current Claude usage
limits (5-hour session + weekly limit), fetched from the private
endpoint of your claude.ai account. Hover over the icon to see the
percentages and the time each limit resets.

**Note:** this is not an official, documented Anthropic API — the
program queries the same endpoint used by the `Settings → Usage` page
on claude.ai. If Anthropic changes that page's structure, the program
may stop working until it is fixed.

Digit color on the icon:
- green — below 50% session usage
- yellow — 50-79%
- red — 80%+

## Project files

- `usage_tracker.py` / `usage_tracker.pyw` — the program itself (`.pyw`
  runs without a visible console window, for autostart)
- `config.example.json` — config template, safe to commit
- `config.json` — your private config with the token (never commit it,
  it is in `.gitignore`)
- `start_tracker.bat` — starts the tracker with one click, without
  opening PowerShell
- `requirements.txt` — dependency list

## Installation

**1. Install Python** (3.10+), tick "Add Python to PATH" during
installation: https://python.org/downloads

**2. Clone/download the repo and enter the folder:**
```powershell
git clone https://github.com/Botipy/claude-usage-tracker.git
cd claude-usage-tracker
```

**3. Install dependencies:**
```powershell
pip install -r requirements.txt
```

**4. Create the config file:**
```powershell
copy config.example.json config.json
```

**5. Get `sessionKey` and `org_id` from your browser:**
- Go to claude.ai and log in
- Open DevTools (`F12`) → `Application` tab (Chrome) / `Storage` (Firefox)
- `Cookies → https://claude.ai` → find `sessionKey`, copy the value
  into `config.json`
- **`org_id`**: in DevTools, open the `Network` tab, go to `Settings →
  Usage` on claude.ai, find the `usage` request in the list and check
  its `Request URL` — the part between `/organizations/` and `/usage`
  is your `org_id`; paste it into `config.json`

**Never commit `config.json`** — it contains your private session
token. The file is already in `.gitignore`.

**6. Run:**
```powershell
python usage_tracker.py
```
Or double-click `start_tracker.bat` — it runs in the background
without a console window.

The icon appears in the system tray (also check the "hidden icons"
arrow next to the clock). Hover over it to see the exact session and
weekly percentages, along with the reset time of each:

```
Session: 53% (resets 14:30)
Week: 68% (resets Mon 09:00)
```

Reset times are shown in your local time zone.

## Refreshing an expired token

`sessionKey` does not last forever — it expires on logout, password
change, or simply over time. When the icon tooltip shows
`Error 401/403: token expired...`, repeat step 5 (DevTools) and paste
a fresh token into `config.json`.

## Common error: `Expecting value: line 1 column 1 (char 0)`

It means claude.ai returned an HTML page instead of JSON — Cloudflare
blocks requests without a browser `User-Agent` header. The program
sends it since the August 2026 fix; if you see this error, you have an
old version of `usage_tracker.py` / `.pyw`.

## Autostart with Windows

1. `Win + R` → `shell:startup` → Enter
2. Create a shortcut to `start_tracker.bat` in that folder

The program will start by itself when Windows starts, with no visible
window.

## Risks / notes

- `sessionKey` gives full access to your claude.ai account, just like
  a regular login — keep `config.json` as safe as a password.
- This tool is unofficial and relies on an internal endpoint, not a
  public, documented API — it may stop working without notice on
  Anthropic's side.
