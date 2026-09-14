import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sympy import sympify, lambdify, symbols

st.set_page_config(
    page_title="ГРАФИКЫЫ",
    layout="centered", 
    initial_sidebar_state="collapsed"
)
st.title("Графк")

st.sidebar.header("Настройки")
formula_input = st.sidebar.text_input(
    "Введите функцию", 
    value="x^3 - 3*x"
)
col1, col2 = st.sidebar.columns(2)
with col1:
    x_min = st.number_input("X min", value=-10.0, step=1.0)
    y_min = st.number_input("Y min", value=-10.0, step=1.0)
with col2:
    x_max = st.number_input("X max", value=10.0, step=1.0)
    y_max = st.number_input("Y max", value=10.0, step=1.0)

keep_aspect_ratio = st.sidebar.checkbox("", value=True)

if formula_input:
    try:
        x_sym = symbols('x')
        formatted_str = formula_input.replace('^', '**')
        expr = sympify(formatted_str)
        
        f = lambdify(x_sym, expr, modules=['numpy'])

        step = 0.1
        num_points = int(np.round((x_max - x_min) / step)) + 1
        x_vals = np.linspace(x_min, x_max, num_points)
        x_vals = np.round(x_vals, 1)

        y_vals = f(x_vals)

        if isinstance(y_vals, (int, float)):
            y_vals = np.full_like(x_vals, float(y_vals))
        dy = np.abs(np.diff(y_vals, prepend=y_vals[0]))
        y_vals[dy > (y_max - y_min) * 2] = np.nan
        hover_labels = [
            f"X: {x:.1f}<br>Y: {y:.2f}" if not np.isnan(y) else ""
            for x, y in zip(x_vals, y_vals)
        ]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_vals, 
            y=y_vals, 
            mode='lines', 
            name=f'y = {formula_input}',
            line=dict(color='#00F5D4', width=2.5),
            hoverinfo='text',
            hovertext=hover_labels
        ))
        fig.add_hline(y=0, line_width=2, line_color="#FFFFFF", opacity=0.8)
        fig.add_vline(x=0, line_width=2, line_color="#FFFFFF", opacity=0.8)

        yaxis_dict = dict(
            range=[y_min, y_max],
            zeroline=False,
            showgrid=True,
            gridcolor='#333333'
        )
        if keep_aspect_ratio:
            yaxis_dict["scaleanchor"] = "x"
            yaxis_dict["scaleratio"] = 1

        fig.update_layout(
            title=f"График функции:",
            xaxis=dict(
                range=[x_min, x_max],
                zeroline=False,
                showgrid=True,
                gridcolor='#333333'
            ),
            yaxis=yaxis_dict,
            paper_bgcolor="#111111",
            plot_bgcolor="#1E1E1E",
            font=dict(color="#EEEEEE"),
            hovermode="x",
            height=650
        )
        st.plotly_chart(
            fig, 
            width="stretch", 
            config={'displayModeBar': False}
        )
    except Exception as e:
        st.error(f"Eror")
