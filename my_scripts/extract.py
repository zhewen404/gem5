from collections import OrderedDict
import argparse
import re
from scipy.stats import gmean

pattern_map = {
    'runtime': 'simTicks\s+\d+',
    'network_lat': 'system.ruby.network.average_packet_network_latency\s+\d+',
    'inst': 'simInsts\s+\d+',
}

prune_map = {
    'runtime': lambda line: float(line.replace(' ','').split('simTicks')[-1].split('#')[0]),
    'network_lat': lambda line: float(line.replace(' ','').split('system.ruby.network.average_packet_network_latency')[-1].split('(')[0]),
    'inst': lambda line: float(line.replace(' ','').split('simInsts')[-1].split('#')[0]),
}

# reduction_map = {
#     'ipc': lambda list_ : gmean(list_),
#     'l1d_mr': lambda list_: sum(list_) / len(list_),
#     'l2_mr': lambda list_: sum(list_) / len(list_),
#     'llc_mr': lambda list_: sum(list_) / len(list_),
# }

def construct_argparser():
    parser = argparse.ArgumentParser(description='writeStats')
    parser.add_argument('-o',
                        '--outdir',
                        nargs='+',
                        help='file to parse results',
                        default=[\

                            'my_STATS/blackscholes_64_simsmall_0/stats.txt', \
                            'my_STATS/blackscholes_64_simsmall_1/stats.txt', \
                            'my_STATS/canneal_64_simsmall_0/stats.txt', \
                            'my_STATS/canneal_64_simsmall_1/stats.txt', \
                            'my_STATS/swaptions_64_simlarge_1/stats.txt', \
                            'my_STATS/swaptions_64_simlarge_0/stats.txt', \
                            ]
                        )
    return parser

def get_list(file, metric):
    pattern = pattern_map[metric]

    list_ = []
    with open(file, 'r') as searchfile:
        for line in searchfile:
            if re.match(pattern, line):
                prune_func = prune_map[metric]
                res = prune_func(line)
                list_.append(res)
    # print(list_)
    return list_

if __name__ == "__main__":
    parser = construct_argparser()
    args = parser.parse_args()

    o_arr = [o.split('/')[1].split('_')[0] for o in args.outdir]
    print(f'benchmarks={o_arr}')

    metric = 'runtime'
    rt_list_base = [get_list(o, metric)[0] for o in args.outdir if '_1' in o]
    print(f'rt base ={rt_list_base}')
    rt_list_large = [get_list(o, metric)[0] for o in args.outdir if '_0' in o]
    print(f'rt large={rt_list_large}')

    rt_norm = [l / b for b,l in zip(rt_list_base, rt_list_large)]
    rt_norm_mean = gmean(rt_norm)
    print(f'rt (norm) ={rt_norm}\n')

    metric = 'network_lat'
    nl_list_base = [get_list(o, metric)[0] for o in args.outdir if '_1' in o]
    print(f'nl base ={nl_list_base}')
    nl_list_large = [get_list(o, metric)[0] for o in args.outdir if '_0' in o]
    print(f'nl large={nl_list_large}')
    
    nl_norm = [l / b for b,l in zip(nl_list_base, nl_list_large)]
    nl_norm_mean = gmean(nl_norm)
    print(f'nl (norm) ={nl_norm}\n')


    metric = 'inst'
    in_list_base = [get_list(o, metric)[0] for o in args.outdir if '_1' in o]
    print(f'in base ={in_list_base}')
    in_list_large = [get_list(o, metric)[0] for o in args.outdir if '_0' in o]
    print(f'in large={in_list_large}')

    ipc_list_base = [i / c for i,c in zip(in_list_base,nl_list_base)]
    ipc_list_base_norm = [i/i for i in ipc_list_base]
    print(f'ipc base: {ipc_list_base_norm}')
    ipc_list_large = [i / c for i,c in zip(in_list_large,nl_list_large)]
    ipc_list_large_norm = [i/j for i,j in zip(ipc_list_large,ipc_list_base)]
    print(f'ipc large: {ipc_list_large_norm}')
    ipc_base_avg = gmean(ipc_list_base_norm)
    ipc_large_avg = gmean(ipc_list_large_norm)

    print(f'\n=== summary ===\nrt_norm_mean:{rt_norm_mean}\nipc_base:{ipc_base_avg}, ipc_large:{ipc_large_avg}\nnl_norm_mean:{nl_norm_mean}')

