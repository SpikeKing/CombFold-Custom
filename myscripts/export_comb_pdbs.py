#!/usr/bin/env python
# -- coding: utf-8 --
"""
Copyright (c) 2024. All rights reserved.
Created by C. L. Wang on 2024/2/20
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if p not in sys.path:
    sys.path.append(p)

from myutils.project_utils import mkdir_if_not_exist, traverse_dir_files


class ExportCombPdbs(object):
    """
    导出 Comb PDBs 文件
    """
    def __init__(self):
        pass

    def process(self, input_dir, output_dir):
        print(f"[Info] input_dir: {input_dir}")
        print(f"[Info] output_dir: {output_dir}")
        mkdir_if_not_exist(output_dir)
        path_list = traverse_dir_files(input_dir, "pdb")
        for path in path_list:
            base_name = os.path.basename(path)
            folder_name = path.split("/")[-2]
            if not base_name.startswith("unrelaxed"):
                continue
            # AFM_A0_A0_A0_unrelaxed_rank_1_model_3.pdb
            output_name = f"AFM_{folder_name}_{base_name}"
            output_path = os.path.join(output_dir, output_name)
            shutil.copy(path, output_path)  # 复制文件


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input-dir",
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
    output_dir = str(args.output_dir)

    assert os.path.isdir(input_dir)

    ecp = ExportCombPdbs()
    ecp.process(input_dir, output_dir)


def main2():
    input_dir = "mydata/comb_msas"
    output_dir = "mydata/outputs"
    ecp = ExportCombPdbs()
    ecp.process(input_dir, output_dir)


if __name__ == '__main__':
    main()
