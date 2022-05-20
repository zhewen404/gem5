import argparse

def construct_argparser():
    parser = argparse.ArgumentParser(description='writeStats')
    parser.add_argument('-s',
                        '--sim',
                        help='sim size',
                        default='simsmall',
                        choices=['simsmall', 'simlarge', 'simmedium'],
                        )
    parser.add_argument('-b',
                        '--benchmark',
                        help='benchmark name',
                        default='dedup',
                        choices=['blackscholes', 'bodytrack', 'canneal', 'dedup', \
                            'facesim', 'ferret', 'fluidanimate', 'freqmine', 'raytrace', \
                            'streamcluster', 'swaptions', 'vips', 'x264'],
                        )
    parser.add_argument('-c',
                        '--core',
                        help='thread num',
                        default=16,
                        )
    return parser

if __name__ == "__main__":
    parser = construct_argparser()
    args = parser.parse_args()

    filename = f"my_scripts/fs/{args.benchmark}_{args.sim}_{args.core}.rcS"
    file1 = open(filename, "w") 
    string_wr = f'cd /home/gem5/parsec-benchmark;\nsource env.sh;\n' \
        f'echo "{args.benchmark} starts :)";\n' \
        f'parsecmgmt -a run -p {args.benchmark} -c gcc-hooks -i {args.sim} -n {args.core};\n' \
        f'echo "{args.benchmark} ends :)";\n' \
        f'sleep 5\n' \
        f'echo "ready to exit m5";\n' \
        f'm5 exit;'
    file1.write(string_wr)
    file1.close()
    print(f'written file {filename}')
