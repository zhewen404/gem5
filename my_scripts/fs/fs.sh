#!/bin/bash
if [ $# -lt 1 ] 
    then 
        echo using default
        sim='simsmall'
        benchmark='dedup'
        mesh=4
        baseline=1
    else
        if [ $# -eq 2 ] 
            then
                sim='simsmall'
                benchmark=$1
                mesh=8
                baseline=$2
            else
                sim=$3
                benchmark=$1
                mesh=$4
                baseline=$2
        fi
fi

let core=mesh*mesh

l1_size='32kB'
l1_assoc=4

if [ $baseline -eq 1 ] 
    then 
        l2_size='128kB'
        l2_assoc=8
    else
        l2_size='168kB'
        l2_assoc=10
fi

python3 my_scripts/fs/gen_script.py -s ${sim} -c ${core} -b ${benchmark}
echo "run script generated"
echo "gem5 results will be in my_STATS/${benchmark}_${core}_${sim}_${baseline}"

time build/X86/gem5.fast \
-d my_STATS/${benchmark}_${core}_${sim}_${baseline} \
configs/example/fs.py \
--kernel ~/.cache/gem5/x86-linux-kernel-4.19.83 \
--disk-image ~/.cache/gem5/x86-parsec \
--script /home/zhewen/repo/gem5-resources/src/parsec/gem5/my_scripts/fs/${benchmark}_${sim}_${core}.rcS \
--ruby \
--restore-with-cpu TimingSimpleCPU \
--num-cpus=${core} \
--num-dirs=4 \
--mem-size=1GB \
--num-l2caches=${core} \
--l1d_size=${l1_size} \
--l1i_size=${l1_size} \
--l1d_assoc=${l1_assoc} \
--l1i_assoc=${l1_assoc} \
--l2_size=${l2_size} \
--l2_assoc=${l2_assoc} \
--network=garnet \
--topology=MeshDirCorners_XY \
--mesh-rows=${mesh} \
--vcs-per-vnet=8 \
--router-latency=1
