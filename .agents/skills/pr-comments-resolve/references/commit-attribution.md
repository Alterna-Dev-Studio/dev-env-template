# Commit Attribution

Every commit you make MUST end with a `Co-Authored-By` trailer naming **the model
you are actually running as** — not a model name copied from a skill file.

Follow the consumer repository attribution policy and any active session requirement. If it requires a `Co-Authored-By` trailer, use the actual current agent/model identity and the configured address; do not copy the Claude-specific address from the source package.

Never hardcode a model name into a skill file, and never carry one forward from an
example. Spawned agents are frequently overridden to a different model than the
orchestrator, so a literal name
in a template is wrong for anyone but the one model that wrote it.
