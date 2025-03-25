import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Charger les données
df = pd.read_excel('last.xlsx')

# Filtrer les donneurs temporairement non éligibles
df_temp_non_eligible = df[df['ÉLIGIBILITÉ_AU_DON.'] == 'Temporairement Non-eligible']

# Séparer les hommes et les femmes
df_temp_men = df_temp_non_eligible[df_temp_non_eligible['Genre_'] == 'Homme']
df_temp_women = df_temp_non_eligible[df_temp_non_eligible['Genre_'] == 'Femme']

# Définir une palette de couleurs
color_men = '#1f77b4'
color_women = '#ff7f0e'

# Fonction pour générer un graphique Plotly
def plot_top4_demographic(data_men, data_women, column, title_prefix, orientation='v'):
    count_men = data_men[column].value_counts()
    count_women = data_women[column].value_counts()
    
    all_categories = pd.concat([count_men, count_women], axis=1, sort=False).fillna(0)
    all_categories.columns = ['Hommes', 'Femmes']
    all_categories['Total'] = all_categories['Hommes'] + all_categories['Femmes']
    top4_categories = all_categories.sort_values('Total', ascending=False).head(4).index
    
    count_men = count_men[count_men.index.isin(top4_categories)]
    count_women = count_women[count_women.index.isin(top4_categories)]
    
    fig = go.Figure()
    
    if orientation == 'v':
        fig.add_trace(go.Bar(x=count_men.index, y=count_men.values, name='Hommes', marker_color=color_men))
        fig.add_trace(go.Bar(x=count_women.index, y=count_women.values, name='Femmes', marker_color=color_women))
        fig.update_layout(xaxis_title=column, yaxis_title='Nombre de donneurs')
    else:
        fig.add_trace(go.Bar(y=count_men.index, x=count_men.values, name='Hommes', marker_color=color_men, orientation='h'))
        fig.add_trace(go.Bar(y=count_women.index, x=count_women.values, name='Femmes', marker_color=color_women, orientation='h'))
        fig.update_layout(xaxis_title='Nombre de donneurs', yaxis_title=column)
    
    return fig

# Interface Streamlit
st.title("Analyse des donneurs temporairement non éligibles")

demographic_columns = {
    'Classe_Age': 'Tranche d\'âge',
    'categories': 'Catégories professionnelles',
    'Arrondissement_de_résidence_': 'Arrondissement de résidence',
    'Raison_indisponibilité_fusionnée': 'Raisons d’inéligibilité'
}

selected_column = st.selectbox("Sélectionnez une catégorie à analyser", list(demographic_columns.keys()), format_func=lambda x: demographic_columns[x])

graph_orientation = 'h' if selected_column in ['categories', 'Arrondissement_de_résidence_', 'Raison_indisponibilité_fusionnée'] else 'v'

st.plotly_chart(plot_top4_demographic(df_temp_men, df_temp_women, selected_column, "Profil des donneurs", orientation=graph_orientation))

st.subheader("Résumé des profils")
st.write(f"**Nombre total d'hommes:** {len(df_temp_men)}")
st.write(f"**Nombre total de femmes:** {len(df_temp_women)}")

st.subheader("Top 4 par catégorie")
st.write("### Hommes")
st.write(df_temp_men[selected_column].value_counts().head(4))
st.write("### Femmes")
st.write(df_temp_women[selected_column].value_counts().head(4))
