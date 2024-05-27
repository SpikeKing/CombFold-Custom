# 大型蛋白质复合物的组装流程 (CombFold)

By C.L. Wang

参考 [大型蛋白质复合物的组装流程 (CombFold)](https://blog.csdn.net/caroline_wendy/article/details/136187314)

> 使用 docker 的原因是 `sudo apt-get install libboost-all-dev` 需要 sudo 安装。


## 1. 生成 subunits.json 文件



调用 `generate_subunits.py` 脚本：

```bash
python myscripts/generate_subunits.py \
-i 7qrb_A292_B286_C292_D292_1162.fasta \
-o subunits.json
```

FASTA 示例，即 `7qrb_A292_B286_C292_D292_1162.fasta` ：

```bash
>A
LRVGNRYRLGRKIGSGSFGDIYLGTDIAAGEEVAIKLECVKTKHPQLHIESKIYKMMQGGVGIPTIRWCGAEGDYNVMVMELLGPSLEDLFNFCSRKFSLKTVLLLADQMISRIEYIHSKNFIHRDVKPDNFLMGLGKKGNLVYIIDFGLAKKYRDARTHQHIPYRENKNLTGTARYASINTHLGIEQSRRDDLESLGYVLMYFNLGSLPWQGLKAATKRQKYERISEKKMSTPIEVLCKGYPSEFATYLNFCRSLRFDDKPDYSYLRQLFRNLFHRQGFSYDYVFDWNMLK
>B
LRVGNRYRLGRKIGSGSFGDIYLGTDIAAGEEVAIKLECVKTKHPQLHIESKIYKMMQGGVGIPTIRWCGAEGDYNVMVMELLGPSLEDLFNFCSRKFSLKTVLLLADQMISRIEYIHSKNFIHRDVKPDNFLMGLGKKGNLVYIIDFGLAKKYRHIPYRENKNLTGTARYASINTHLGIEQSRRDDLESLGYVLMYFNLGSLPWQGLKAATKRQKYERISEKKMSTPIEVLCKGYPSEFATYLNFCRSLRFDDKPDYSYLRQLFRNLFHRQGFSYDYVFDWNMLK
>C
LRVGNRYRLGRKIGSGSFGDIYLGTDIAAGEEVAIKLECVKTKHPQLHIESKIYKMMQGGVGIPTIRWCGAEGDYNVMVMELLGPSLEDLFNFCSRKFSLKTVLLLADQMISRIEYIHSKNFIHRDVKPDNFLMGLGKKGNLVYIIDFGLAKKYRDARTHQHIPYRENKNLTGTARYASINTHLGIEQSRRDDLESLGYVLMYFNLGSLPWQGLKAATKRQKYERISEKKMSTPIEVLCKGYPSEFATYLNFCRSLRFDDKPDYSYLRQLFRNLFHRQGFSYDYVFDWNMLK
>D
LRVGNRYRLGRKIGSGSFGDIYLGTDIAAGEEVAIKLECVKTKHPQLHIESKIYKMMQGGVGIPTIRWCGAEGDYNVMVMELLGPSLEDLFNFCSRKFSLKTVLLLADQMISRIEYIHSKNFIHRDVKPDNFLMGLGKKGNLVYIIDFGLAKKYRDARTHQHIPYRENKNLTGTARYASINTHLGIEQSRRDDLESLGYVLMYFNLGSLPWQGLKAATKRQKYERISEKKMSTPIEVLCKGYPSEFATYLNFCRSLRFDDKPDYSYLRQLFRNLFHRQGFSYDYVFDWNMLK
```

输出结果 `subunits.json` ，即：

```bash
{
    "A0": {
        "name": "A0",
        "chain_names": [
            "A",
            "C",
            "D"
        ],
        "start_res": 1,
        "sequence": "LRVGNRYRLGRKIGSGSFGDIYLGTDIAAGEEVAIKLECVKTKHPQLHIESKIYKMMQGGVGIPTIRWCGAEGDYNVMVMELLGPSLEDLFNFCSRKFSLKTVLLLADQMISRIEYIHSKNFIHRDVKPDNFLMGLGKKGNLVYIIDFGLAKKYRDARTHQHIPYRENKNLTGTARYASINTHLGIEQSRRDDLESLGYVLMYFNLGSLPWQGLKAATKRQKYERISEKKMSTPIEVLCKGYPSEFATYLNFCRSLRFDDKPDYSYLRQLFRNLFHRQGFSYDYVFDWNMLK"
    },
    "B0": {
        "name": "B0",
        "chain_names": [
            "B"
        ],
        "start_res": 1,
        "sequence": "LRVGNRYRLGRKIGSGSFGDIYLGTDIAAGEEVAIKLECVKTKHPQLHIESKIYKMMQGGVGIPTIRWCGAEGDYNVMVMELLGPSLEDLFNFCSRKFSLKTVLLLADQMISRIEYIHSKNFIHRDVKPDNFLMGLGKKGNLVYIIDFGLAKKYRHIPYRENKNLTGTARYASINTHLGIEQSRRDDLESLGYVLMYFNLGSLPWQGLKAATKRQKYERISEKKMSTPIEVLCKGYPSEFATYLNFCRSLRFDDKPDYSYLRQLFRNLFHRQGFSYDYVFDWNMLK"
    }
}
```



## 2. 调用函数生成一组 FASTA 文件



调用默认函数 `scripts/prepare_fastas.py` ，即：

- 输入已生成的 `subunits.json` 文件
- `--stage` 选择 `pairs` 模式，同时支持 `groups` 模式
- `--output-fasta-folder` 是输出文件夹，例如 `mydata/fastas`
- `--max-af-size` 是最大序列长度，即 1800

即：

```bash
# 默认 pairs 生成
python3 scripts/prepare_fastas.py mydata/subunits.json --stage pairs --output-fasta-folder mydata/fastas --max-af-size 1800
# 根据 groups 生成
# python3 scripts/prepare_fastas.py mydata/subunits.json  --stage groups --output-fasta-folder mydata/fastas --max-af-size 1800 --input-pairs-results <path_to_AFM_pairs_results>
```

输出文件夹的内容如下，例如 `mydata/fastas`，即：

```bash
A0_A0.fasta
A0_A0_A0.fasta
A0_A0_B0.fasta
A0_B0.fasta
```



## 3. 根据 AFM 的搜索生成一组 MSAs



调用函数 `generate_comb_msa.py`：

- `-i`：输入已生成的一组 FASTA 文件
- `-m`：AFM 已搜索的 MSAs 文件夹 (需要提前准备)，例如 `7qrb_A292_B286_C292_D292_1162/msas`
- `-o`：输出的一组 MSAs 文件，例如 `mydata/comb_msas`

即：

```bash
python myscripts/generate_comb_msa.py \
-i mydata/fastas \
-m [afm searched msas]
-o mydata/comb_msas
```

输出文件夹 `mydata/comb_msas` 示例：

```bash
A0_A0/
A0_A0_A0/
A0_A0_B0/
A0_B0/
```

调用 AFM 程序，执行 `Subunits PDB` 推理：

```bash
bash run_alphafold.sh \
-o mydata/comb_msas/ \
-f mydata/fastas/ \
-m "multimer" \
-l 5
```



## 4. 导出 Subunits 的 PDBs 文件



调用函数 `export_comb_pdbs.py`：

- `-i`：输入 AFM 已生成 Subunits 的  PDB 文件，例如  `mydata/comb_msas`
- `-o`：输出 一组 PDB 文件，合并至一个文件夹，并且重命名，例如 `mydata/pdbs`

即：

```bash
python myscripts/export_comb_pdbs.py \
-i mydata/comb_msas \
-o mydata/pdbs
```



## 5. 调用 Comb Assembly 程序



调用函数 `myscripts/run_examples.py`，具体参数源码，即：

```python
path_on_drive = os.path.join(DATA_DIR, "example_1")  # @param {type:"string"}
max_results_number = "5"  # @param [1, 5, 10, 20]
create_cif_instead_of_pdb = False  # @param {type:"boolean"}

subunits_path = os.path.join(path_on_drive, "subunits.json")
pdbs_folder = os.path.join(path_on_drive, "pdbs")
assembled_folder = os.path.join(path_on_drive, "assembled")
mkdir_if_not_exist(assembled_folder)
tmp_assembled_folder = os.path.join(path_on_drive, "tmp_assembled")
```

最终输出文件 `assembled`，即：

```bash
confidence.txt
output_clustered_0.pdb
```

最终结果，即 `output_clustered_0.pdb` 。



其中，也可以输入 Crosslinks 交联质谱数据。来源于 pLink2 软件的交联肽段的分析结果。

每一行代表一个交联对，由两个肽段组成，即：

- 第1维和第2维，表示 蛋白质序号 与 蛋白质链名。
- 第3维和第4维，同上，即表示 A链中的a位置蛋白，与B链中的b位置蛋白，相互作用。
- 第5维和第6维，表示 联剂的类型 与 交联剂的臂长，确定交联位点的距离限制和交联剂的选择。
- 第7维表示为置信度。

例如：

```bash
94 2 651 C 0 30 0.85
149 2 651 C 0 30 0.92
280 2 196 A 0 30 0.96
789 C 159 T 0 30 0.67
40 T 27 b 0 30 0.86
424 2 206 A 0 30 0.55
351 2 29 T 0 30 0.84
149 2 196 A 0 30 0.93
761 C 304 T 0 30 0.95
152 2 651 C 0 30 0.94
351 2 832 C 0 30 0.87
206 A 645 C 0 30 0.75
832 C 40 T 0 30 0.85
424 2 23 b 0 30 0.75
```

> 0 表示交联剂是不可裂解型的，如 BS3 或 DSS2。30 表示交联剂的臂长是 30 A。




