import plotly.express as px
import streamlit as st


def buyer_persona_chart(df):

    persona = (
        df["Buyer_Persona"]
        .value_counts()
        .reset_index()
    )

    persona.columns = [
        "Buyer Persona",
        "Count"
    ]

    fig = px.bar(
        persona,
        x="Buyer Persona",
        y="Count",
        color="Buyer Persona",
        text="Count",
        title="Buyer Persona Distribution"
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        template="plotly_white",
        height=450,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)