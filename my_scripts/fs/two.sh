#!/bin/bash
time build/X86/gem5.fast \
-d my_STATS/two \
configs/example/fs.py \
--kernel ~/.cache/gem5/x86-linux-kernel-4.19.83 \
--disk-image ~/.cache/gem5/x86-parsec \
--script /home/zhewen/repo/gem5-resources/src/parsec/gem5/my_scripts/fs/two.rcS \
--checkpoint-dir /home/zhewen/repo/gem5-resources/src/parsec/gem5/ckpt \
-r 1
