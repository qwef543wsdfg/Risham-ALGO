"""
Load external CSS stylesheets for the Streamlit interface.
"""

from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSS_DIRECTORY = (
    PROJECT_ROOT
    / "assets"
    / "css"
)


def _inject_css(css_file: Path) -> None:
    """
    Read a CSS file and inject it into Streamlit.
    """

    css_content = css_file.read_text(
        encoding="utf-8"
    )

    st.markdown(
        f"<style>{css_content}</style>",
        unsafe_allow_html=True,
    )


def apply_theme() -> None:
    """
    Load every CSS stylesheet inside assets/css.
    """

    if not CSS_DIRECTORY.exists():

        st.warning(
            f"CSS directory not found:\n{CSS_DIRECTORY}"
        )

        return

    css_files = sorted(
        CSS_DIRECTORY.glob("*.css")
    )

    if not css_files:

        st.warning(
            "No CSS stylesheets were found."
        )

        return

    for css_file in css_files:

        try:

            _inject_css(css_file)

        except OSError as error:

            st.error(
                f"Unable to load {css_file.name}\n\n{error}"
            )