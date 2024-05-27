#!/usr/bin/env python
# -- coding: utf-8 --
"""
Copyright (c) 2024. All rights reserved.
Created by C. L. Wang on 2024/2/19
"""

import os
import shutil
import sys

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if p not in sys.path:
    sys.path.append(p)


from scripts import run_on_pdbs
from myutils.project_utils import mkdir_if_not_exist
from root_dir import ROOT_DIR, DATA_DIR


class RunExamples(object):
    """
    运行程序
    """
    def __init__(self):
        pass

    def process(self):
        path_on_drive = os.path.join(ROOT_DIR, "example")  # @param {type:"string"}
        max_results_number = "5"  # @param [1, 5, 10, 20]
        create_cif_instead_of_pdb = False  # @param {type:"boolean"}

        subunits_path = os.path.join(path_on_drive, "subunits.json")
        pdbs_folder = os.path.join(path_on_drive, "pdbs")
        assembled_folder = os.path.join(path_on_drive, "assembled")
        mkdir_if_not_exist(assembled_folder)
        tmp_assembled_folder = os.path.join(path_on_drive, "tmp_assembled")

        mkdir_if_not_exist(assembled_folder)
        mkdir_if_not_exist(tmp_assembled_folder)

        if os.path.exists(assembled_folder):
            answer = input(f"[Info] {assembled_folder} already exists, Should delete? (y/n)")
            if answer in ("y", "Y"):
                print("[Info] Deleting")
                shutil.rmtree(assembled_folder)
            else:
                print("[Info] Stopping")
                exit()

        if os.path.exists(tmp_assembled_folder):
            shutil.rmtree(tmp_assembled_folder)

        # 核心运行逻辑
        run_on_pdbs.run_on_pdbs_folder(subunits_path, pdbs_folder, tmp_assembled_folder,
                                       output_cif=create_cif_instead_of_pdb,
                                       max_results_number=int(max_results_number))

        shutil.copytree(os.path.join(tmp_assembled_folder, "assembled_results"),
                        assembled_folder)

        print("[Info] Results saved to", assembled_folder)


def main():
    re = RunExamples()
    re.process()


if __name__ == '__main__':
    main()
