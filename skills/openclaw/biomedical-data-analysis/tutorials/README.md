<!--
# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

-->

# Data Analysis Tutorials

This directory contains comprehensive tutorials for data analysis covering Python, R, SQL, and visualization tools.

## Contents Summary

| Category | Repositories | Files | Description |
|----------|--------------|-------|-------------|
| **Python** | 3 | 34 notebooks | NumPy, Pandas, SciPy |
| **R** | 2 | 15 R Markdown | tidyverse, dplyr, ggplot2 |
| **SQL** | 3 | 147 SQL files | Biomedical, Healthcare, Analytics |
| **Visualization** | 2 | Multiple | Tableau, Power BI |

---

## Python Tutorials

### numpy-tutorials (Official)
**Source:** [numpy/numpy-tutorials](https://github.com/numpy/numpy-tutorials)

NumPy tutorials & educational content in notebook format. Official documentation from the NumPy project.

**Topics covered:**
- Array fundamentals and operations
- Linear algebra with NumPy
- X-ray image analysis
- NLP from scratch
- Saving and sharing arrays

### pandas-workshop
**Source:** [stefmolin/pandas-workshop](https://github.com/stefmolin/pandas-workshop)

An introductory workshop on pandas delivered at major conferences (ODSC Europe, PyCon US 2022, PyCon Poland 2024, SciPy 2025).

**Topics covered:**
- Getting started with pandas
- Data wrangling
- Data visualization
- Hands-on exercises with solutions

### pandas-cookbook
**Source:** [jvns/pandas-cookbook](https://github.com/jvns/pandas-cookbook)

Recipes for using Python's pandas library with real-world data examples.

**Topics covered:**
- Reading from CSV
- Selecting data
- Groupby operations
- Handling messy data
- Combining dataframes

---

## R Tutorials

### tidyverse-workshop (RStudio Education)
**Source:** [rstudio-education/welcome-to-the-tidyverse](https://github.com/rstudio-education/welcome-to-the-tidyverse)

Official RStudio Education workshop taught by Garrett Grolemund, co-author of "R for Data Science."

**Topics covered:**
- Data visualization with ggplot2
- Data transformation with dplyr
- Tidy data principles with tidyr
- Data import

### r-tidyverse-series (Northwestern IT)
**Source:** [nuitrcs/r-tidyverse](https://github.com/nuitrcs/r-tidyverse)

Workshop series materials from Northwestern University IT Research Computing.

**Topics covered:**
- dplyr data manipulation
- ggplot2 visualization
- tidyr data reshaping
- lubridate date handling
- stringr string manipulation

---

## SQL Tutorials

### biomedsql (NIH)
**Source:** [NIH-CARD/biomedsql](https://github.com/NIH-CARD/biomedsql)

BiomedSQL: A text-to-SQL benchmark for scientific reasoning on biomedical knowledge bases. From NIH researchers (arXiv:2505.20321).

**Biomedical applications:**
- PubMed database queries
- Clinical trial data analysis
- Genomic variant queries
- Drug-disease relationships

### sql-for-analytics (Packt)
**Source:** [TrainingByPackt/SQL-for-Data-Analytics](https://github.com/TrainingByPackt/SQL-for-Data-Analytics)

SQL for Data Analysis - covers techniques for extracting insights from data.

**Topics covered:**
- Basic to advanced SQL queries
- Aggregations and window functions
- Time-series analysis
- Geospatial data
- Text analytics

### healthcare-sql
**Source:** [SPARTANX21/SQL-Data-Analysis-Healthcare-Project](https://github.com/SPARTANX21/SQL-Data-Analysis-Healthcare-Project)

SQL analysis of healthcare datasets with real-world scenarios.

**Topics covered:**
- Patient demographics analysis
- Medical condition trends
- Treatment outcomes
- Hospital performance metrics
- Financial analysis

---

## Visualization Tutorials

### tableau-powerbi-learning
**Source:** [Ashleshk/TableaU-PowerBI-Visualisation-Learning-path](https://github.com/Ashleshk/TableaU-PowerBI-Visualisation-Learning-path)

Hands-on project on Prepare, Clean, Transform, and Load Data using Tableau & Power BI.

**Topics covered:**
- Data preparation workflows
- Dashboard design
- Interactive filters
- Calculated fields
- Publishing and sharing

### data-viz-projects
**Source:** [ptyadana/SQL-Data-Analysis-and-Visualization-Projects](https://github.com/ptyadana/SQL-Data-Analysis-and-Visualization-Projects)

SQL data analysis & visualization projects using MySQL, PostgreSQL, SQLite, Tableau, Apache Spark and pySpark.

**Topics covered:**
- End-to-end analysis projects
- Database integration
- Spark for big data
- Dashboard creation

---

## Getting Started

### Python Tutorials
```bash
cd python/pandas-workshop
pip install -r requirements.txt
jupyter notebook
```

### R Tutorials
```r
# Install tidyverse
install.packages("tidyverse")

# Open RStudio and navigate to r/tidyverse-workshop/
```

### SQL Tutorials
```bash
# Most SQL tutorials can be run with any SQL client
# For biomedsql, follow the repository instructions for setup
```

---

## Contributing

To add more tutorials, please:
1. Clone the repository with `--depth 1` to save space
2. Add an entry to this README
3. Update the main skill README.md

---

## License

Individual tutorial repositories maintain their own licenses. Please refer to each repository for licensing information.


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->