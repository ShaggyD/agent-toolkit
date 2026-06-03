# Test Coverage Audit

A lightweight, automation-friendly technique for finding source files that have zero test coverage by cross-referencing filenames against test files.

## When to use

- Before declaring a project "done" — verify all source files have coverage
- After adding new source files — confirm tests exist for them
- During code review — identify gaps before merging
- When the user says "testing is important" and you need to prove you've checked

## The technique

```bash
# For each source file, check if any test file references its basename
for f in $(find components hooks store -name "*.ts" -o -name "*.tsx" | grep -v node_modules | grep -v __tests__ | sort); do
  basename=$(basename "$f" | sed 's/\.tsx$\|\.ts$//')
  found=$(grep -rl "$basename" __tests__/ 2>/dev/null | head -1)
  if [ -z "$found" ]; then
    echo "NO TEST: $f"
  fi
done
```

This works because test files import source files by their module name. If no test file anywhere in the `__tests__/` directory references a source file's basename, it likely has no direct test coverage.

## Limitations

- **Indirect coverage**: A source file might be tested indirectly through integration tests (e.g., `createStore.ts` is implicitly tested when hook tests use it). The script will flag these as "no test" even though they have functional coverage.
- **Name collisions**: A basename like `types` might match different files. Manually verify flagged files.
- **Shared export barrels**: An `index.ts` barrel that re-exports modules won't be imported by tests by name — tests import from the barrel path, not individual files. These get flagged but are often fine.

## Triage checklist for flagged files

| Finding | Likely action |
|---------|---------------|
| Trivial wrapper (themed-text, external-link, haptic-tab) | Low value to test — skip |
| Platform-specific stub (icon-symbol.ios.tsx, use-color-scheme.web.ts) | Skip — platform variants covered by main implementation tests |
| Mock/data file (mockData.ts) | Skip — data fixtures, not logic |
| Shared barrel export (index.ts) | Skip — re-exports, tested via consumers |
| Business logic component (ErrorBoundary, EmptyState) | **Write tests** — high value |
| Store/db factory (createPersistedStore) | **Write tests** — important for data integrity |
| Repository implementation with no dedicated test file | Check if tested in integration tests; add dedicated tests if not |

## Priority order for writing new tests

1. **Error/edge case components** (ErrorBoundary) — critical for UX
2. **UI components with complex rendering** (EmptyState, GlassCard variants)
3. **Data layer factories** (createPersistedStore, createStore) — important for state management
4. **Hooks with complex logic** (useTimer, useColorScheme variants)
5. **Trivial wrappers** — only if the user specifically asks

## Integration with SDLC-5 (Code Review)

When reviewing a PR, add this to the verification step:

```markdown
### Coverage audit
- [ ] Ran coverage audit against source files
- [ ] All high-value source files have tests
- [ ] Untested files are documented as intentionally excluded (trivial wrappers, platform stubs)
```
