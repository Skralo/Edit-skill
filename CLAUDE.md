# Edit-skill

This repo holds the `skralovnik-motion-edit` skill (`.claude/skills/skralovnik-motion-edit/`), its
working template, Anže's brand and elements, and the approved SKRALOVNIK v3 as a reference example.

- For any video-edit request, follow the skill: read `SKILL.md`, then `references/process.md`.
- Talk to Anže in Slovenian, in plain words. Start every session with a popup (AskUserQuestion),
  explain each question and what each answer changes (`references/questions.md`).
- Ask before anything not done with him before (new service, storing his files somewhere new,
  pushing to another repo, paid generation).
- Films are made in their own folder or repo from a copy of `template/`; do not edit the template's
  v3 defaults unless improving the engine itself, and then re-verify against
  `examples/skralovnik-v3/` (frames and soundtrack must stay identical, or say what changed and why).
- When a new version is approved, update `references/feedback-log.md` with his words, the affected
  reference files, and repackage: `python -m scripts.package_skill .claude/skills/skralovnik-motion-edit dist/`
  (from the skill-creator skill) or zip the folder as `dist/skralovnik-motion-edit.skill`.
- Never include model names in commits or files.
