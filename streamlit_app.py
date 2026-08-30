"""EduPrep — Streamlit app (single file, no subfolders).

Handles login, registration, and password reset against Supabase Auth.
Once signed in, a sidebar menu switches between Catalogue and Profile
views — implemented as functions in this one script instead of a
Streamlit `pages/` folder, so the whole repo is flat files.

Run locally with:
    streamlit run streamlit_app.py
"""

from __future__ import annotations

import streamlit as st

from supabase_client import SupabaseError, get_client

st.set_page_config(page_title="EduPrep", page_icon="📚", layout="centered")


def _init_session_state() -> None:
    st.session_state.setdefault("access_token", None)
    st.session_state.setdefault("user_email", None)


# ---------------------------------------------------------------------------
# Signed-out views: login / register / reset
# ---------------------------------------------------------------------------

def _render_login_tab() -> None:
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Log in", use_container_width=True)
    if submitted:
        try:
            session = get_client().login(email, password)
        except SupabaseError as exc:
            st.error(str(exc))
        else:
            st.session_state["access_token"] = session.get("access_token")
            st.session_state["user_email"] = email
            st.rerun()


def _render_register_tab() -> None:
    with st.form("register_form"):
        email = st.text_input("Email", key="register_email")
        password = st.text_input(
            "Password", type="password", key="register_password",
            help="At least 8 characters.",
        )
        full_name = st.text_input("Full name (optional)", key="register_full_name")
        class_level = st.text_input(
            "Class level (optional)", key="register_class_level",
            placeholder="e.g. SS3",
        )
        submitted = st.form_submit_button("Create account", use_container_width=True)
    if submitted:
        if len(password) < 8:
            st.error("Password must be at least 8 characters.")
            return
        try:
            get_client().register(
                email=email,
                password=password,
                full_name=full_name or None,
                class_level=class_level or None,
            )
        except SupabaseError as exc:
            st.error(str(exc))
        else:
            st.success("Account created. Check your email to confirm, then log in.")


def _render_reset_tab() -> None:
    with st.form("reset_form"):
        email = st.text_input("Email", key="reset_email")
        submitted = st.form_submit_button("Send reset link", use_container_width=True)
    if submitted:
        try:
            get_client().send_password_reset(email)
        except SupabaseError as exc:
            st.error(str(exc))
        else:
            st.success("If an account exists for this email, reset instructions have been sent.")


def _render_signed_out() -> None:
    st.title("📚 EduPrep")
    st.caption("Nigerian WAEC and JAMB exam preparation.")
    login_tab, register_tab, reset_tab = st.tabs(["Log in", "Register", "Forgot password"])
    with login_tab:
        _render_login_tab()
    with register_tab:
        _render_register_tab()
    with reset_tab:
        _render_reset_tab()


# ---------------------------------------------------------------------------
# Signed-in views: catalogue / profile
# ---------------------------------------------------------------------------

def _render_catalogue(token: str) -> None:
    st.title("📚 Catalogue")
    client = get_client()
    try:
        exams = client.list_exams(token)
        subjects = client.list_subjects(token)
    except SupabaseError as exc:
        st.error(str(exc))
        return

    st.subheader("Exams")
    if exams:
        for exam in exams:
            with st.expander(exam["name"]):
                st.write(exam.get("description") or "No description yet.")
    else:
        st.info("No exams have been added yet.")

    st.subheader("Subjects")
    if not subjects:
        st.info("No subjects have been added yet.")
        return

    subject_names = {subject["name"]: subject["id"] for subject in subjects}
    selected_name = st.selectbox("Select a subject to view its topics", list(subject_names))
    if selected_name:
        subject_id = subject_names[selected_name]
        try:
            topics = client.list_topics(subject_id, token)
        except SupabaseError as exc:
            st.error(str(exc))
        else:
            if topics:
                for topic in topics:
                    st.markdown(f"- **{topic['name']}** — {topic.get('description') or 'No description yet.'}")
            else:
                st.info(f"No topics have been added for {selected_name} yet.")


def _render_profile(token: str) -> None:
    st.title("👤 Profile")
    client = get_client()
    try:
        user = client.get_user(token)
        profile = client.get_profile(token, user["id"])
    except SupabaseError as exc:
        st.error(str(exc))
        return

    with st.form("profile_form"):
        full_name = st.text_input("Full name", value=profile.get("full_name") or "")
        class_level = st.text_input(
            "Class level", value=profile.get("class_level") or "", placeholder="e.g. SS3"
        )
        submitted = st.form_submit_button("Save changes")

    if submitted:
        changes = {}
        if full_name != (profile.get("full_name") or ""):
            changes["full_name"] = full_name
        if class_level != (profile.get("class_level") or ""):
            changes["class_level"] = class_level
        if not changes:
            st.info("No changes to save.")
        else:
            try:
                client.update_profile(token, user["id"], changes)
            except SupabaseError as exc:
                st.error(str(exc))
            else:
                st.success("Profile updated.")
                st.rerun()


def _render_signed_in() -> None:
    token = st.session_state["access_token"]
    with st.sidebar:
        st.write(f"Signed in as **{st.session_state['user_email']}**")
        page = st.radio("Menu", ["Catalogue", "Profile"], label_visibility="collapsed")
        if st.button("Log out", use_container_width=True):
            try:
                get_client().logout(token)
            except SupabaseError:
                pass  # Token may already be invalid — clear local state regardless.
            st.session_state["access_token"] = None
            st.session_state["user_email"] = None
            st.rerun()

    if page == "Catalogue":
        _render_catalogue(token)
    else:
        _render_profile(token)


def main() -> None:
    _init_session_state()
    if st.session_state["access_token"]:
        _render_signed_in()
    else:
        _render_signed_out()


main()
