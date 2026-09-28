"""Small visual layer for the VisionControl Streamlit dashboard."""

import streamlit as st


def render_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --vc-bg: #0B0F14;
            --vc-panel: #131A22;
            --vc-panel-raised: #18212B;
            --vc-border: #2B3744;
            --vc-text: #E6EDF3;
            --vc-muted: #AAB6C2;
            --vc-accent: #22D3A6;
            --vc-amber: #F2C46B;
        }
        [data-testid="stAppViewContainer"] { background: var(--vc-bg); }
        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stSidebar"] { border-right: 1px solid var(--vc-border); }
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--vc-panel);
            border-color: var(--vc-border);
            border-radius: 12px;
        }
        [data-testid="stMetric"] {
            background: var(--vc-panel-raised);
            border: 1px solid var(--vc-border);
            border-radius: 10px;
            padding: 12px 14px;
        }
        [data-testid="stMetricLabel"] { color: var(--vc-muted); }
        .vc-eyebrow {
            color: var(--vc-accent);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }
        .vc-title {
            color: var(--vc-text);
            font-family: Georgia, serif;
            font-size: 2.5rem;
            line-height: 1.08;
            margin: 0.15rem 0 0.3rem;
        }
        .vc-subtitle { color: var(--vc-muted); font-size: 0.95rem; }
        .vc-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            border: 1px solid currentColor;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 700;
            line-height: 1;
            padding: 0.55rem 0.8rem;
            white-space: nowrap;
        }
        .vc-status-pill::before {
            background: currentColor;
            border-radius: 50%;
            content: "";
            height: 0.48rem;
            width: 0.48rem;
        }
        .vc-status-on { color: var(--vc-accent); background: #102A25; }
        .vc-status-paused { color: var(--vc-amber); background: #2A2417; }
        .vc-status-no-hand { color: var(--vc-muted); background: var(--vc-panel-raised); }
        .vc-section-label {
            color: var(--vc-muted);
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        .vc-gesture-grid {
            display: grid;
            gap: 0.75rem;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        }
        .vc-gesture-card {
            background: var(--vc-panel);
            border: 1px solid var(--vc-border);
            border-radius: 10px;
            min-height: 116px;
            padding: 0.85rem;
        }
        .vc-gesture-card.is-active {
            border-color: var(--vc-accent);
            box-shadow: 0 0 0 1px var(--vc-accent), 0 0 18px #22D3A633;
        }
        .vc-gesture-icon { font-size: 1.45rem; line-height: 1; }
        .vc-gesture-name { color: var(--vc-text); font-weight: 700; margin-top: 0.65rem; }
        .vc-gesture-action { color: var(--vc-muted); font-size: 0.86rem; margin-top: 0.2rem; }
        .vc-hint { color: var(--vc-muted); font-size: 0.85rem; margin-top: 0.35rem; }
        @media (max-width: 900px) {
            .vc-title { font-size: 2rem; }
            .vc-gesture-grid { grid-template-columns: repeat(auto-fit, minmax(135px, 1fr)); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )