#!/bin/bash
# Batch profile all 15 new clips
set -euo pipefail

SCRIPT_DIR="/home/aifeier/org-dev/bip/outgiving/scripts/src"
FOOTAGE_DIR="/home/aifeier/org-dev/bip/outgiving/ai-video/projects/T004-funny-video/assets/footage"
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

cd "$FOOTAGE_DIR"

for f in pexels-new-*.mp4; do
    profile="${f%.mp4}.profile.md"
    if [ -f "$profile" ]; then
        echo "SKIP: $profile exists"
        continue
    fi
    echo "=== Profiling: $f ==="
    python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from editor.profiler import profile_video
result = profile_video('$FOOTAGE_DIR/$f')
print(f'  -> {result}')
" 2>&1 | tail -1
done

echo "=== All profiling complete ==="
ls -1 pexels-new-*.profile.md 2>/dev/null | wc -l
