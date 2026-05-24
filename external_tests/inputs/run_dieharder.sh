#!/usr/bin/env bash
set -euo pipefail

mkdir -p ../results/dieharder
for f in *.bin; do
  base=${f%.bin}
  dieharder -a -g 201 -f "$f" > "../results/dieharder/${base}.txt"
done
