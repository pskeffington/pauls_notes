# Scholarly Literature Matrix: Agentic Templating, Skills, and Best Practices

**Scope:** Research supporting reusable agent skills, tool integration, planning, retrieval, evaluation, and security.  
**Reviewed:** 2026-10-31. **Evidence rule:** Publications below are external research; suggested adoption is an engineering inference, not a result measured in this repository.

## Matrix

| ID | Authors / year | Publication and venue | Method / contribution | Limitations / transfer risks | Implication for Paul's Notes |
| --- | --- | --- | --- | --- | --- |
| AG-LIT-01 | Yao, Zhao, Yu, Du, Shafran, Narasimhan & Cao (2023) | [ReAct: Synergizing Reasoning and Acting in Language Models](https://mlanthology.org/iclr/2023/yao2023iclr-react/), ICLR | Interleaved reasoning and external actions | Tool behavior and reliability depend on environment and model | Define observable plan/action/result records; do not require exposure of private internal reasoning |
| AG-LIT-02 | Schick, Dwivedi-Yu, Dessì, Raileanu et al. (2023) | [Toolformer: Language Models Can Teach Themselves to Use Tools](https://proceedings.neurips.cc/paper_files/paper/2023/file/d842425e4bf79ba039352da0f658a906-Paper-Conference.pdf), NeurIPS | Self-supervised tool/API use | Training approach does not establish safety or portability for arbitrary tools | Explicit tool signatures, arguments, permission checks and tool-result validation |
| AG-LIT-03 | Wang, Xie, Jiang, Mandlekar et al. (2023) | [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291), arXiv preprint | Executable skill library, curriculum and iterative feedback | Minecraft-specific evaluation; not proof of software-development or general-model robustness | Versioned atomic skills; catalog, retrieval and composability fixtures |
| AG-LIT-04 | Khattab, Singhvi, Maheshwari, Zhang et al. (2024) | [DSPy: Compiling Declarative Language Model Calls into State-of-the-Art Pipelines](https://proceedings.iclr.cc/paper_files/paper/2024/hash/f1cf02ce09757f57c3b93c0db83181e0-Abstract-Conference.html), ICLR | Declarative modules with metric-driven prompt/pipeline optimization | Gains depend on datasets, objectives and studied models | Separate task specifications from prompt rendering; evaluate optimizer changes on held-out fixtures |
| AG-LIT-05 | Lewis, Perez, Piktus, Petroni et al. (2020) | [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html), NeurIPS | Retrieval-backed generation using external non-parametric memory | Evidence retrieval can be incomplete, stale or misleading | Stable source identifiers, provenance, retrieval diagnostics and citations |
| AG-LIT-06 | Shinn, Cassano, Gopinath, Narasimhan & Yao (2023) | [Reflexion: Language Agents with Verbal Reinforcement Learning](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html), NeurIPS | Reflective feedback reused on subsequent attempts | Feedback can be wrong; retries can compound errors or cost | Bounded retries, failure taxonomies, independent verification and escalation |
| AG-LIT-07 | Jimenez, Yang, Wettig, Yao, Pei, Press & Narasimhan (2024) | [SWE-bench: Can Language Models Resolve Real-world Github Issues?](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html), ICLR | Real-world issue resolution evaluated with execution-based tests | Dataset, environment and test coverage limit generalizability; historical benchmark scores are not current scores | Repo-specific regression suite, clean environment and fail-to-pass acceptance |
| AG-LIT-08 | Liu, Yu, Zhang, Xu et al. (2024) | [AgentBench: Evaluating LLMs as Agents](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html), ICLR | Multi-environment interactive agent benchmark | Different environments and models have distinct failure distributions | Model capability matrix and equivalent tasks across hosted/local runtimes |
| AG-LIT-09 | Greshake, Abdelnabi, Mishra, Endres, Holz & Fritz (2023) | [Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173), preprint | Shows instruction/data boundary attacks through retrieved material | Attack feasibility varies by architecture; mitigations require separate testing | Treat retrieval and tool output as untrusted; constrain privileges and test injection resistance |

## Synthesis and implementation priorities

1. **AG-M1 — Templates and schemas:** use typed input/output definitions, explicit capability permissions and stop criteria (AG-LIT-01, 02, 04).
2. **AG-M2 — Skill registry:** skill identity/version, eligibility rules, dependencies, examples, evaluation fixtures and provenance (AG-LIT-03, 04).
3. **AG-M3 — Retrieval:** source-level citation, freshness, relevance evaluation, no implicit authority from indexed text (AG-LIT-05, 09).
4. **AG-M4 — Evaluation:** deterministic success criteria, reproducible baseline tasks, multiple model/runtime adapters and error classification (AG-LIT-07, 08).
5. **AG-M5 — Recovery and safety:** bounded retry loops, independent gate checks, audit records and human approval for high-impact actions (AG-LIT-06, 09).

## Suggested empirical study

**Question:** Does a structured skill contract improve completion quality and reduce token/time cost compared with an unstructured prompt, across Codex and selected locally deployed models?

- Compare **baseline prompt**, **templated prompt**, and **templated prompt + retrieved skill**.
- Use identical tasks and fixed repository snapshots with independent validation; randomize task order and record model/runtime/configuration.
- Measure acceptance pass rate, unsupported claims, invalid tool calls, median wall time, tokens, memory and recovery attempts.
- Keep test-writing and grading separated where possible; pre-register criteria and retain failures rather than selectively reporting successful runs.
- Report uncertainty, sample size and environment details; do not generalize across model families without paired evidence.

## Evidence classifications

- **Peer-reviewed conference papers:** AG-LIT-01, 02, 04, 05, 06, 07, 08.
- **Preprints not represented here as peer-reviewed:** AG-LIT-03, 09.
- **Design proposals, not experimentally established findings:** AG-M1 through AG-M5 and the suggested empirical study.

**Scientific boundary:** These papers establish approaches and benchmark results in their studied settings; they do not certify any agent as production-safe or any research workflow as clinically valid.
