import streamlit as st
import numpy as np

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="🎮",
    layout="centered"
)

# -----------------------------
# Initialize game
# -----------------------------
if "board" not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)

if "current" not in st.session_state:
    st.session_state.current = 1

if "winner" not in st.session_state:
    st.session_state.winner = None


# -----------------------------
# Check winner
# -----------------------------
def check_winner(b):

    # Rows
    if 3 in np.sum(b, axis=1):
        return "X"

    if -3 in np.sum(b, axis=1):
        return "O"

    # Columns
    if 3 in np.sum(b, axis=0):
        return "X"

    if -3 in np.sum(b, axis=0):
        return "O"

    # Diagonals
    if np.trace(b) == 3:
        return "X"

    if np.trace(b) == -3:
        return "O"

    if np.trace(np.fliplr(b)) == 3:
        return "X"

    if np.trace(np.fliplr(b)) == -3:
        return "O"

    # Draw
    if not np.any(b == 0):
        return "DRAW"

    return None


# -----------------------------
# Make a move
# -----------------------------
def make_move(row, col):

    board = st.session_state.board

    # Don't allow move if cell is occupied
    if board[row, col] != 0:
        st.warning("⚠️ This cell is already taken!")
        return

    # Don't allow moves after game ends
    if st.session_state.winner is not None:
        return

    # Place player's move
    board[row, col] = st.session_state.current

    # Check winner
    result = check_winner(board)

    if result is not None:
        st.session_state.winner = result
    else:
        # Switch player
        if st.session_state.current == 1:
            st.session_state.current = -1
        else:
            st.session_state.current = 1


# -----------------------------
# Reset game
# -----------------------------
def reset_game():

    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1
    st.session_state.winner = None


# -----------------------------
# UI
# -----------------------------
st.title("🎮 Tic Tac Toe")
st.write("### NumPy + Streamlit")

st.divider()

# Game status
if st.session_state.winner == "DRAW":

    st.success("🤝 It's a Draw!")

elif st.session_state.winner is not None:

    st.success(f"🎉 Player {st.session_state.winner} Wins!")

else:

    if st.session_state.current == 1:
        st.info("👉 Player X's Turn")
    else:
        st.info("👉 Player O's Turn")


# -----------------------------
# Board
# -----------------------------
board = st.session_state.board

symbols = {
    0: " ",
    1: "❌",
    -1: "⭕"
}

for row in range(3):

    cols = st.columns(3)

    for col in range(3):

        value = board[row, col]

        # Button label
        if value == 0:
            label = " "
        else:
            label = symbols[value]

        # Unique button key
        if cols[col].button(
            label,
            key=f"cell_{row}_{col}",
            use_container_width=True
        ):
            make_move(row, col)
            st.rerun()


st.divider()

# Reset button
if st.button("🔄 New Game", use_container_width=True):
    reset_game()
    st.rerun()