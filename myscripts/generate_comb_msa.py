#!/usr/bin/env python
# -- coding: utf-8 --
"""
Copyright (c) 2024. All rights reserved.
Created by C. L. Wang on 2024/2/19
"""
import argparse
import json
import os
import shutil
import sys
from pathlib import Path

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if p not in sys.path:
    sys.path.append(p)

from myutils.project_utils import mkdir_if_not_exist, traverse_dir_folders, traverse_dir_files
from myutils.protein_utils import get_seq_from_fasta
from root_dir import DATA_DIR


class GenerateCombMsa(object):
    """
    根据已知的 MSA 搜索，构建新的 MSA 文件夹
    """
    def __init__(self):
        pass

    def process(self, input_dir, msa_path, output_dir):
        print(f"[Info] input_dir: {input_dir}")
        print(f"[Info] msa_path: {msa_path}")
        print(f"[Info] output_dir: {output_dir}")
        paths_list = traverse_dir_files(input_dir, "fasta")
        print(f"[Info] fasta: {len(paths_list)}")

        for path in paths_list:
            self.process_fasta(path, msa_path, output_dir)
        print(f"[Info] 处理完成: {output_dir}")

    def process_fasta(self, input_path, msa_path, output_dir):
        mkdir_if_not_exist(output_dir)

        map_path = os.path.join(msa_path, "chain_id_map.json")

        folder_list = traverse_dir_folders(msa_path)
        chain_folder_map = {}
        for folder_path in folder_list:
            # print(f"[Info] folder_path: {folder_path}")
            name = os.path.basename(folder_path)
            chain_folder_map[name] = folder_path
        # print(f"[Info] chain_folder_map: {chain_folder_map}")

        with open(map_path, "r") as f:
            chain_id_map = json.load(f)
        # print(f"[Info] chain_id_map: {chain_id_map}")
        seq_folder_map = dict()
        for key in chain_id_map.keys():
            seq = chain_id_map[key]["sequence"]
            if key in chain_folder_map.keys():
                folder_path = chain_folder_map[key]
                seq_folder_map[seq] = folder_path
        # print(f"[Info] seq_folder_map: {seq_folder_map}")

        # 创建文件夹
        fasta_name = os.path.basename(input_path).split(".")[0]
        fasta_dir = os.path.join(output_dir, fasta_name, "msas")
        mkdir_if_not_exist(fasta_dir)

        new_chain_id_map = {}
        seq_list, desc_list = get_seq_from_fasta(input_path)
        copied_set = set()

        for seq, desc in zip(seq_list, desc_list):
            new_chain_id_map[desc] = {
                "description": desc,
                "sequence": seq
            }
            if seq in seq_folder_map.keys():
                if seq not in copied_set:
                    copied_set.add(seq)
                    output_msa_folder = os.path.join(fasta_dir, desc)
                    if not os.path.exists(output_msa_folder):
                        shutil.copytree(seq_folder_map[seq], output_msa_folder)

        output_map_path = os.path.join(fasta_dir, "chain_id_map.json")
        with open(output_map_path, "w") as f:
            f.write(json.dumps(new_chain_id_map, indent=4))

        print(f"[Info] fasta 处理完成: {fasta_dir}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input-dir",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "-m",
        "--msa-path",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        required=True
    )
    args = parser.parse_args()

    input_dir = str(args.input_dir)
    msa_path = str(args.msa_path)
    output_dir = str(args.output_dir)

    assert os.path.isdir(input_dir) and os.path.isdir(msa_path)
    mkdir_if_not_exist(output_dir)

    gcm = GenerateCombMsa()
    gcm.process(input_dir, msa_path, output_dir)


def main2():
    gcm = GenerateCombMsa()
    input_dir = os.path.join(DATA_DIR, "fastas")
    msa_path = "/pfs_beijing/chenlong/multimer_train/val_data/fasta_100_af2_msas/7qrb_A292_B286_C292_D292_1162/msas"
    output_dir = os.path.join(DATA_DIR, "comb_msas")
    gcm.process(input_dir, msa_path, output_dir)


if __name__ == '__main__':
    main()
