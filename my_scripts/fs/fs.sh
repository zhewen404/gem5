#!/bin/bash

l1_size='32kB'
l1_assoc=4
l2_size='128kB'
l2_assoc=8

# -d $out_dir/${benchmark}_${num_cores}c_${inp}_w${work_items}_${cfg} \


time build/X86/gem5.opt \
-d my_STATS/dedup_16_simsmall \
configs/example/fs.py \
--kernel ~/.cache/gem5/x86-linux-kernel-4.19.83 \
--disk-image ~/.cache/gem5/x86-parsec \
--script /home/zhewen/repo/gem5-resources/src/parsec/gem5/my_scripts/fs/run.rcS \
--ruby \
--restore-with-cpu TimingSimpleCPU \
--num-cpus=16 \
--num-dirs=4 \
--mem-size=1GB \
--num-l2caches=16 \
--l1d_size=${l1_size} \
--l1i_size=${l1_size} \
--l1d_assoc=${l1_assoc} \
--l1i_assoc=${l1_assoc} \
--l2_size=${l2_size} \
--l2_assoc=${l2_assoc} \
--network=garnet \
--topology=MeshDirCorners_XY \
--mesh-rows=4 \
--vcs-per-vnet=8 \
--router-latency=1
