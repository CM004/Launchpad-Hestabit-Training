# 🧩 DAY 5 — Automation & Mini CI Pipeline

## 🎯 Learning outcomes

- Developed an automation mindset
- Implemented safeguards to prevent bad commits
- Practiced basic CI-style validation using shell, ESLint, Prettier & Husky

---

## ⚙️ Tasks & solutions

### ✅ 1. Validation script (`validate.sh`)

- Checks:
  - `src/` directory exists
  - `config.json` is valid JSON (uses `python3 -m json.tool` for simplicity)
  - Logs actions with timestamps to `logs/validate.log`
- Exits non-zero on failure, so the pipeline is blocked on errors.

Run manually:

```bash
bash validate.sh
```

![alt text](<Screenshot from 2025-11-09 19-20-52.png>)

---

### ✅ 2. ESLint + Prettier setup

- Installed dev dependencies:
  - eslint, @eslint/js, prettier, eslint-config-prettier, eslint-plugin-prettier, husky
- Configured a flat `eslint.config.js` (example rules used):
  - single quotes
  - semicolons required
  - no unused variables

Recommended npm script:

```json
"mohan-check": "bash validate.sh && eslint . --max-warnings=0 && prettier --check ."
```

If formatting fails, use Prettier `--write` to auto-fix.

![alt text](<Screenshot from 2025-11-09 19-23-19.png>)

---

### ✅ 3. Husky pre-commit hook

- Initialized Husky:

```bash
npx husky init
```

- Add a pre-commit hook (.husky/pre-commit):

```bash
#!/usr/bin/env bash
npm run mohan-check
```

Husky will run the validation + lint + format check before each commit and block commits that fail.

---

### ✅ 4. Build artifact creation

One-liner to create timestamped artifact and checksum:

```bash
TS=$(date +%Y%m%d%H%M%S)
mkdir -p artifacts
tar -czf artifacts/build-$TS.tgz src logs
sha256sum artifacts/build-$TS.tgz > artifacts/build-$TS.tgz.sha256
```

Artifact contains:

- `src/`
- `logs/`
- A SHA256 checksum file for verification

![alt text](<Screenshot from 2025-11-09 20-57-30.png>)

---

### ✅ 5. Cron job automation

Example crontab entry (runs daily at 02:00):

```
0 2 * * * cd /home/chandramohan/Desktop/Day5 && TS=$(date +\%Y\%m\%d\%H\%M\%S) && mkdir -p artifacts && tar -czf artifacts/build-$TS.tgz src logs && sha256sum artifacts/build-$TS.tgz > artifacts/build-$TS.tgz.sha256 >> artifacts/cron.log 2>&1
```

Generates nightly artifacts and logs for auditability.

![alt text](<Screenshot from 2025-11-09 21-18-56.png>)

---

## 🧠 Summary

- `validate.sh` ensures project sanity.
- ESLint + Prettier enforce consistent code style.
- Husky automates pre-commit checks (mini CI).
- Artifacts + cron add lightweight build automation and traceability.

---


