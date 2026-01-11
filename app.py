from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from figures import *

# Carrega les dades i divideix en categories algunes variables
df = pd.read_csv("data/heart_combined_clean.csv")
df["age_group"] = pd.cut(df["Age"],bins=[0,30,45,60,75,120],labels=["<30","30-45","45-60","60-75","75+"])
df["metabolic_cat"] = pd.cut(df["metabolic_risk"],bins=[-1,2,4,10],labels=["Baix","Mitjà","Alt"])
df["lifestyle_cat"] = pd.cut(df["lifestyle_score"],bins=[-10,0,3,10],labels=["Pobre","Mitjà","Saludable"])

# CREACIÓ DE FIGURES

# Sankey
flow1 = (df.groupby(["Smoking","metabolic_cat","Heart Disease Status"]).size().reset_index(name="count"))
flow2 = (df.groupby(["Exercise Habits","lifestyle_cat","Heart Disease Status"]).size().reset_index(name="count"))
fig_sankey1 = build_sankey(flow1, "Smoking","metabolic_cat","Heart Disease Status","Flux: Tabac → Risc metabòlic → Malaltia cardíaca")
fig_sankey2 = build_sankey(flow2,"Exercise Habits","lifestyle_cat","Heart Disease Status","Flux: Exercici → Estil de vida → Malaltia cardíaca")

# Parallel
fig_parallel = px.parallel_coordinates(df,dimensions=["Age","BMI","Cholesterol Level","Triglyceride Level","CRP Level","lifestyle_score","metabolic_risk"], color=df["Heart Disease Status"].map({"No":0,"Yes":1}), color_continuous_scale=px.colors.diverging.Tealrose,title="Perfils multivariants de risc")

# Scatter matrix
vars_matrix = ["Age","BMI","Cholesterol Level","Triglyceride Level","CRP Level","lifestyle_score","metabolic_risk"]
fig_matrix = px.scatter_matrix(df,dimensions=vars_matrix,color="metabolic_risk",opacity=0.35,color_continuous_scale="Viridis",title="Matriu de dispersió avançada")
fig_matrix.update_layout(title=dict(text="Matriu de dispersió",x=0.5,xanchor="center",font=dict(size=26)),margin=dict(t=120),height=900)
# Funció per formatejar el tex de les imatges
def story_block(title, text, bullets=None):
    children = [html.H4(title), html.P(text)]
    if bullets:
        children.append(html.Ul([html.Li(b) for b in bullets]))
    return html.Div(children)



# Gràfics de barres multiples
habits = ["Smoking","Exercise Habits","Alcohol Consumption","Sugar Consumption","Stress Level","Sleep Hours"]
df["sleep_cat"] = pd.cut(df["Sleep Hours"],bins=[0,5,7,24],labels=["<5h","5-7h",">7h"])
from plotly.subplots import make_subplots
fig_sm = make_subplots(rows=3, cols=2, subplot_titles=habits)

for i, habit in enumerate(habits):
    row = i//2 + 1
    col = i%2 + 1
    x = "sleep_cat" if habit=="Sleep Hours" else habit
    data = (df.groupby(x)["metabolic_risk"].mean().reset_index())
    fig_sm.add_trace(go.Bar(x=data[x], y=data["metabolic_risk"]),row=row, col=col)

fig_sm.update_layout(title="Hàbits de vida vs risc metabòlic (Small multiples)",height=900)

#DASH

app = Dash(__name__)
app.layout = html.Div([

html.H1("Visualitzacions per datasets sobre la Malaltia Cardíaca", style={"textAlign":"center"}),

html.H2("Procés de creació"),

html.Div([
    html.P(
        "En aquest projecte s'ha seguit un procés estructurat per garantir la qualitat de la visualització final."
    ),
    html.P(
        "S'han descarregat dos conjunts de dades de Kaggle i s'han normalitzat els noms de les variables per assegurar coherència. Els datasets s'han fusionat i s'han imputat valors nuls utilitzant la mediana i la moda segons el tipus de variable."
    ),
    html.P(
        "Un cop preparades les dades, s'han definit preguntes clau sobre el risc cardiovascular i els hàbits de vida."
    ),
    html.P(
        "A partir d'aquestes preguntes, s'han seleccionat els tipus de gràfics més adequats, que es detallaran més endavant."
    ),
    html.P(
        "Finalment, s'han creat indicadors derivats com el risc metabòlic i l'estil de vida per enriquir l'anàlisi."
    )
], style={"maxWidth":"900px","margin":"auto"}),
html.H2("Conjunt de dades"),
html.Div([
    html.P(
        "S'utilitzen dos conjunts de dades de heart-disease de Kaggle: johnsmith88 i oktayrdeki, amb informació clínica i d'estil de vida. Inclouen variables com edat, gènere, colesterol, BMI, hàbits i indicadors bioquímics."
    ),
    html.P(
        "S'ha realitzat un procés de preprocessat que inclou la unificació de columnes, fusió de datasets i tractament de valors nuls."
    )
], style={"maxWidth":"900px","margin":"auto"}),

html.H2("Preguntes clau"),
html.Div([
html.P(
    "La visualització respon a diverses preguntes clau orientades a comprendre els factors de risc associats a la malaltia cardíaca."
),

html.H4("1. Influència dels hàbits de vida"),
html.P("Com influeixen l'exercici, el consum de sucre, el tabac i l'alcohol en la presència de malaltia cardíaca?"
),
html.P(
    "Aquesta pregunta s'aborda mitjançant els diagrames Sankey i els diagrames de barres multiples, que permeten visualitzar la relació entre hàbits, risc metabòlic i malaltia."
),

html.H4("2. Factors metabòlics i Metabolic Risk Index"),
html.P("Quin és el paper del colesterol, triglicèrids, sucre i inflamació en el risc cardíac segons l'índex de risc metabòlic?"
),
html.P(
    "S'analitza mitjançant coordenades paral·leles i matrius de dispersió per identificar perfils multivariants."
),

html.H4("3. Diferències per edat i gènere"),
html.P("Hi ha diferències en el risc cardíac segons grups d'edat i gènere?"
),
html.P(
    "Aquesta qüestió s'explora mitjançant el ridgeline plot i el heatmap dinàmic."
),

html.H4("4. Valor dels indicadors derivats"),
html.P(
    "Els indicadors creats milloren la comprensió del risc respecte a les variables originals?"
),
html.P(
    "S'analitza comparant patrons multivariants i distribucions de risc."
)

], style={"maxWidth":"900px","margin":"auto"}),


html.H3("1. Fluxos de risc (Sankey)"),

story_block(
    "Què pretén respondre?",
    [
        "Aquesta representació preten respondre a la pregunta: com influeixen els hàbits de vida en la presència de malaltia cardíaca?",
        "La idea és transformar variables categòriques (tabac/exercici) en un recorregut causal simplificat cap a un indicador (risc metabòlic o estil de vida) i, finalment, cap a la variable objectiu (malaltia: Sí/No)."
    ],
    bullets=[
        "Limitació: és una visualització descriptiva no prova causalitat, però és molt útil per detectar patrons."
    ]
),

story_block(
    "Interactivitat i accessibilitat",
    [
        "Interactivitat: en passar el cursor pels nodes i fluxos veuràs els recomptes i es ressaltaran les connexions.",
        "Accessibilitat: els fluxos es codifiquen visualment per amplada."
    ]
),

dcc.Graph(figure=fig_sankey1),
dcc.Graph(figure=fig_sankey2),

html.H3("2. Perfils multivariants"),


story_block(
    "Què pretén respondre?",
    [
        "Aquesta figura respon sobretot a: quin és el paper dels factors metabòlics (colesterol, triglicèrids, sucre, inflamació) en el risc de malaltia cardíaca segons el Metabolic Risk Index?",
        "En lloc de mirar variables d'una en una, aquí busquem perfils complets: combinacions de valors que tendeixen a aparèixer juntes en persones amb i sense malaltia."
    ]
),

story_block(
    "Interactivitat i accessibilitat",
    [
        "Interactivitat (Plotly): pots seleccionar rangs en un o més eixos per filtrar visualment i veure quines línies compleixen un patró.",
        "Accessibilitat: les coordenades paral·leles poden ser denses"
    ]
),


dcc.Graph(figure=fig_parallel),

html.H3("3. Mapa de correlacions (dinàmic)"),

story_block(
    "Què pretén respondre?",
    [
        "Aquesta secció respon a: hi ha diferències en el risc cardíac entre grups d'edat?"
    ],
    bullets=[
        "Què s'hi veu: correlacions entre variables clíniques i indicadors derivats on valors propers a +1 indiquen relació positiva, propers a -1 relació inversa."
    ]
),

story_block(
    "Interactivitat i accessibilitat",
    [
        "Interactivitat (Plotly): hover sobre cada cel·la per veure el valor exacte; zoom per inspeccionar zones concretes.",
        "Accessibilitat: escala de colors divergent + números sobre les cel·les ajuda a no dependre només del color."
    ]
),

dcc.Graph(figure=correlation_heatmap(df, "All", "All", "All")),

html.H3("4. Ridgeline"),

story_block(
    "Què pretén respondre?",
    [
        "Aquesta figura complementa la pregunta de diferències per edat i gènere. L'objectiu és veure com es distribueix el Metabolic Risk Index en diferents franges d'edat, separant homes i dones."
    ],
    bullets=[
        "Cada “cresta” mostra la densitat del risc metabòlic per un grup. Si una cresta està desplaçada cap a valors alts, aquell grup tendeix a tenir més risc metabòlic."
    ]
),
story_block(
    "Interactivitat i accessibilitat",
    [
        "Interactivitat (Plotly): es poden selecionar els grups i zoom per comparar millor crestes properes."
    ]
),

dcc.Graph(figure=ridgeline_plot(df)),

html.H3("5. Matriu de dispersió"),

story_block(
    "Què pretén respondre?",
    [
        "Aquesta matriu dona suport a dues preguntes: (1) paper dels factors metabòlics i (2) si els indicadors derivats aporten valor respecte a variables originals. Aquí es busquen relacions per parelles i patrons de separació segons el risc metabòlic."
    ],
    bullets=[
        "Cada cel·la és un scatter entre dues variables, on el color codifica el Metabolic Risk Index. De manera que núvols inclinats suggereixen correlació"
    ]
),

story_block(
    "Interactivitat i accessibilitat",
    [
        "Interactivitat (Plotly): zoom i selecció per explorar subconjunts",
        "Accessibilitat: evita dependre només del color"
    ]
),


dcc.Graph(figure=fig_matrix),

html.H3("6. Hàbits vs risc metabòlic"),

story_block(
    "Què pretén respondre?",
    [
        "Aquesta secció aterra la pregunta principal sobre hàbits: com canvia el risc metabòlic segons tabac, exercici, alcohol, sucre, estrès i son?"
    ]
),

story_block(
    "Interactivitat i accessibilitat",
    [
        "Interactivitat (Plotly): hover per veure el valor exacte; zoom si vols inspeccionar categories.",
        "Accessibilitat: escales compartides + títols clars ajuden molt."
    ]
),

dcc.Graph(figure=fig_sm),

html.H2("Reflexió final"),

html.Div([
    html.P(
        "Aquest projecte m'ha permès aprendre a combinar fonts de dades, crear indicadors derivats i seleccionar visualitzacions adequades."
    ),
    html.P(
        "Com a limitacions, destaca la qualitat desigual de les dades i la manca de variables clíniques més específiques."
    ),
    html.P(
        "M'hauria agradat incorporar més interacció entre gràfics i filtres, però el temps ho ha limitat."
    )
], style={"maxWidth":"900px","margin":"auto"})

])

app.run(debug=True)
