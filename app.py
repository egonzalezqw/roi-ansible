import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Linux Lab Game", layout="centered")

# ----------------------
# QUESTIONS / CHALLENGES
# ----------------------
challenges = [
    {"q": "List all files in the current directory", "a": "ls"},
    {"q": "Copy all .txt files to folder red", "a": "cp *.txt red/"},
    {"q": "Move all .log files to folder blue", "a": "mv *.log blue/"},
    {"q": "Delete files starting with eliminar with confirmation", "a": "rm -i eliminar*"},
    {"q": "Create backup/2026/marzo in one command", "a": "mkdir -p backup/2026/marzo"},
    {"q": "Remove non-empty directory test_directory safely", "a": "rm -ri test_directory"},
    {"q": "Copy directory red into backup", "a": "cp -r red backup/"},
    {"q": "List hidden files", "a": "ls -a"},
    {"q": "Show current directory path", "a": "pwd"},
    {"q": "Change permissions to executable for all", "a": "chmod a+x archivo"},
    {"q": "Find command location for ls", "a": "which ls"},
    {"q": "Display PATH variable", "a": "echo $PATH"}
]

# ----------------------
# SESSION STATE
# ----------------------
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.name = ""

# ----------------------
# TITLE
# ----------------------
st.title("🐧 Linux Challenge Game - NDG I")

# ----------------------
# NAME INPUT
# ----------------------
if st.session_state.name == "":
    name = st.text_input("Enter your name:")
    if st.button("Start Game"):
        if name:
            st.session_state.name = name
            random.shuffle(challenges)
            st.rerun()

# ----------------------
# GAME
# ----------------------
else:
    if st.session_state.index < len(challenges):
        c = challenges[st.session_state.index]

        st.subheader(f"Challenge {st.session_state.index + 1}")
        st.write(c["q"])

        answer = st.text_input("Your command:", key=st.session_state.index)

        if st.button("Submit"):
            if answer.strip().lower() == c["a"]:
                st.success("✅ Correct!")
                st.session_state.score += 10
            else:
                st.error(f"❌ Incorrect. Expected: {c['a']}")
                st.session_state.score -= 2

            st.session_state.index += 1
            st.rerun()

        st.progress(st.session_state.index / len(challenges))
        st.write(f"Score: {st.session_state.score}")

    else:
        st.success("🎉 Game Finished!")
        st.write(f"Player: {st.session_state.name}")
        st.write(f"Final Score: {st.session_state.score}")

        # SAVE SCORES
        try:
            df = pd.read_csv("scores.csv")
        except:
            df = pd.DataFrame(columns=["name", "score"])

        new = pd.DataFrame([[st.session_state.name, st.session_state.score]], columns=["name", "score"])
        df = pd.concat([df, new], ignore_index=True)
        df = df.sort_values(by="score", ascending=False)
        df.to_csv("scores.csv", index=False)

        st.subheader("🏆 TOP PLAYERS")

        if len(df) > 0:
            st.write(f"🥇 1st: {df.iloc[0]['name']} - {df.iloc[0]['score']}")
        if len(df) > 1:
            st.write(f"🥈 2nd: {df.iloc[1]['name']} - {df.iloc[1]['score']}")
        if len(df) > 2:
            st.write(f"🥉 3rd: {df.iloc[2]['name']} - {df.iloc[2]['score']}")

        st.dataframe(df)

        if st.button("Play Again"):
            st.session_state.index = 0
            st.session_state.score = 0
            st.session_state.name = ""
            st.rerun()
