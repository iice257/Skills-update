# Skills Update

Reusable Codex skill for checking and updating installed skills, including copied custom skills that do not update automatically.

## What It Does

`skills-update` scans the installed Codex skills directory, resolves each skill to a known GitHub source, compares the installed files with the latest remote version, and updates changed skills when asked.

It is conservative by design:

- Dry-run by default.
- Skips `.system` skills unless explicitly included.
- Creates timestamped backups before replacing skill folders.
- Infers OpenAI curated and experimental skills by name.
- Requires source metadata for copied custom skills because copied folders do not preserve their GitHub origin.
- Supports optional daily automatic updates through Codex Automations.

## Install

Use the built-in skill installer:

```bash
python "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" --repo iice257/Skills-update --path skills/skills-update
```

On Windows PowerShell:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo iice257/Skills-update --path skills/skills-update
```

Restart Codex after installing so the new skill is picked up.

## Use

In Codex:

```text
Use $skills-update to update my installed skills.
```

On first use, the skill asks:

```text
Do you want to turn on automatic updates? This will set up an automation that runs every day. You can turn it off at any time in `Automations`.
```

If accepted, Codex creates a daily automation that runs the skill and applies safe updates.

## Direct Script Usage

From this repo or the installed skill folder:

```bash
python skills/skills-update/scripts/update_skills.py
python skills/skills-update/scripts/update_skills.py --apply
python skills/skills-update/scripts/update_skills.py --json
python skills/skills-update/scripts/update_skills.py --only frontend-skill --apply
```

## Verify

```bash
python -m py_compile skills/skills-update/scripts/update_skills.py
python -m unittest discover -s tests
python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" skills/skills-update
```

## Custom Skill Sources

For copied custom skills, add per-skill metadata at:

```text
$CODEX_HOME/skills/<skill-name>/.skills-update.json
```

Example:

```json
{
  "repo": "owner/repo",
  "path": "skills/my-skill",
  "ref": "main"
}
```

Or use global config:

```text
$CODEX_HOME/skills/.skills-update/sources.json
```

Example:

```json
{
  "skills": {
    "my-skill": {
      "repo": "owner/repo",
      "path": "skills/my-skill",
      "ref": "main"
    }
  }
}
```

You can also pass a one-off source:

```bash
python skills/skills-update/scripts/update_skills.py --source "my-skill=owner/repo:skills/my-skill@main" --apply
```

## Notes

The updater cannot safely discover the upstream for a plain copied custom skill without metadata. It reports those skills as `untracked` instead of guessing.
