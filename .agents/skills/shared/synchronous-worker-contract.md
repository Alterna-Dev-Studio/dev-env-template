# Synchronous Worker Contract

When an orchestrator delegates work to a Codex subagent, it treats the joined
result as the completion of that work. The worker must:

- Wait for every subagent it starts and every command session it opens. A
  running test run or script is not completion evidence.
- Use a sufficiently long foreground command timeout for slow work (the
  unittest suite, `python3 -m unittest discover -s tests -v`). If a
  command outlives its timeout, split or rerun it and verify the final result.
- Follow the invoked skill through its defined terminal state and inspect the
  required artifacts before returning. Some skills intentionally leave an
  analysis or review result uncommitted; their own completion evidence still
  applies.
- Report what was verified, including any commit, test result, or tracker
  update. Do not report a started task as completed.

This is the Codex adaptation of
`.claude/skills/shared/synchronous-worker-contract.md`, patched for the
dev-env-template consumer.
