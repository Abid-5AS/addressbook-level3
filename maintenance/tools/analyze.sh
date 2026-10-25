#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../.."
export JAVA_HOME="${JAVA_HOME:-$(/usr/libexec/java_home -v 21)}"
mkdir -p maintenance/generated/doxygen maintenance/evidence/reproduced
# PMD exit 4 means findings, not a tool failure.
run_pmd() {
  local result=0
  /opt/homebrew/bin/pmd "$@" || result=$?
  if [ "$result" -ne 0 ] && [ "$result" -ne 4 ]; then return "$result"; fi
}
run_pmd cpd --minimum-tokens 50 --dir src/main/java --language java --format text > maintenance/evidence/reproduced/clones.txt 2>&1
run_pmd check --dir src/main/java --rulesets category/java/errorprone.xml --format text --no-cache > maintenance/evidence/reproduced/pmd.txt 2>&1
/opt/homebrew/bin/doxygen maintenance/tools/Doxyfile > maintenance/evidence/reproduced/doxygen.txt 2>&1
"$JAVA_HOME/bin/java" maintenance/tools/AstDump.java src/main/java/seedu/address/logic/parser/FindCommandParser.java > maintenance/evidence/reproduced/ast.txt
for diagram in maintenance/diagrams/*.dot; do
  /opt/homebrew/bin/dot -Tpng "$diagram" -o "${diagram%.dot}.png"
done
