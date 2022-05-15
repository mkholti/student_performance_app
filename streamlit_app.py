import pandas as pd
import streamlit as st

from utils import calculate_matiere_stats


st.set_page_config(
    page_title="Performance des élèves", page_icon="⬇",layout="centered")


st.title("⬇ Performances des élèves")

st.markdown("### Etablissement")
school = st.selectbox(
    "Selectionner l'établissement", ["Gabriel Pereira", "Mousinho da Silveira"]
)

school_map = {"Gabriel Pereira": "GP", "Mousinho da Silveira": "MS"}


# load data

df_por = pd.read_csv("student-por.csv", sep=";")
df_por["matière"] = "por"

df_mat = pd.read_csv("student-mat.csv", sep=";")
df_mat["matière"] = "mat"
data_df = pd.concat([df_mat, df_por])

# filter on school data
data_school = data_df.loc[data_df["school"]==school_map[school]]
mat_scool = df_mat.loc[df_mat["school"]==school_map[school]]
por_scool = df_por.loc[df_por["school"]==school_map[school]]


st.write("Suivre Tes élèves en regardant de près ceux en difficultés !")
st.markdown("## 1. Performance globale")

# stats performance globale
matiere_note_stats = calculate_matiere_stats(data_school)

col1, col2, col3 = st.columns(3)
st.write("Moyenne de la note globale au sein de l'établissement")
st.dataframe(data=matiere_note_stats)


st.markdown("## 2. Notes des élèves en difficultés")

# worst student
worst_math = mat_scool.sort_values(["G3", "G2", "G1"])[["G1", "G2", "G3"]].head()
worst_por = por_scool.sort_values(["G3", "G2", "G1"])[["G1", "G2", "G3"]].head()

col1, col2 = st.columns(2)

with col1:
    st.write("Les élèves en difficultés en mathématiques")
    st.dataframe(data=worst_math)

with col2:
    st.write("Les élèves en difficultés en portugais")
    st.dataframe(data=worst_por)


st.markdown("## 3. Indicateur de performance des élèves en difficultés")

matiere = st.selectbox(
    "Selectionner la matière", ["Mathématique", "Portugais"]
)

if matiere=="Mathématique":
    worst_student_df = mat_scool.loc[mat_scool["G3"]<matiere_note_stats.loc["Mathématiques", "Moyenne"]].sort_values(["G3", "G2", "G1"])
    student_df = mat_scool
elif matiere=="Portugais":
    worst_student_df = por_scool.loc[por_scool["G3"]<matiere_note_stats.loc["Mathématiques", "Moyenne"]].sort_values(["G3", "G2", "G1"])
    student_df = por_scool

worst_indicators = {}
all_student_indicators = {}

all_student_indicators["absences"] = student_df["absences"].mean()
worst_indicators["absences"] = worst_student_df["absences"].mean()

all_student_indicators["studytime"] = student_df["studytime"].mean()
worst_indicators["studytime"] = worst_student_df["studytime"].mean()

all_student_indicators["health"] = student_df["health"].mean()
worst_indicators["health"] = worst_student_df["health"].mean()


col1, col2 = st.columns(2)
with col1:
    st.write("Les élèves en difficultés")
    st.dataframe(data=pd.DataFrame([worst_indicators]))

with col2:
    st.write("Tous les élèves")
    st.dataframe(data=pd.DataFrame([all_student_indicators]))