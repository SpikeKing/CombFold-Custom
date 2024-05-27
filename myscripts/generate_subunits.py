#!/usr/bin/env python
# -- coding: utf-8 --
"""
Copyright (c) 2024. All rights reserved.
Created by C. L. Wang on 2024/2/19
"""
import argparse
import collections
import json
import os
import sys
from pathlib import Path

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if p not in sys.path:
    sys.path.append(p)

from myutils.protein_utils import get_seq_from_fasta
from root_dir import DATA_DIR


class GenerateSubunits(object):
    """
    从 fasta 生成 subunits.json
    """
    def __init__(self):
        pass

    def process(self, input_path, output_path):
        print(f"[Info] input_path: {input_path}")
        print(f"[Info] output_path: {output_path}")

        seq_list, desc_list = get_seq_from_fasta(input_path)
        print(f"[Info] seq_list: {seq_list}")
        print(f"[Info] desc_list: {desc_list}")

        seq_dict = collections.defaultdict(list)
        for seq, desc in zip(seq_list, desc_list):
            seq_dict[seq].append(desc)

        su_dict = {}
        for seq in seq_dict.keys():
            chain_names = seq_dict[seq]
            su_name = chain_names[0] + "0"
            su_dict[su_name] = {
                "name": su_name,
                "chain_names": chain_names,
                "start_res": 1,
                "sequence": seq
            }
        with open(output_path, "w") as f:
            f.write(json.dumps(su_dict, indent=4))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input-path",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output-path",
        type=Path,
        required=True
    )
    args = parser.parse_args()

    input_path = str(args.input_path)
    output_path = str(args.output_path)

    assert os.path.isfile(input_path)

    gs = GenerateSubunits()
    gs.process(input_path, output_path)


def main2():
    gs = GenerateSubunits()
    input_path = os.path.join(DATA_DIR, "7qrb_A292_B286_C292_D292_1162.fasta")
    output_path = os.path.join(DATA_DIR, "subunits.json")
    gs.process(input_path, output_path)


if __name__ == '__main__':
    main()
