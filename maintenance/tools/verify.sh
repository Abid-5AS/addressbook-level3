#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../.."
export JAVA_HOME="${JAVA_HOME:-$(/usr/libexec/java_home -v 21)}"
./gradlew test checkstyleMain checkstyleTest coverage shadowJar --console=plain
