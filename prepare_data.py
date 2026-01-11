# prepare_data.py
import numpy as np
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter

#Carrega dels datasets
df1 = kagglehub.load_dataset(KaggleDatasetAdapter.PANDAS,"johnsmith88/heart-disease-dataset","heart.csv")

df2 = kagglehub.load_dataset(KaggleDatasetAdapter.PANDAS,"oktayrdeki/heart-disease","heart_disease.csv")

# PREPROCESS
# Uneix noms
df1 = df1.rename(columns={"age":"Age","sex":"Gender","trestbps":"Blood Pressure","chol":"Cholesterol Level","fbs":"Fasting Blood Sugar","target":"Heart Disease Status"})
df1["Gender"] = df1["Gender"].map({0:"Female",1:"Male"})
df1["Heart Disease Status"] = df1["Heart Disease Status"].map({0:"No",1:"Yes"})

common_cols = list(set(df1.columns) & set(df2.columns))
df1 = df1[common_cols].copy()

extra_cols = list(set(df2.columns) - set(common_cols))
for col in extra_cols:
    df1[col] = np.nan

df_final = pd.concat([df1, df2], ignore_index=True)

# IMPUTATION

num_cols = df_final.select_dtypes(include=np.number).columns
for col in num_cols:
    df_final[col] = df_final[col].fillna(df_final[col].median())

cat_cols = df_final.select_dtypes(include="object").columns
for col in cat_cols:
    df_final[col] = df_final[col].fillna(df_final[col].mode()[0])

#INDICATORS

crp_threshold = df_final["CRP Level"].quantile(0.75)

df_final["metabolic_risk"] = (
    (df_final["High LDL Cholesterol"] == "Yes").astype(int) +
    (df_final["Low HDL Cholesterol"] == "Yes").astype(int) +
    (df_final["BMI"] > 30).astype(int) +
    (df_final["Fasting Blood Sugar"] > 120).astype(int) +
    (df_final["CRP Level"] > crp_threshold).astype(int) +
    (df_final["Triglyceride Level"] > 150).astype(int)
)

exercise_score = df_final["Exercise Habits"].map({"High":2,"Medium":1,"Low":0})

sleep_score = pd.cut(
    df_final["Sleep Hours"],
    bins=[0,5,7,24],
    labels=[0,1,2]
).astype(int)

smoking_penalty = (df_final["Smoking"]=="Yes").astype(int)
alcohol_penalty = df_final["Alcohol Consumption"].map({"High":2,"Medium":1,"Low":0,"None":0})
sugar_penalty = df_final["Sugar Consumption"].map({"High":2,"Medium":1,"Low":0})
df_final["lifestyle_score"] = (exercise_score + sleep_score -smoking_penalty - alcohol_penalty - sugar_penalty)
HDL_factor = np.where(df_final["Low HDL Cholesterol"]=="Yes",0,50)
df_final["lipid_profile"] = (df_final["Cholesterol Level"] +(df_final["Triglyceride Level"]/2) -HDL_factor)

# Guardar

df_final.to_csv("data/heart_combined_clean.csv", index=False)
print("CSV generado correctamente")
