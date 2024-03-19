# IDENTIFICATION TRIGGERS OF PARIS DEFENCE SYSTEM

## Content
- [Project Goal](#project_goal)
- [Project presentation](#project_presentation)
- [Datasets](#datasets)
- [Project tasks](#tasks)
- [Methods and technologies](#methods_and_technologies)
- [Authors](#authors)

## [Project Goal](#project_goal)
The main objective of the project is to identify viral triggers of the PARIS abortive defense system through changes in gene frequencies in plasmid libraries.

## [Project presentation](#project_presentation)
A detailed presentation of the project is available at the following link:
[Project Presentation in Google Slides](https://docs.google.com/presentation/d/1-KTM0OiHdkXXXEEehxYrX4-w9287vMTyLXqOCywW6qE/edit#slide=id.g2c46fa53951_0_13)

## [Datasets (you can find them in `data/raw`)](#datasets)
The following datasets are used in the project:
- T5_lib_PARIS_triggers:
  * 16_t5-d-plasm_x200 - Cells before induction
  * 16_t5_plus_d-plasm_x200 - Induction of T5 genes library in cells without PARIS
  * 185_t5_plus_d-plasm_x200 - Induction of T5 genes library in cells with PARIS
  
- MSK10_lib_PARIS_triggers:
  * 16_msk10-d-plasm_x200 - Cells before induction
  * 16_msk10_plus_d-plasm_x200 - Induction of Msk10 genes library in cells without PARIS
  * 185_msk10_plus_d-plasm_x200 - Induction of Msk10 genes library in cells with PARIS
  
- T5_lib_Meth_Inhib_Dpn:
  * T5_lib_Meth_Inhib_Dpn/t5_plus_dapg-plasm_x200 - Cells before treatment with Dpn
  * T5_lib_Meth_Inhib_Dpn/t5_plus_dapg_plus_dpn-plasm_x200 - Cells after several rounds of treatment with Dpn

## [Project tasks](#tasks)
1. Analyzing the genomic composition of the mapped reads of the dataset.
2. Comparing the differences in coverage of mapped genes of bacteriophage genome samples with the genome containing PARIS trigger using featurecounts and peakcalling.
3- Detecting the position of PARIS triggers and visualizing the results.
4. Explanation of the results.
5. Repeating the analysis on other datasets.

## [Methods and technologies used](#methods_and_technologies)
(здесь можно описать основные используемые методы и технологии, например, какие библиотеки или инструменты биоинформатики использовалиcь)

## [Authors](#authors)
- 💼 **Chernikov Danila** - `architector` and `developer`. [Telegram](https://t.me/dachernikov)
- 🚀 **Babaeva Maria** - `analyst` and `developer`. [Telegram](https://t.me/icalledmyselfmoon)
- ✨ **Kotovskaya Oksana** - `supervisor` and `team-leader`. [Telegram](https://t.me/nerawe)
