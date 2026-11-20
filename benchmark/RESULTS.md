# Benchmark results

**Not run.** There are no results yet, neither positive nor negative.

The benchmark compares three setups on the same scenarios:
- an agent with its own compaction only;
- an agent with a well-kept notes file, git and grep;
- an agent with this engine.

It was designed and pre-registered before any run: scenarios, gold answers and the go/no-go thresholds are in
[PROTOCOL.md](PROTOCOL.md), with the fixtures beside it. It was not run because it needs a Claude Code plan for
all three setups, and the project had none (ADAM issue
[#57](https://github.com/AdamMostofi/ADAM/issues/57), closed as not possible). Nothing in the protocol was
changed afterwards.

**What has been measured** comes from the engine's test suite and its stage evidence, not from this benchmark:
- hook latency through the session server: p50 36–39 ms, p95 103–150 ms, replaying real Claude Code sessions;
- recall on prompts that share no words with the records they need: 20% to 80% on a test fixture;
- the cost of the tool definitions: about 1,224 estimated tokens.

These are not evidence that the engine reduces stale-state errors. That is the claim the benchmark exists to
test.

A later run, for example in OpenCode with free models, would record the change of agent and model as a
deviation in PROTOCOL.md before its first run.
