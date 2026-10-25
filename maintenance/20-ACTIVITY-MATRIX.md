# Twenty Activity Maintenance Matrix

Each row maps a required activity to completed work and an inspectable artifact. PC = program comprehension, CM = change management, IA = impact analysis, RE = reverse engineering, RF = refactoring. Source work and analysis were completed with AI assistance. An actual IntelliJ walkthrough (Find Usages, static data flow, debugger and Extract Method) is recorded under evidence/intellij. Personal student rehearsal remains necessary.

| ID | Category | Activity | Completed work and evidence |
|---|---|---|---|
| COR-PC | Corrective | Program comprehension | Traced `MainApp` -> JSON storage -> `JsonUtil.readJsonFile` -> Jackson -> `Optional.of`; identified why checked recovery missed JSON null. COR-001 and null-flow diagram. |
| COR-CM | Corrective | Change management | Recorded defect, failing test, acceptance, scope, regression result and rollback. Commit 7110f09a; later helper extraction c0060abb. |
| COR-IA | Corrective | Impact analysis | Both contacts and preferences share `readJsonFile`; missing files and valid objects retain their existing behavior. COR-001 impact table and storage regression tests. |
| COR-RE | Corrective | Reverse engineering | Reconstructed decoder/exception/recovery flow in `diagrams/null-flow.dot` and PNG; Doxygen source links. |
| COR-RF | Corrective | Refactoring | Extracted `requireDocumentValue` from the corrected loading method; preserved the new error behavior; full tests and Checkstyle pass. |
| ADA-PC | Adaptive | Program comprehension | Inspected Gradle wrapper, JDK target and JavaFX classifiers; captured JDK 21 compile failure. `00-baseline-build.txt`. |
| ADA-CM | Adaptive | Change management | Defined local requirement for JDK 21 and macOS ARM64; recorded dependency/configuration changes and rollback. ADA-001; ddedfbc2. |
| ADA-IA | Adaptive | Impact analysis | Identified compiler, test JVM, packaging and native-library effects; domain/storage schemas do not change. ADA-001 impact table. |
| ADA-RE | Adaptive | Reverse engineering | Recovered Gradle -> JDK toolchain -> host classifier -> JavaFX runtime dependency path. ADA-001 and TOOL-EVIDENCE. |
| ADA-RF | Adaptive | Refactoring | Replaced twelve repeated platform dependency declarations with four modules driven by one host-classifier selection. Build and desktop launch verified on this Mac. |
| PRE-PC | Preventive | Program comprehension | Traced JSON serialization through `FileUtil.writeToFile`; direct target writes could expose a partial file. PRE-001. |
| PRE-CM | Preventive | Change management | Documented preventive hazard, acceptance criteria, injected failure, filesystem limitation and rollback. PRE-001; dd9d211b. |
| PRE-IA | Preventive | Impact analysis | Contacts and preferences both gain staged writes; disk-space, permissions and atomic-move support are affected. PRE-001 impact table. |
| PRE-RE | Preventive | Reverse engineering | Reconstructed serialize -> stage -> write -> replace -> cleanup flow. `diagrams/save-flow.dot` and PNG. |
| PRE-RF | Preventive | Refactoring | Centralized replacement in `FileUtil.writeAtomically`, with a package-private writer seam for deterministic fault injection; JsonUtil delegates. |
| PER-PC | Perfective | Program comprehension | Traced existing name search from parser to predicate, command, observable filtered list and UI. PER-001 and architecture diagram. |
| PER-CM | Perfective | Change management | Defined `find t/TAG [MORE_TAGS]...`, OR matching, exact tags, case-insensitivity, error handling and no data mutation. PER-001; 7268979e. |
| PER-IA | Perfective | Impact analysis | Parser, command predicate type, help text and filtering change; contact schema/save format remain compatible. Integration test covers normal name search and list restoration. |
| PER-RE | Perfective | Reverse engineering | Recovered command/filter relationships, parser AST and Doxygen relationships. `diagrams/architecture.dot`, `12-find-parser-ast.txt`. |
| PER-RF | Perfective | Refactoring | Generalized FindCommand from a concrete name predicate to `Predicate<Person>`, reusing execution/count/UI behavior for a separate tag policy. |

## Interpretation

All twenty rows have implementation or analysis evidence. This does not mean twenty independent features were added: each of four maintenance cases was studied using all five activities. Category boundaries are justified by the initiating problem, not by the tool name. Tests, tools, and diagrams are supporting evidence across rows.
