#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../.."
project_dir="$PWD"
export JAVA_HOME="${JAVA_HOME:-$(/usr/libexec/java_home -v 21)}"
./gradlew shadowJar --console=plain
# Keep demo data separate from any normal AddressBook installation.
mkdir -p maintenance/demo-state
cd maintenance/demo-state
exec "$JAVA_HOME/bin/java" -jar "$project_dir/build/libs/addressbook.jar"
