# SWE 4802 — AddressBook Maintenance Submission

**Student:** Md. Abid Shahriar, 210042155

**Project:** maintained se-edu AddressBook Level 3, MIT license preserved.

## Read

- [Printable report](maintenance/AddressBook_Maintenance_Report.pdf)
- [Editable report source](maintenance/REPORT.md)
- [Four maintenance records](maintenance/changes/)
- [Twenty-activity matrix](maintenance/20-ACTIVITY-MATRIX.md)
- [Tool usage and evidence](maintenance/TOOL-EVIDENCE.md)
- [Maintenance README](maintenance/README.md)

## Run and verify

```bash
maintenance/tools/run-demo.sh
maintenance/tools/verify.sh
```

These local macOS scripts select an installed Java 21 JDK unless JAVA_HOME is already set. The run script creates an isolated maintenance/demo-state directory. Java 21 was a local compatibility choice, not an instructor requirement. With a configured JDK/toolchain, the Gradle wrapper provides the build entry point.

For IntelliJ, open this project as a Gradle project and use the saved AddressBook Demo configuration, main class seedu.address.Main. Run the demo script once to create the isolated working directory before using the IDE configuration in a fresh checkout.

Recorded full verification: 245 tests pass, line coverage 77.33%, branch coverage 85.02%; main/test Checkstyle pass. See the report for scope and limitations.

## Evidence

- [Full test report](maintenance/evidence/final-tests/index.html)
- [Coverage report](maintenance/evidence/final-coverage/html/index.html)
- [PMD findings](maintenance/evidence/reproduced/pmd.txt)
- [Generated Doxygen documentation](maintenance/generated/doxygen/html/index.html)
- [Diagrams](maintenance/diagrams/)
- [Source changes](maintenance/evidence/patches/all-source-changes.patch)

The original project is credited in the upstream README and LICENSE. The preserved baseline is 56d1ffbb9cc8df72b97c112fcfdd0cac635652db. Retained outputs describe their recorded runs; untested environments and remaining findings are not presented as verified.
