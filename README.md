# Claude Usage Tracker

Mała ikona w zasobniku systemowym Windows pokazująca aktualne zużycie
limitu Claude (sesja 5-godzinna + limit tygodniowy), pobierana z
prywatnego endpointu Twojego konta claude.ai.

**Uwaga:** to nie jest oficjalne, udokumentowane API Anthropic —
program odpytuje ten sam endpoint, którego używa strona `Settings →
Usage` na claude.ai. Jeśli Anthropic zmieni strukturę tej strony,
program może przestać działać do czasu poprawki.

Ikona pokazuje procent zużycia sesji ze znakiem `%` (np. `7%`).

Kolor cyfry na ikonie:
- zielony — poniżej 50% zużycia sesji
- żółty — 50-79%
- czerwony — 80%+

## Pliki w projekcie

- `usage_tracker.py` / `usage_tracker.pyw` — sam program (`.pyw`
  odpala się bez widocznego okna konsoli, do autostartu)
- `config.example.json` — szablon configu, bezpieczny do commitowania
- `config.json` — Twój prywatny config z tokenem (nigdy nie commituj,
  jest w `.gitignore`)
- `start_tracker.bat` — uruchamia tracker jednym kliknięciem, bez
  otwierania PowerShella
- `requirements.txt` — lista zależności

## Instalacja

**1. Zainstaluj Pythona** (3.10+), zaznacz "Add Python to PATH" przy
instalacji: https://python.org/downloads

**2. Sklonuj/pobierz repo, wejdź do folderu:**
```powershell
git clone https://github.com/Botipy/claude-usage-tracker.git
cd claude-usage-tracker
```

**3. Zainstaluj zależności:**
```powershell
pip install -r requirements.txt
```

**4. Stwórz plik configu:**
```powershell
copy config.example.json config.json
```

**5. Zdobądź `sessionKey` i `org_id` z przeglądarki:**
- Wejdź na claude.ai, zaloguj się
- Otwórz DevTools (`F12`) → zakładka `Application` (Chrome) / `Storage` (Firefox)
- `Cookies → https://claude.ai` → znajdź `sessionKey`, skopiuj wartość
  do `config.json`
- **`org_id`**: w DevTools, zakładka `Network`, wejdź w `Settings →
  Usage` na claude.ai, znajdź zapytanie `usage` na liście, sprawdź
  `Request URL` — fragment między `/organizations/` a `/usage` to
  Twój `org_id`, wklej go do `config.json`

**Nigdy nie commituj `config.json`** — zawiera Twój prywatny token
sesji. Plik jest już w `.gitignore`.

**6. Odpal:**
```powershell
python usage_tracker.py
```
Albo kliknij dwukrotnie `start_tracker.bat` — odpali się bez okna
konsoli w tle.

Ikona pojawi się w zasobniku systemowym (sprawdź też strzałkę
"ukryte ikony" obok zegara). Najedź myszką, żeby zobaczyć dokładny
procent sesji i tygodnia.

## Odświeżanie wygasłego tokena

`sessionKey` nie jest wieczny — wygasa przy wylogowaniu, zmianie
hasła, albo po prostu z czasem. Gdy tooltip ikony pokaże
`Blad 401/403: token wygasl...`, powtórz krok 5 (DevTools) i wklej
świeży token do `config.json`.

## Częsty błąd: `Expecting value: line 1 column 1 (char 0)`

Oznacza, że claude.ai zwrócił stronę HTML zamiast JSON-a — Cloudflare
blokuje zapytania bez nagłówka `User-Agent` przeglądarki. Program
wysyła go od poprawki z sierpnia 2026; jeśli widzisz ten błąd, masz
starą wersję pliku `usage_tracker.py` / `.pyw`.

## Autostart z Windows

1. `Win + R` → `shell:startup` → Enter
2. Stwórz w tym folderze skrót do `start_tracker.bat`

Program odpali się sam przy starcie Windows, bez widocznego okna.

## Ryzyko / uwagi

- `sessionKey` daje pełny dostęp do Twojego konta claude.ai jak
  zwykłe zalogowanie — trzymaj `config.json` tak samo bezpiecznie
  jak hasło.
- To narzędzie nieoficjalne, oparte o wewnętrzny endpoint, nie
  publiczne, udokumentowane API — może przestać działać bez
  zapowiedzi po stronie Anthropic.
