# Skill Benchmark: skralovnik-motion-edit

**Date**: 2026-09-28T20:32:28Z
**Evals**: 1, 2 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 21% ± 13% | +0.79 |
| Time | 758.5s ± 25.6s | 583.3s ± 136.8s | +175.2s |
| Tokens | 185693 ± 385 | 139319 ± 11042 | +46374 |

Light test (28. 9. 2026): a fresh Claude, with and without the skill, made the plan, the film files
and 4 test frames (no full render) for two tasks: (1) the original brief on day.mp4 (the v3 footage),
(2) a 4-shot teaser (Train, Run, Recover, Repeat). With the skill both landed on the v3 style on the
first try; without it both made a different look (graded footage, permanent titles, no scans).
Note: both tasks used the v3 footage, so a test on genuinely new footage is still open.
See comparison.jpg and evals.json (prompts + assertions).
