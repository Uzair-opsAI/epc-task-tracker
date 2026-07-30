import streamlit as st


def load_css():

    st.markdown(
        """
<style>

/* ===========================================================
   GLOBAL
=========================================================== */

html,
body,
[class*="css"]{

    font-family: "Segoe UI", sans-serif;

}

.block-container{

    max-width:95%;

    padding-top:1.2rem;

    padding-bottom:1rem;

}

/* ===========================================================
   HEADER
=========================================================== */

h1{

    color:#1565C0;

    font-weight:700;

}

h2{

    color:#1E3A5F;

}

h3{

    color:#1E3A5F;

}

/* ===========================================================
   SIDEBAR
=========================================================== */

section[data-testid="stSidebar"]{

    background:#15202B;

    border-right:2px solid #1E88E5;

}

section[data-testid="stSidebar"] *{

    color:white;

}

section[data-testid="stSidebar"] hr{

    border-color:#37474F;

}

/* ===========================================================
   METRIC CARDS
=========================================================== */

div[data-testid="metric-container"]{

    background:white;

    border-radius:14px;

    padding:18px;

    border:1px solid #E5E7EB;

    box-shadow:0px 2px 8px rgba(0,0,0,0.08);

    transition:0.25s;

}

div[data-testid="metric-container"]:hover{

    transform:translateY(-3px);

    box-shadow:0px 6px 16px rgba(0,0,0,0.15);

}

/* ===========================================================
   BUTTONS
=========================================================== */

.stButton>button{

    width:100%;

    border-radius:10px;

    background:#1976D2;

    color:white;

    border:none;

    padding:10px;

    font-weight:600;

}

.stButton>button:hover{

    background:#1565C0;

}

/* ===========================================================
   INPUTS
=========================================================== */

.stSelectbox div[data-baseweb="select"]{

    border-radius:10px;

}

.stTextInput input{

    border-radius:10px;

}

textarea{

    border-radius:10px !important;

}

/* ===========================================================
   DATAFRAMES
=========================================================== */

thead tr th{

    background:#1976D2 !important;

    color:white !important;

}

tbody tr:hover{

    background:#E3F2FD !important;

}

/* ===========================================================
   TABS
=========================================================== */

button[data-baseweb="tab"]{

    font-weight:600;

    font-size:15px;

}

/* ===========================================================
   EXPANDER
=========================================================== */

.streamlit-expanderHeader{

    font-weight:700;

}

/* ===========================================================
   ALERT BOXES
=========================================================== */

div[data-baseweb="notification"]{

    border-radius:10px;

}

/* ===========================================================
   PLOTLY
=========================================================== */

.js-plotly-plot{

    border-radius:14px;

}

/* ===========================================================
   SCROLLBAR
=========================================================== */

::-webkit-scrollbar{

    width:8px;

}

::-webkit-scrollbar-thumb{

    background:#90CAF9;

    border-radius:10px;

}

/* ===========================================================
   FOOTER
=========================================================== */

footer{

    visibility:hidden;

}

#MainMenu{

    visibility:hidden;

}

header{

    visibility:hidden;

}

</style>
""",
        unsafe_allow_html=True
    )
