import streamlit as st
from contextlib import contextmanager

from components.theme import *

# ============================================================
# Enterprise Dashboard Card
# ============================================================

@contextmanager
def dashboard_card(
    title,
    icon="📊",
    subtitle=None
):
    """
    Enterprise Dashboard Container

    Usage:

    with dashboard_card(
        "Project Health",
        "🏗"
    ):
        st.plotly_chart(fig)
    """

    st.markdown(
        f"""
        <div style="
            background:{CARD_BACKGROUND};
            border-radius:{CARD_RADIUS};
            padding:{CARD_PADDING};
            margin-bottom:20px;
            box-shadow:{CARD_SHADOW};
            border-top:5px solid {PRIMARY};
        ">
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            display:flex;
            align-items:center;
            gap:10px;
            margin-bottom:6px;
        ">

            <div style="
                font-size:26px;
            ">
                {icon}
            </div>

            <div>

                <div style="
                    font-size:20px;
                    font-weight:700;
                    color:{TEXT_PRIMARY};
                ">
                    {title}
                </div>

                <div style="
                    color:{TEXT_SECONDARY};
                    font-size:13px;
                ">
                    {subtitle if subtitle else ""}
                </div>

            </div>

        </div>

        <hr style="
            margin-top:10px;
            margin-bottom:15px;
            border:1px solid #ECECEC;
        ">
        """,
        unsafe_allow_html=True
    )

    yield

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )
