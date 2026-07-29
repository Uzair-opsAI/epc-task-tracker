import streamlit as st


def metric_card(
    title,
    value,
    icon="📊",
    color="#0E6FFF",
    subtitle=""
):
    """
    Professional KPI Card
    """

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg,#1f2937,#111827);
            border-left:6px solid {color};
            border-radius:14px;
            padding:18px;
            box-shadow:0px 3px 10px rgba(0,0,0,0.25);
            min-height:130px;
        ">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
            ">

                <div style="
                    color:#d1d5db;
                    font-size:15px;
                    font-weight:600;
                ">
                    {title}
                </div>

                <div style="
                    font-size:30px;
                ">
                    {icon}
                </div>

            </div>

            <div style="
                font-size:42px;
                font-weight:bold;
                color:white;
                margin-top:12px;
            ">
                {value}
            </div>

            <div style="
                color:#9ca3af;
                margin-top:8px;
                font-size:13px;
            ">
                {subtitle}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


def success_card(title, value):

    metric_card(
        title,
        value,
        "🟢",
        "#16a34a"
    )


def warning_card(title, value):

    metric_card(
        title,
        value,
        "🟡",
        "#f59e0b"
    )


def danger_card(title, value):

    metric_card(
        title,
        value,
        "🔴",
        "#dc2626"
    )


def info_card(title, value):

    metric_card(
        title,
        value,
        "🔵",
        "#2563eb"
    )
