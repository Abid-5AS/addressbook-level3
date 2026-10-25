# AddressBook Maintenance — Submission Files

This maintained fork demonstrates four changes: Java/toolchain and host-native JavaFX adaptation, JSON-null loading correction, staged atomic JSON saving, and tag-based search.

## Report and records

- [Printable report](AddressBook_Maintenance_Report.pdf)
- [Report source](REPORT.md)
- [Activity matrix](20-ACTIVITY-MATRIX.md)
- [Change records](changes/)
- [Tool evidence](TOOL-EVIDENCE.md)

## Supporting material

- evidence/: selected before/after logs, frozen test/style/coverage reports, static findings, IDE evidence, original source and patches.
- diagrams/: editable DOT sources and rendered PNG diagrams.
- generated/doxygen/: local generated HTML documentation, retained in the submission export.
- tools/: verification, analysis, launch, report-rendering and packaging scripts.
- assets/: cover logo used by the printable report.

## Reproduction

From the repository root:

```bash
maintenance/tools/verify.sh
maintenance/tools/analyze.sh
maintenance/tools/run-demo.sh
```

The recorded setup is macOS ARM64 with a Java 21 application toolchain. Analysis reproduction additionally uses local PMD/CPD, Doxygen and Graphviz. Other platforms were not verified. The Main launcher is required for the prepared non-modular JavaFX run configuration.

Final recorded result: 245 tests pass; 921/1191 lines (77.33%) and 278/327 branches (85.02%) covered. Source/style checks pass. Initial static/documentation findings remain; see TOOL-EVIDENCE.md for interpretation and scan-snapshot boundaries.

The baseline tag/original-source archive identifies revision 56d1ffbb9cc8df72b97c112fcfdd0cac635652db. The latest full source-verification log is evidence/intellij/10-refactor-fresh-verification.txt. The later 11 log records the corrected IntelliJ Main launcher.

## Submission packaging

The clean export uses an explicit allowlist rather than every tracked file. Personal preparation, notes, handoffs, optional CPG setup, machine state, tool downloads, raw JFR and local Git history are excluded. The source/evidence manifest verifies the contents of the submission archive.
