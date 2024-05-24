# ALGORITHM FOR SEARCHING OF FREQUENCY CHANGES IN RANDOMIZED DNA LIBRARIES

## Content
- [Project Goal](#project_goal)
- [Project presentation](#project_presentation)
- [Tested datasets](#datasets)
- [Project tasks](#tasks)
- [Getting coverages from fasta-files](#bash-script)
- [PeakCalling work example](#peakcalling)
- [Methods and technologies](#methods_and_technologies)
- [Authors](#authors)

## [Project Goal](#project_goal)
Our mission was to design and to implement algorithm of detection and analysis of gene frequency changes in different random DNA libraries.

## [Project presentation](#project_presentation)
A detailed presentation of the project is available at the following link:
[Project Presentation in Google Slides](https://docs.google.com/presentation/d/19mHDZ0CSnLlx3B0bmdQ0IPGS7Bzpw0VhEKGx3RNjeOc/edit#slide=id.g2dab76cc6da_0_0)

## [Tested datasets](#datasets)

- Dataset 1 (search for the PARIS system triggers from T5 phage): \
  DNA samples were extracted from cells under three different conditions:
  - (1) Сells before induction (16_t5-d-plasm_x200);
  - (2) Induction of T5 genes library in cells without PARIS (16_t5_plus_d-plasm_x200);
  - (3) Induction of T5 genes library in cells with PARIS (185_t5_plus_d-plasm_x200);
  
- Dataset 2 (search for genes responsible for methylation inhibition from T5 phage): \
  DNA samples were extracted from cells under two different conditions:
  - (1) Cells before treatment with Dpn (T5_lib_Meth_Inhib_Dpn/t5_plus_dapg-plasm_x200);
  - (2) Cells after several rounds of treatment with Dpn (T5_lib_Meth_Inhib_Dpn/t5_plus_dapg_plus_dpn-plasm_x200);

## [Project tasks](#tasks)
1. Analyzing the genomic composition of the mapped reads of the dataset.
2. Comparing the differences in coverage of mapped genes of bacteriophage genome samples with the genome containing PARIS trigger using featurecounts and peakcalling.
3. Visualizing significant changes and comparing them to genome annotation.
4. Find genes of interests (PARIS triggers).
5. Repeating the analysis on other datasets.

## [Getting coverages from fasta-files](#bash-script)
Bash script for reads preprocessing with the following operions:\
- fastp v. 0.23.2: trimming, quality control and deduplication of paired-end reads (fastq); 
- bowtie2 v2.5.4: mapping reads to T5 phage reference genome (fasta);
- samtools v. 1.20:
- convertion of dam files to bam, sorting and indexing of bam files;
- generation of coverage.txt files from sorted_bam files (further, coverage files are parsed to peak calling script).


## [PeakCalling example](#peakcalling)
Full example you can find in `PeakCaller_example.ipynb`

`TXT` files (datasets with coverages from fasta files) you can get from our bash-script (previous point)

### Installation 
To install our peakcalling script, please, follow these steps:
- First, you need to clone this repository by `git clone` command in command line.

- After that you can copy `peakcaller.py` and `requirements.txt` files to your default Jupiter Notebook folder (commonly its *Home* directory on your computer)
- Create `your notebook.ipynb` file in Jupiter notebook (or Jupiter Lab) and use commands below.

### Example of use

1. Import `peakcaller.py` and requirements to your notebook:
```python
pip install -r requirements.txt
from peakcaller import PeakCalling
```

2. Input number of reads for each dataset:
```python
# Example
reads_count_1 = 1504149
reads_count_2 = 8991837
```
3. Initiate Peak Calling class:
```python
peak_calling = PeakCalling( \
    data_1='./data/coverage_16t5_plus_r209.txt', \  # path to first dataset
    data_2='./data/coverage_185_t5_sorted.txt', \   # path to second dataset
    threshold=0.6, \                                # optional param for filtering significant changes
    window_size=250,                                # required param for setting significant changes areas
    reads_count_1=reads_count_1, \                  # required param for normalization of datasets to each other
    reads_count_2=reads_count_2 \                   # required param for normalization of datasets to each other
)
```
4. Find significant changes:
```python
changes = peak_calling.find_significant_coverage_changes()
changes.head(10)
```
5. View significant changes on coverage map:
```python
peak_calling.visualize_coverage()
```
6. Compare significant changes with genome annotation:
```python
gff_path = 'data/t5.gff3' # Path to .gff annotation
peak_calling.compare_coverage_changes_with_annotation(gff_annotation=gff_path)
```


## [Methods and technologies used](#methods_and_technologies)
- `featureCounts`
- `genomenotebook` - used in Peak Calling algorithm for visualization coverages and significant changes with genome annotation (need `annotation.gff` file as option)
- `pandas` - used in Peak Calling algorithm as the main tool of work with data
- `numpy` - used in Peak Calling for identification of significant changes in two applied datasets
- `plotly` - used in Peak Calling for dynamic visualization of coverages and significant changes (not compared with genome annotation)

## [Authors](#authors)
- 💼 **Chernikov Danila** - `architector` and `developer`. [Telegram](https://t.me/dachernikov)
- 🚀 **Babaeva Maria** - `analyst` and `developer`. [Telegram](https://t.me/icalledmyselfmoon)
- ✨ **Kotovskaya Oksana** - `supervisor` and `team-leader`. [Telegram](https://t.me/nerawe)
