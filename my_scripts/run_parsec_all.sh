#!/bin/bash
# This script runs the configs specified in the input file

if [ $# -lt 1 ] 
    then 
        echo using default
        file_inp="/home/zhewen/repo/gem5-resources/src/parsec/gem5/my_scripts/test.txt"
        sim='simsmall'
        noc=1
        opt=0
    else
        file_inp=$1
        sim=$2
        noc=$3
        opt=$4
fi

# config noc_str
if [ $noc -eq 1 ] 
    then 
        noc_str='_noc'
    else
        noc_str=''
fi

# config binary
if [ $opt -eq 1 ] 
    then 
        binary='build/X86/gem5.opt'
    else
        binary='build/X86/gem5.debug'
fi

mkdir -p log;
logdir="./log/"
# sim="simsmall"

while IFS= read -r line; do
    dir=${logdir}${sim};
    mkdir -p ${dir}
    echo "$binary"
    time ${binary} -d my_STATS/${sim}_${line} configs/example/gem5_library/x86-parsec-benchmarks${noc_str}.py --benchmark $line --size $sim > ./log/${sim}/${line}.log &
    # time build/X86/gem5.opt -d my_STATS/${sim}_${line} configs/example/gem5_library/x86-parsec-benchmarks.py --benchmark $line --size $sim > ./log/${sim}/${line}.log &
    echo "launched $line"
done < "$file_inp"
