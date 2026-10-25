# Tool Usage and Evidence

The listed outputs were produced against this local project. Initial implementation used terminal/editor tools. A subsequent actual IntelliJ session is saved under evidence/intellij; the student should still repeat it personally.

| Tool | Actual operation | Saved output | Interpretation and limit |
|---|---|---|---|
| IntelliJ IDEA | Find Usages, Data Flow to Here, null-value debug/step/resume, Extract Method | selected screenshots/exports under evidence/intellij and the 10 fresh-verification log | Actual IDE operations; three focused tests and fresh 245-test verification pass. Static data flow is not dynamic slicing. |
| Git | Cloned upstream; tagged baseline; recorded separate changes; exported diffs | upstream-commit.txt, commit-index.txt, patches | Traceable changes and rollback; timestamps are genuine, not proof of authorship. |
| Gradle + JDK 21 compiler | Built baseline then adapted project | 00-baseline-build.txt, 01-adaptive-tests.txt, 23-release-verification.txt | Baseline fails with invalid source release 25; maintained build succeeds using JDK 21. |
| OpenJDK 27 Gradle launcher | Forced fresh compile/test/style tasks while Java toolchain remains 21 | 16-jdk27-fresh.txt | Launcher compatibility only; does not establish application execution under a JDK 27 toolchain. |
| JUnit 5 | Full existing suite plus six new regression/integration tests | build/test-results/test and copied final-tests report | 245 cases pass. Tests exercise application behavior; no complete automated JavaFX interaction suite. |
| Checkstyle | Analyzed main and test Java source | 23-release-verification.txt, copied checkstyle reports | Both pass; stylistic conformance does not prove correctness. |
| JaCoCo | Measured test execution coverage | summary.json, final-coverage report | 77.33% full-package line coverage; 85.02% branch coverage. Untested code remains, especially UI. |
| PMD error-prone rules | Static source scan | 09-pmd-findings.txt and reproduced/pmd.txt | 29 initial findings; many are inherited. Findings are candidates, not automatically defects. An app-level System.exit warning for a J2EE rule is contextually weak for this desktop app. |
| PMD CPD | Java token clone detection at 80 and 50 tokens | 03-clones-before.txt, 05-clones-50tokens.txt | Zero groups at 80; two small groups at 50. Mostly value-object/formatting boilerplate. No unsupported claim of semantic clone classification or clone reduction. |
| Doxygen | Recovered documentation from Java source, including private members | generated/doxygen/html/index.html, Doxyfile, doxygen-warnings.txt | HTML generated; warnings retained. Documentation graphs are incomplete approximations of runtime dispatch. |
| Graphviz | Doxygen graph rendering plus three source-derived diagrams | diagrams/*.dot and *.png | Source-checked diagrams, not automatically generated CPGs. |
| JDK compiler Tree API | Parsed FindCommandParser using JavacTask and TreeScanner | AstDump.java, 12-find-parser-ast.txt | Real syntax tree; no type resolution, CFG, PDG or CPG is claimed. |
| Java Flight Recorder | Captured a 15-second recording of the running packaged app | demo.jfr, 20-jfr-summary.txt | Basic dynamic observation only. No performance improvement or representative benchmark is claimed. Original filename parsing issue is recorded in 19-jfr-start.txt; the valid recording was recovered and inspected. |
| JDK jpackage | Built Apple Silicon app image with bundled JDK runtime | generated/app/AddressBookLab.app, 14-package.txt | Local development app; no signing/notarization claim. Rebuild after source changes. |
| Native UI automation | Submitted tag search, empty tag query and list command to packaged app | ui-tag-search.png, ui-invalid-tag.png, ui-list-restored.txt | Tag query returned two expected sample contacts; invalid input gave usage; list restored normal view. Manual smoke evidence, not exhaustive UI testing. |

PMD/CPD, Doxygen and AST outputs describe their recorded scan snapshots before the final behavior-preserving parseTagQuery extraction; a new scan is not claimed. Latest tests/coverage/style and the runnable JAR do include that extraction.

## Commands to reproduce

```bash
maintenance/tools/verify.sh
maintenance/tools/analyze.sh
maintenance/tools/run-demo.sh
```

`analyze.sh` treats PMD exit status 4 as a completed run with findings. Other failures stop the script. Homebrew tools are under `/opt/homebrew/bin` on this Mac. The scripts are local macOS helpers, not cross-platform installers.

## Lab tools not claimed as used

- IntelliJ IDEA was actually used as recorded above. No Ultimate subscription purchase or activation is claimed.
- Optional Joern/Neo4j expansion was stopped before AddressBook graph analysis. Neo4j was installed and its local connectivity/version checked; the Joern Homebrew bottle was downloaded and checksum-verified, but a successful installation or graph analysis is not claimed. The temporary Neo4j service was stopped. Existing files under tools/cpg are preparatory, unexecuted queries. No AddressBook CPG/PDG/CDG artifact is claimed.
- IDA belongs to the separate compiled C/C++ reverse-engineering exercise. It was not used for this Java source maintenance case.
- jadx was an optional mobile exercise; this is a desktop Java application.
- Loguru, PySnooper, VizTracer, SnakeViz, Scalene and sys.settrace target Python. They did not analyze the Java application. JFR, debugger techniques and JaCoCo serve related purposes, without being identical substitutes.
- SonarQube was not installed or run. PMD and Checkstyle provide the static-analysis evidence in this pack.

The final-task screenshot asks for appropriate tools, not every previous lab tool. If an instructor separately requires a named tool, that requirement must be addressed explicitly; this report does not assert an exemption.
