from pathlib import Path
from random import randrange

import streamlit as st
from src.styles.menu_styles import FOOTER_STYLES, HEADER_STYLES

from src.utils.conversation import get_user_input, show_chat_buttons, show_conversation
from src.utils.footer import show_donates, show_info
from src.utils.helpers import get_files_in_dir, get_random_img
from src.utils.lang import en, ru
from streamlit_option_menu import option_menu

# --- PATH SETTINGS ---
current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file: Path = current_dir / "src/styles/.css"
assets_dir: Path = current_dir / "assets"
icons_dir: Path = assets_dir / "icons"
img_dir: Path = assets_dir / "img"
tg_svg: Path = icons_dir / "tg.svg"


# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "AI Talks"
PAGE_ICON: str = "🤖"
LANG_EN: str = "En"
LANG_RU: str = "Ru"
AI_MODEL_OPTIONS: list[str] = [
    "gpt-4-1106-preview",
    "gpt-4-vision-preview",
    "gpt-4",
    "gpt-4-32k",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
]
VOICE_OPTIONS: list[str] = [
    "alloy",
    "echo",
    "fable",
    "onyx",
    "nova",
    "shimmer"
]

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


# --- LOAD CSS ---
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

selected_lang = option_menu(
    menu_title=None,
    options=[LANG_EN, LANG_RU, ],
    icons=["globe2", "translate"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles=HEADER_STYLES
)


# openai.api_key = st.secrets['api_secret']
API_O = st.text_input(
    ":blue[Enter Your OPENAI API-KEY :]",
    placeholder="Paste your OpenAI API key here (sk-...)",
    type="password",
)


# Storing The Context
if "locale" not in st.session_state:
    st.session_state.locale = en
if "generated" not in st.session_state:
    st.session_state.generated = []
if "past" not in st.session_state:
    st.session_state.past = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "input_kind" not in st.session_state:
    st.session_state.input_kind = st.session_state.locale.input_kind_1
if "seed" not in st.session_state:
    st.session_state.seed = randrange(10**3)  # noqa: S311
if "costs" not in st.session_state:
    st.session_state.costs = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = []
if "voice" not in st.session_state:
    st.session_state.voice = VOICE_OPTIONS[0]


def main() -> None:
    c1, c2, c3 = st.columns(3)

    with c1:
        c1.selectbox(
            label=st.session_state.locale.select_placeholder1, 
            options=AI_MODEL_OPTIONS, 
            key="model"
        )
        role_kind = c1.radio(
            label=st.session_state.locale.radio_placeholder,
            options=(st.session_state.locale.radio_text1, st.session_state.locale.radio_text2),
            horizontal=True,
        )

    with c2:
        st.session_state.input_kind = c2.radio(
            label=st.session_state.locale.input_kind,
            options=(st.session_state.locale.input_kind_1, st.session_state.locale.input_kind_2),
            horizontal=True,
        )
        
        if role_kind == st.session_state.locale.radio_text1:
            c2.selectbox(
                label=st.session_state.locale.select_placeholder2, 
                options=st.session_state.locale.ai_role_options, 
                key="role"
            )
        elif role_kind == st.session_state.locale.radio_text2:
            c2.text_input(
                label=st.session_state.locale.select_placeholder3, 
                key="role"
            )

    with c3:
        c3.selectbox(
            label=st.session_state.locale.select_placeholder4, 
            options=VOICE_OPTIONS, 
            key="voice"
        )

    if st.session_state.user_text:
        show_conversation(API_O)
        st.session_state.user_text = ""
    get_user_input()
    show_chat_buttons()


def run_agi():
    if selected_lang == "En":
        st.session_state.locale = en
    elif selected_lang == "Ru":
        st.session_state.locale = ru
    else:
        st.session_state.locale = en

    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.locale.title}</h1>", unsafe_allow_html=True)
    
    selected_footer = option_menu(
        menu_title=None,
        options=[
            st.session_state.locale.footer_option1,
            st.session_state.locale.footer_option0,
            st.session_state.locale.footer_option2,
        ],
        icons=["info-circle", "chat-square-text", "piggy-bank"],  # https://icons.getbootstrap.com/
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles=FOOTER_STYLES
    )

    if selected_footer == st.session_state.locale.footer_option0:
        main()
    elif selected_footer == st.session_state.locale.footer_option1:
        st.image(f"{img_dir}/{get_random_img(get_files_in_dir(img_dir))}")
        show_info(tg_svg)
    elif selected_footer == st.session_state.locale.footer_option2:
        show_donates()
    else:
        show_info(tg_svg)



if __name__ == "__main__":
    run_agi()
