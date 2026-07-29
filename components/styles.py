import streamlit as st


def load_css():
    st.markdown("""
<style>

/* ==========================================================
   GLOBAL
========================================================== */

html,
body,
[class*="css"]{
    font-family: "Segoe UI", sans-serif;
}

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
    max-width:98%;
}

/* ==========================================================
   HEADER
========================================================== */

.main-title{

    font-size:34px;

    font-weight:700;

    color:#1E88E5;

    margin-bottom:2px;

}

.sub-title{

    color:#9aa5b1;

    font-size:15px;

    margin-bottom:25px;

}

/* ==========================================================
   SIDEBAR
========================================================== */

section[data-testid="stSidebar"]{

    background:#16202A;

    border-right:1px solid #263238;

}

section[data-testid="stSidebar"] h1{

    color:white;

}

section[data-testid="stSidebar"] label{

    color:#E8EAF6;

}

/* ==========================================================
   BUTTONS
========================================================== */

.stButton>button{

    background:#1976D2;

    color:white;

    border:none;

    border-radius:10px;

    padding:10px;

    font-weight:600;

    transition:0.3s;

}

.stButton>button:hover{

    background:#1565C0;

    transform:scale(1.02);

}

/* ==========================================================
   SELECTBOX
========================================================== */

.stSelectbox div[data-baseweb="select"]{

    border-radius:8px;

}

/* ==========================================================
   TEXT INPUT
========================================================== */

.stTextInput input{

    border-radius:8px;

}

/* ==========================================================
   TEXT AREA
========================================================== */

textarea{

    border-radius:10px !important;

}

/* ==========================================================
   TABLES
========================================================== */

thead tr th{

    background:#1E88E5 !important;

    color:white !important;

}

tbody tr:hover{

    background:#E3F2FD22;

}

/* ==========================================================
   METRICS
========================================================== */

div[data-testid="metric-container"]{

    background:#1b2430;

    border-radius:12px;

    border-left:5px solid #1976D2;

    padding:15px;

}

/* ==========================================================
   TABS
========================================================== */

button[data-baseweb="tab"]{

    font-weight:600;

}

/* ==========================================================
   EXPANDERS
========================================================== */

.streamlit-expanderHeader{

    font-weight:bold;

}

/* ==========================================================
   SCROLLBAR
========================================================== */

::-webkit-scrollbar{

    width:10px;

}

::-webkit-scrollbar-thumb{

    background:#5c6bc0;

    border-radius:20px;

}

/* ==========================================================
   FOOTER
========================================================== */

footer{

    visibility:hidden;

}

</style>
""", unsafe_allow_html=True)
