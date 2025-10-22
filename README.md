# 🏏 Cricket Score Predictor (ML-based)

A Dynamic Cricket Match Predictor utilizing a trained Machine Learning model to deliver actionable, real-time win probability analysis. The system is initialized by specifying the two competing teams and the match venue, along with the First Innings Score. Its core strength lies in its adaptive prediction engine, which continuously adjusts and outputs the win probability for each team based on the evolving state of the second innings (current run rate, completed overs, and wickets down).

---

## 📌 Project Overview

This project demonstrates how historical ball-by-ball data from IPL matches can be used to train a **regression model** that predicts the final score of an ongoing innings. It leverages :

- Data preprocessing with **Pandas**
- Model building with **Scikit-learn**
- Dashboard UI with **Streamlit**

---

## 📁 Dataset Used

- Dataset: `ipl_2022_deliveries.csv`
- Source: Kaggle (or official IPL data)
- Format: Ball-by-ball breakdown of each innings

---

## ⚙️ Features

- Predict final score given:
  - Current over
  - Cumulative score
- Simple Streamlit UI to test different scenarios
- MAE, RMSE, and R² Score evaluation of model performance

---

## 📊 Libraries & Tools Used

| Tool           | Purpose                             |
|----------------|-------------------------------------|
| `pandas`       | Data manipulation                   |
| `numpy`        | Numeric calculations                |
| `matplotlib`   | Visualizations           |
| `seaborn`      | Visualizations           |
| `scikit-learn` | Model training and evaluation       |
| `streamlit`    | Interactive web dashboard           |

---

## 🧠 Machine Learning Model

- Model Used: **Linear Regression**
- Input Features:
  - `over`
  - `cumulative_score`
- Target:
  - `final_score`

#### 📈 Evaluation Metrics:
- **MAE**: ~17 runs  
- **RMSE**: ~23 runs  
- **R² Score**: ~0.34

---

## 💻 How to Run

### 1. Clone this repo
```bash
https://github.com/vedprakash8721/Cricket-Score-Predictor
