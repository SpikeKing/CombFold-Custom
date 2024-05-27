#!/usr/bin/env python
# -- coding: utf-8 --
"""
Copyright (c) 2022. All rights reserved.
Created by C. L. Wang on 2023/7/5
"""

import os

from Bio.Data.PDBData import protein_letters_3to1_extended as d3to1_ex
from Bio.PDB import PDBParser

from myutils.project_utils import read_file, create_empty_file, write_line


def get_seq_from_fasta(fasta_path):
    """
    获取 FASTA 序列
    """
    lines = read_file(fasta_path)
    seq_list, desc_list = [], []
    for i in range(1, len(lines), 2):
        desc_list.append(lines[i-1][1:])  # 去除 <
        seq_list.append(lines[i])
    return seq_list, desc_list


def get_seq_from_pdb(pdb_path, version="new"):
    """
    从PDB中获取序列
    :param pdb_path: PDB路径
    :param version: PDB路径
    :return: sequence序列, 链长, 链字典
    """
    # 常见的20种结构
    if version == "old":
        d3to1 = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
                 'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
                 'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
                 'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}
    elif version == "new":
        d3to1 = d3to1_ex
    else:
        raise Exception("[Error] version must be old or new!")

    def_ids = ['I', 'Q', 'R', 'L', 'M', 'A', 'V', 'B', 'E', 'D', 'S', 'C',
               'K', 'Y', 'X', 'J', 'T', 'F', 'G', 'W', 'H', 'P', 'Z', 'N']

    record = pdb_path  # PDB路径

    # 解析器
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('struct', record)

    chain_dict = {}
    res_str = ""
    for model in structure:
        for c_id, chain in enumerate(model):
            header = chain.id
            seq = []
            for residue in chain:
                if residue.resname in d3to1.keys():
                    a = d3to1[residue.resname]
                    if a in def_ids:
                        seq.append(a)
                    else:
                        raise Exception(f"atom not in default: {a}")
                elif residue.resname == "HOH":
                    continue
                # else:
                #     print(f"[Warning] {residue.resname} don't support!")
            if not seq:
                continue
            seq_str = "".join(seq)
            if not str(header).strip():
                header = f"{chr(c_id+97).upper()}"
            if len(header) > 5:   # 避免header过长和重复
                header = f"{header[:5]}_{chr(c_id+97).upper()}"
            res_str += f">{header}\n{seq_str}\n"
            # print(f"[Info] chain: {header}, num of residue: {len(seq_str)}")
            chain_dict[header] = seq_str
    seq_str = res_str.strip()
    n_chains = len(chain_dict)

    return seq_str, n_chains, chain_dict


def get_fasta_from_pdb(pdb_path, fasta_dir):
    """
    从PDB文件中，提取FASTA文件
    写入文件命名 [PDB名称]_[链A][链A长度]_[链B][链B长度]...
    """
    seq_str, _, chain_dict = get_seq_from_pdb(pdb_path)
    sum_len = 0
    # 确定文件名称
    suffix = ""
    for key in chain_dict.keys():
        val = chain_dict[key]
        suffix += f"{key}{str(len(val))}"
        suffix += "_"
        sum_len += len(val)
    if suffix.endswith("_"):
        suffix = suffix[:-1]

    # 写入文件
    pdb_name = os.path.basename(pdb_path).split(".")[0]
    fasta_path = os.path.join(fasta_dir, f"{pdb_name}_{suffix}_{sum_len}.fasta")
    create_empty_file(fasta_path)
    write_line(fasta_path, seq_str)
