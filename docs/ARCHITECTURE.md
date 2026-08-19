# Agent Reliability Lab — Architecture

## 1. System Overview

Agent Reliability Lab is a **hybrid reliability classification system** for AI agent traces.  
It combines:

1. Behavioral feature extraction  
2. TF-IDF text representation  
3. Structured behavioral features  
4. Logistic-regression classification  
5. Deterministic reliability rules (V8 hybrid layer)  
6. Final hybrid prediction  

The system is deliberately designed to distinguish **specific failure modes** rather than treating every incorrect or suboptimal response as a single generic “failure” class.

---

## 2. End-to-End Pipeline

```text
Agent Trace
    │
    ▼
Dataset
    │
    ▼
Feature Extraction
    │
    ├──────────────────────────┐
    │                          │
    ▼                          ▼
Combined Text             Behavioral Features
    │                          │
    ▼                          ▼
TF-IDF Vectorizer         Structured Numeric Features
    │                          │
    └────────────┬─────────────┘
                 │
                 ▼
        Logistic Regression
                 │
                 ▼
           ML Prediction
                 │
                 ▼
         V8 Hybrid Rules
                 │
                 ▼
         Final Prediction