#!/usr/bin/env python3

'''
Description: Filters the longest isoforms of each gene (Work in progress)
'''

import argparse
import os
import re
import sys
import utils

def main():
    parser = argparse.ArgumentParser( description='Filters trinity output for longest subcomponents based on naming convention')

    # writing output file 
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to an input FASTA file' )
    parser.add_argument('-o', '--output', type=str, required=False, help='Output file to be created.  Default = STDOUT' )
    args = parser.parse_args()

    # output formatting
    fout = sys.stdout
    if args.output is not None:
        fout = open(args.output, 'wt')

    seqs = utils.fasta_dict_from_file(args.input)

    components = dict()

    for seq_id in seqs:
        m = re.search("(comp\d+)_", seq_id)
        if m:
            component_id = m.group(1)

            if component_id not in components or len(seqs[seq_id]['s']) > len(components[component_id]['s']):
                components[component_id] = seqs[seq_id]
                components[component_id]['longest_id'] = seq_id
        else:
            raise Exception("ERROR: This ID wasn't in the expected format of compN_cN_seqN: {0}".format(seq_id))

    for c_id in components:
        seq_wrapped = utils.wrapped_fasta(components[c_id]['s'], every=60)
        fout.write(">{0} {1}\n{2}\n".format(components[c_id]['longest_id'], components[c_id]['h'], seq_wrapped))


if __name__ == '__main__':
    main()