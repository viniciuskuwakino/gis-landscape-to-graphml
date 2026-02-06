# A Graph-Based Approach for Modeling Landscape Connectivity and Analyzing Runoff Potential

This repository contains the computational framework *gis-landscape-to-graphml*, developed to convert landscape mosaics into Directed Acyclic Graphs (DAGs) for surface runoff analysis.

## 📋 Overview

This work presents a computational approach for modeling landscape structures aimed at hydrological analysis. The primary contribution is a reproducible Python pipeline that converts geospatial data describing land patches and boundaries into a Directed Acyclic Graph (DAG).

Unlike traditional raster-based models, this approach focuses on functional connectivity between discrete management units, enabling the identification of critical flow corridors through graph theory algorithms.

## 🚀 Main Features

*GIS-to-Graph Conversion:* Automated transformation of geographic polygons and boundaries into vertex–edge graph structures.

*Edge Valuation Metric:* Implementation of a composite edge-weighting metric integrating elevation difference (), Curve Number contrast (), and boundary length ().

*Algorithmic Analysis:* Tools to compute Degree Centrality (sources/sinks), flow propagation via Breadth-First Search (BFS), and identification of the maximum-influence path through an adaptation of the Bellman–Ford algorithm.

## 📁 Repository Structure

* /src: Python scripts implementing the three pipeline stages: Cleaning, Structuring, and Generation. And the `algorithms.py` to run on Gephi terminal and execute Graph Algorithms.

* /notebooks: A Python notebook that documents, step by step, the procedures executed by `script.py`.

* /data: Sample input datasets in CSV format (patches and boundaries).

* /output: Example generated GraphML files, compatible with network analysis software such as Gephi.

## 💻 Technical Requirements

*Language:* Python 3.8 or higher

*Hardware:* Standard personal computer

*License:* MIT License

## ⚠️ Project Status

This codebase is an integral part of a manuscript submitted for publication to the journal *Computers & Geosciences*. The repository is intended to ensure the reproducibility of the results presented in the case study conducted in Alto Piquiri and Mariluz, Paraná, Brazil.

---