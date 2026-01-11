# figures.py
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# SANKEY

def build_sankey(flow, col1, col2, col3, title):

    labels = list(pd.concat([flow[col1],flow[col2],flow[col3]]).unique())
    label_map = {k:i for i,k in enumerate(labels)}
    source,target,value = [],[],[]
    for _,r in flow.groupby([col1,col2])["count"].sum().reset_index().iterrows():
        source.append(label_map[r[col1]])
        target.append(label_map[r[col2]])
        value.append(r["count"])
    for _,r in flow.groupby([col2,col3])["count"].sum().reset_index().iterrows():
        source.append(label_map[r[col2]])
        target.append(label_map[r[col3]])
        value.append(r["count"])
    fig = go.Figure(go.Sankey(node=dict(label=labels),link=dict(source=source,target=target,value=value)))
    fig.update_layout(title=title)
    return fig


# HEATMAP

def correlation_heatmap(df, gender, age_group, target):
    dff = df.copy()
    if gender!="All":
        dff = dff[dff["Gender"]==gender]
    if age_group!="All":
        dff = dff[dff["age_group"]==age_group]
    if target!="All":
        dff = dff[dff["Heart Disease Status"]==target]
    cols = ["Age","BMI","Cholesterol Level","Triglyceride Level","CRP Level","lifestyle_score","metabolic_risk"]
    corr = dff[cols].corr()
    fig = px.imshow(
        corr,text_auto=".2f",
        color_continuous_scale="RdBu",
        zmin=-1,zmax=1
    )
    return fig


# RIDGELINE
def ridgeline_plot(df):
    fig = go.Figure()
    age_groups = df["age_group"].dropna().unique()
    genders = ["Male","Female"]
    y_shift = 0
    for g in genders:
        for a in age_groups:
            sub = df[(df["Gender"]==g) &(df["age_group"]==a)]
            if len(sub)<10:
                continue
            hist,bins = np.histogram(sub["metabolic_risk"],bins=20,density=True)
            fig.add_trace(go.Scatter(x=bins[:-1],y=hist+y_shift,fill="tozeroy",name=f"{g}|{a}",opacity=0.7))
            y_shift+=0.4

    return fig
