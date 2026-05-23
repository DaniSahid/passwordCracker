"""
=============================================================
  PASSWORD CRACKING SIMULATOR — Interactive Streamlit App
  CSC662 - Computer Security | Cyber Security Awareness Project
  UiTM Faculty of Computer and Mathematical Sciences
=============================================================
"""

import streamlit as st
import time
import string
import itertools
import csv
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Password Cracking Simulator",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS — Dark terminal aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; }

.stApp { background: #0a0e1a; color: #c8d8e8; }

[data-testid="stSidebar"] {
    background: #0d1220;
    border-right: 1px solid #1e3a5f;
}

.hero-header { font-family: 'Share Tech Mono', monospace; text-align: center; padding: 2rem 0 1rem; }
.hero-title  { font-size: 2.8rem; color: #00d4ff; text-shadow: 0 0 20px rgba(0,212,255,0.5); margin: 0; letter-spacing: 3px; }
.hero-sub    { font-size: 1rem; color: #4a7a9b; margin-top: 0.3rem; letter-spacing: 2px; }
.hero-warning {
    display: inline-block; background: rgba(255,100,0,0.1);
    border: 1px solid #ff6400; color: #ff6400;
    padding: 0.4rem 1.2rem; border-radius: 3px;
    font-family: 'Share Tech Mono', monospace; font-size: 0.8rem;
    letter-spacing: 2px; margin-top: 0.5rem;
}

.terminal-box {
    background: #050810; border: 1px solid #1e3a5f; border-radius: 6px;
    padding: 1.5rem; font-family: 'Share Tech Mono', monospace;
    font-size: 0.9rem; margin: 1rem 0;
    box-shadow: 0 0 20px rgba(0,212,255,0.05);
}
.terminal-title {
    color: #00d4ff; font-size: 0.75rem; letter-spacing: 3px;
    border-bottom: 1px solid #1e3a5f; padding-bottom: 0.5rem; margin-bottom: 1rem;
}
.terminal-line      { color: #7ab3d0; margin: 0.2rem 0; }
.terminal-key       { color: #4a7a9b; }
.terminal-val       { color: #00d4ff; }
.terminal-val-crack { color: #ff4444; font-weight: bold; }
.terminal-val-safe  { color: #00ff88; font-weight: bold; }
.terminal-val-bf    { color: #ffaa00; font-weight: bold; }

.strength-bar-wrap {
    background: #111827; border-radius: 4px; height: 12px;
    margin: 0.5rem 0; overflow: hidden; border: 1px solid #1e3a5f;
}
.strength-bar { height: 100%; border-radius: 4px; transition: width 0.6s ease; }

.result-cracked {
    background: rgba(255,50,50,0.1); border: 2px solid #ff3232; border-radius: 6px;
    padding: 1.2rem; text-align: center; font-family: 'Share Tech Mono', monospace;
    font-size: 1.5rem; color: #ff4444; text-shadow: 0 0 15px rgba(255,68,68,0.4);
    letter-spacing: 3px; animation: pulse-red 1.5s infinite;
}
.result-cracked-bf {
    background: rgba(255,170,0,0.1); border: 2px solid #ffaa00; border-radius: 6px;
    padding: 1.2rem; text-align: center; font-family: 'Share Tech Mono', monospace;
    font-size: 1.5rem; color: #ffaa00; text-shadow: 0 0 15px rgba(255,170,0,0.4);
    letter-spacing: 3px; animation: pulse-orange 1.5s infinite;
}
.result-safe {
    background: rgba(0,255,136,0.05); border: 2px solid #00ff88; border-radius: 6px;
    padding: 1.2rem; text-align: center; font-family: 'Share Tech Mono', monospace;
    font-size: 1.5rem; color: #00ff88; text-shadow: 0 0 15px rgba(0,255,136,0.3);
    letter-spacing: 3px;
}
@keyframes pulse-red    { 0%,100%{box-shadow:0 0 10px rgba(255,50,50,0.3);} 50%{box-shadow:0 0 25px rgba(255,50,50,0.6);} }
@keyframes pulse-orange { 0%,100%{box-shadow:0 0 10px rgba(255,170,0,0.3);} 50%{box-shadow:0 0 25px rgba(255,170,0,0.6);} }

.tip-card {
    background: #0d1220; border-left: 3px solid #00d4ff;
    border-radius: 0 6px 6px 0; padding: 0.7rem 1rem;
    margin: 0.4rem 0; font-size: 0.95rem;
}
.scan-line {
    height: 1px; background: linear-gradient(to right, transparent, #00d4ff, transparent);
    margin: 1.5rem 0; opacity: 0.4;
}

.stTextInput input {
    background: #050810 !important; color: #00d4ff !important;
    border: 1px solid #1e3a5f !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1.1rem !important; border-radius: 4px !important;
}
.stTextInput input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 10px rgba(0,212,255,0.2) !important;
}
.stButton button {
    background: linear-gradient(135deg, #0066aa, #0044cc) !important;
    color: white !important; border: 1px solid #00d4ff !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 2px !important; font-size: 0.9rem !important;
    padding: 0.6rem 2rem !important; width: 100% !important;
    border-radius: 4px !important; transition: all 0.2s !important;
}
.stButton button:hover {
    background: linear-gradient(135deg, #0088cc, #0066ee) !important;
    box-shadow: 0 0 15px rgba(0,212,255,0.3) !important;
}

#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CORE FUNCTIONS
# ─────────────────────────────────────────────

@st.cache_data
def load_wordlist():
    combined = set()
    wordlist_files = [
        "malaysia_wordlist.txt",   
        "password-wordlist.txt", 
        "Malaysia.txt",  
        "rockyou.txt",             
    ]
    for filename in wordlist_files:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                words = {line.strip() for line in f if line.strip()}
                combined.update(words)
    return list(combined)


def generate_mutations(word: str) -> list:
    """Generate realistic password mutations from a base word."""
    mutations = [word, word.lower(), word.upper(), word.capitalize()]
    for suffix in ["1","12","123","1234","12345","0","01",
                   "2024","2023","2022","99","00","007"]:
        mutations.append(word + suffix)
        mutations.append(word.capitalize() + suffix)
    leet = word.lower().replace("a","@").replace("e","3") \
                       .replace("i","1").replace("o","0") \
                       .replace("s","$").replace("t","7")
    mutations += [leet, leet.capitalize()]
    for sym in ["!","@","#",".","_"]:
        mutations += [word + sym, word.capitalize() + sym]
    mutations += [word+"!", word+"@123", word+"123!", "123"+word]
    seen, unique = set(), []
    for m in mutations:
        if m not in seen:
            seen.add(m)
            unique.append(m)
    return unique


def classify_strength(password: str):
    """Returns (label, percent, color) for the password strength."""
    has_upper  = any(c.isupper() for c in password)
    has_lower  = any(c.islower() for c in password)
    has_digit  = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    length     = len(password)
    score      = sum([has_upper, has_lower, has_digit, has_symbol])

    if length < 6:                        return "Very Weak",  10, "#e74c3c"
    elif score == 1 and length <= 8:      return "Very Weak",  10, "#e74c3c"
    elif length < 8 or score <= 1:        return "Weak",       28, "#e67e22"
    elif length < 10 or score == 2:       return "Medium",     55, "#f1c40f"
    elif length >= 12 and score >= 3:     return "Strong",     85, "#2ecc71"
    elif score >= 4 and length >= 10:     return "Strong",     80, "#2ecc71"
    else:                                 return "Medium",     55, "#f1c40f"


def dictionary_attack(target_password: str, words: list, max_attempts: int,
                       progress_bar, status_text) -> dict:
    """
    Phase 1: Direct lookup (O1, instant).
    Phase 2: Mutation engine on each wordlist word.
    """
    attempts, cracked, found_word = 0, False, None
    start_time = time.perf_counter()

    # ── Phase 1: Direct lookup ──
    wordlist_set = set(words)
    if target_password in wordlist_set:
        elapsed = time.perf_counter() - start_time
        progress_bar.progress(1.0)
        return {
            "cracked": True, "found_as": target_password,
            "attempts": 1, "time_seconds": round(elapsed, 4),
            "attempts_per_sec": 1, "method": "Dictionary (direct match)",
        }

    # ── Phase 2: Mutation engine ──
    total_est = len(words) * 30
    for word in words:
        for mutated in generate_mutations(word):
            attempts += 1
            if mutated == target_password:
                cracked, found_word = True, mutated
                break
            if attempts >= max_attempts:
                break
            if attempts % 500 == 0:
                pct = min(attempts / total_est, 0.99)
                progress_bar.progress(pct)
                status_text.markdown(
                    f'<div class="terminal-line">[DICT] {attempts:,} attempts — '
                    f'<span style="color:#00d4ff">{mutated[:30]}</span></div>',
                    unsafe_allow_html=True
                )
        if cracked or attempts >= max_attempts:
            break

    elapsed = time.perf_counter() - start_time
    progress_bar.progress(1.0)
    return {
        "cracked"         : cracked,
        "found_as"        : found_word if cracked else "N/A",
        "attempts"        : attempts,
        "time_seconds"    : round(elapsed, 4),
        "attempts_per_sec": round(attempts / elapsed) if elapsed > 0 else 0,
        "method"          : "Dictionary + Mutations",
    }


def brute_force_attack(target_password: str, max_length: int,
                        progress_bar, status_text) -> dict:
    """
    Generates every possible combination of characters up to max_length.
    Will always crack the password if length <= max_length.
    """
    # lowercase only for speed — shows the concept clearly
    charset    = string.ascii_lowercase
    attempts   = 0
    cracked    = False
    found_word = None
    start_time = time.perf_counter()

    # Total combinations for progress estimate
    total_est = sum(len(charset) ** l for l in range(1, max_length + 1))

    for length in range(1, max_length + 1):
        status_text.markdown(
            f'<div class="terminal-line">[BRUTE] Trying length <span style="color:#ffaa00">{length}</span> '
            f'— {len(charset)**length:,} combinations...</div>',
            unsafe_allow_html=True
        )
        for combo in itertools.product(charset, repeat=length):
            attempts += 1
            guess = "".join(combo)

            if guess == target_password:
                cracked, found_word = True, guess
                break

            if attempts % 50000 == 0:
                pct = min(attempts / total_est, 0.99)
                progress_bar.progress(pct)
                status_text.markdown(
                    f'<div class="terminal-line">[BRUTE] {attempts:,} attempts — '
                    f'<span style="color:#ffaa00">{guess}</span></div>',
                    unsafe_allow_html=True
                )

        if cracked:
            break

    elapsed = time.perf_counter() - start_time
    progress_bar.progress(1.0)
    return {
        "cracked"         : cracked,
        "found_as"        : found_word if cracked else "N/A",
        "attempts"        : attempts,
        "time_seconds"    : round(elapsed, 4),
        "attempts_per_sec": round(attempts / elapsed) if elapsed > 0 else 0,
        "method"          : f"Brute Force (up to {max_length} chars, a-z only)",
    }


def make_chart(history):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    fig.patch.set_facecolor("#0a0e1a")

    labels  = [r["password"][:12] for r in history]
    times   = [r["time_seconds"] for r in history]
    attmpts = [r["attempts"] for r in history]
    colors  = []
    for r in history:
        if not r["cracked"]:        colors.append("#00ff88")
        elif "Brute" in r.get("method",""):  colors.append("#ffaa00")
        else:                        colors.append("#ff4444")

    for ax in axes:
        ax.set_facecolor("#050810")
        ax.tick_params(colors="#4a7a9b", labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor("#1e3a5f")

    axes[0].bar(labels, times, color=colors, edgecolor="#1e3a5f", linewidth=0.8)
    axes[0].set_title("Time to Crack (seconds)", color="#00d4ff", fontsize=10, pad=10)
    axes[0].set_ylabel("Seconds", color="#4a7a9b", fontsize=8)
    axes[0].tick_params(axis="x", rotation=20)

    axes[1].bar(labels, attmpts, color=colors, edgecolor="#1e3a5f", linewidth=0.8)
    axes[1].set_title("Number of Attempts", color="#00d4ff", fontsize=10, pad=10)
    axes[1].set_ylabel("Attempts", color="#4a7a9b", fontsize=8)
    axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
    axes[1].tick_params(axis="x", rotation=20)

    legend = [
        mpatches.Patch(color="#ff4444", label="Cracked (Dictionary)"),
        mpatches.Patch(color="#ffaa00", label="Cracked (Brute Force)"),
        mpatches.Patch(color="#00ff88", label="Not Cracked"),
    ]
    fig.legend(handles=legend, loc="upper right", framealpha=0, labelcolor="white", fontsize=8)
    plt.tight_layout(pad=2)
    return fig


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace;color:#00d4ff;letter-spacing:2px;font-size:0.8rem;padding-bottom:0.5rem;border-bottom:1px solid #1e3a5f;">
    ⚙ SETTINGS
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    show_password = st.checkbox("Show password while typing", value=False)

    attack_mode = st.radio(
        "Attack Mode",
        ["Dictionary Only", "Brute Force Only", "Dictionary → then Brute Force"],
        index=2,
        help="Dictionary = wordlist based | Brute Force = tries every combination"
    )

    max_cap = st.slider(
        "Dictionary max attempts", 1000, 500_000, 100_000, step=1000,
        help="Only applies to Dictionary attack"
    )

    bf_length = st.slider(
        "Brute Force max length", 1, 8, 6, step=1,
        help="Max character length to try. WARNING: 7+ chars takes very long!"
    )

    st.markdown("<div class='scan-line'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-family:'Share Tech Mono',monospace;color:#4a7a9b;font-size:0.75rem;line-height:1.8;">
    <b style="color:#00d4ff;">BRUTE FORCE ESTIMATE</b><br>
    a-z only (26 chars)<br>
    26^{bf_length} = {26**bf_length:,} combos<br>
    Up to {bf_length} chars
    </div>
    """, unsafe_allow_html=True)



# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-title">PASSWORD CRACKING SIMULATOR</div>
    <div class="hero-sub">DICTIONARY ATTACK + BRUTE FORCE DEMONSTRATION</div>
    <div class="hero-warning">⚠ EDUCATIONAL USE ONLY - CSC662 COMPUTER SECURITY</div>
</div>
<div class="scan-line"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN LAYOUT
# ─────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace;color:#00d4ff;letter-spacing:2px;font-size:0.85rem;margin-bottom:0.8rem;">
    [ TARGET PASSWORD INPUT ]
    </div>
    """, unsafe_allow_html=True)

    input_type = "default" if show_password else "password"
    password   = st.text_input(
        label="Enter a password to test:",
        type=input_type,
        placeholder="e.g. daniel  |  password123  |  x9#Lm!qZ2@kP",
        label_visibility="collapsed",
        key="password_input"
    )

    # Live strength meter
    if password:
        strength, pct, color = classify_strength(password)
        chars     = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_sym   = any(c in string.punctuation for c in password)

        st.markdown(f"""
        <div style="margin:0.5rem 0 1rem;">
            <div style="display:flex;justify-content:space-between;font-family:'Share Tech Mono',monospace;font-size:0.8rem;margin-bottom:0.3rem;">
                <span style="color:#4a7a9b;">STRENGTH</span>
                <span style="color:{color};font-weight:bold;">{strength.upper()}</span>
            </div>
            <div class="strength-bar-wrap">
                <div class="strength-bar" style="width:{pct}%;background:{color};"></div>
            </div>
            <div style="display:flex;gap:0.5rem;margin-top:0.5rem;flex-wrap:wrap;">
                <span style="font-size:0.75rem;color:{'#00ff88' if chars>=8 else '#ff4444'};font-family:'Share Tech Mono',monospace;">
                    {'✓' if chars>=8 else '✗'} {chars} chars
                </span>
                <span style="font-size:0.75rem;color:{'#00ff88' if has_upper else '#ff4444'};font-family:'Share Tech Mono',monospace;">
                    {'✓' if has_upper else '✗'} UPPER
                </span>
                <span style="font-size:0.75rem;color:{'#00ff88' if has_lower else '#ff4444'};font-family:'Share Tech Mono',monospace;">
                    {'✓' if has_lower else '✗'} lower
                </span>
                <span style="font-size:0.75rem;color:{'#00ff88' if has_digit else '#ff4444'};font-family:'Share Tech Mono',monospace;">
                    {'✓' if has_digit else '✗'} 123
                </span>
                <span style="font-size:0.75rem;color:{'#00ff88' if has_sym else '#ff4444'};font-family:'Share Tech Mono',monospace;">
                    {'✓' if has_sym else '✗'} @#!
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    run_btn = st.button("⚡ LAUNCH ATTACK", key="run")

    # Quick presets
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace;color:#4a7a9b;font-size:0.75rem;letter-spacing:1px;margin-top:1rem;margin-bottom:0.4rem;">
    QUICK TEST PRESETS
    </div>
    """, unsafe_allow_html=True)


    st.markdown("<div class='scan-line'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace;color:#00d4ff;letter-spacing:2px;font-size:0.8rem;margin-bottom:0.6rem;">
    💡 SECURITY TIPS
    </div>
    <div class="tip-card">Use at least <b>12 characters</b> — length is your best defence</div>
    <div class="tip-card">Mix <b>UPPER, lower, numbers & symbols</b></div>
    <div class="tip-card">Try a <b>passphrase</b>: <code>PurpleTiger$RunsFast!</code></div>
    <div class="tip-card">Never use <b>real words or names</b> alone</div>
    <div class="tip-card">Enable <b>Multi-Factor Authentication (MFA)</b></div>
    <div class="tip-card">Use a <b>Password Manager</b> — never reuse passwords</div>
    """, unsafe_allow_html=True)


with col_right:
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace;color:#00d4ff;letter-spacing:2px;font-size:0.85rem;margin-bottom:0.8rem;">
    [ ATTACK CONSOLE ]
    </div>
    """, unsafe_allow_html=True)

    console_placeholder = st.empty()
    result_placeholder  = st.empty()

    if run_btn and password:
        words = load_wordlist()

        # ── Show init box ──
        console_placeholder.markdown(f"""
        <div class="terminal-box">
            <div class="terminal-title">// ATTACK INITIALIZING</div>
            <div class="terminal-line"><span class="terminal-key">TARGET     </span> : <span class="terminal-val">{'*' * len(password)} ({len(password)} chars)</span></div>
            <div class="terminal-line"><span class="terminal-key">MODE       </span> : <span class="terminal-val">{attack_mode}</span></div>
            <div class="terminal-line"><span class="terminal-key">WORDLIST   </span> : <span class="terminal-val">{len(words):,} words loaded</span></div>
            <div class="terminal-line"><span class="terminal-key">DICT CAP   </span> : <span class="terminal-val">{max_cap:,} attempts</span></div>
            <div class="terminal-line"><span class="terminal-key">BF LENGTH  </span> : <span class="terminal-val">up to {bf_length} chars (a-z)</span></div>
        </div>
        """, unsafe_allow_html=True)

        prog_bar   = st.progress(0)
        status_txt = st.empty()
        result     = None
        method_used = ""

        # ── Dictionary Only ──
        if attack_mode == "Dictionary Only":
            result = dictionary_attack(password, words, max_cap, prog_bar, status_txt)
            method_used = result["method"]

        # ── Brute Force Only ──
        elif attack_mode == "Brute Force Only":
            result = brute_force_attack(password, bf_length, prog_bar, status_txt)
            method_used = result["method"]

        # ── Combined: Dictionary → then Brute Force ──
        elif attack_mode == "Dictionary → then Brute Force":
            status_txt.markdown(
                '<div class="terminal-line" style="color:#00d4ff;">[PHASE 1] Running dictionary attack...</div>',
                unsafe_allow_html=True
            )
            result = dictionary_attack(password, words, max_cap, prog_bar, status_txt)
            method_used = result["method"]

            if not result["cracked"]:
                status_txt.markdown(
                    f'<div class="terminal-line" style="color:#ffaa00;">[PHASE 2] Not in wordlist — switching to brute force (up to {bf_length} chars)...</div>',
                    unsafe_allow_html=True
                )
                prog_bar.progress(0)
                bf_result   = brute_force_attack(password, bf_length, prog_bar, status_txt)
                method_used = bf_result["method"]
                if bf_result["cracked"]:
                    result = bf_result

        status_txt.empty()
        prog_bar.empty()

        strength, pct, color = classify_strength(password)
        is_bf = "Brute" in method_used

        # ── Result banner ──
        if result["cracked"] and is_bf:
            result_placeholder.markdown(
                '<div class="result-cracked-bf">⚡ PASSWORD CRACKED — BRUTE FORCE ⚡</div>',
                unsafe_allow_html=True
            )
        elif result["cracked"]:
            result_placeholder.markdown(
                '<div class="result-cracked">⚠ PASSWORD CRACKED — DICTIONARY ⚠</div>',
                unsafe_allow_html=True
            )
        else:
            result_placeholder.markdown(
                '<div class="result-safe">✓ PASSWORD HELD — NOT CRACKED</div>',
                unsafe_allow_html=True
            )

        # ── Terminal result ──
        val_class = "terminal-val-crack" if result["cracked"] and not is_bf else \
                    "terminal-val-bf"    if result["cracked"] and is_bf else \
                    "terminal-val-safe"
        status_str = "CRACKED ⚠" if result["cracked"] else "NOT CRACKED ✓"

        console_placeholder.markdown(f"""
        <div class="terminal-box">
            <div class="terminal-title">// ATTACK COMPLETE — RESULTS</div>
            <div class="terminal-line"><span class="terminal-key">STATUS     </span> : <span class="{val_class}">{status_str}</span></div>
            <div class="terminal-line"><span class="terminal-key">METHOD     </span> : <span class="terminal-val">{method_used}</span></div>
            <div class="terminal-line"><span class="terminal-key">PASSWORD   </span> : <span class="terminal-val">{'*' * len(password)}</span></div>
            {'<div class="terminal-line"><span class="terminal-key">FOUND AS   </span> : <span class="' + val_class + '">' + result["found_as"] + '</span></div>' if result["cracked"] else ''}
            <div class="terminal-line"><span class="terminal-key">STRENGTH   </span> : <span style="color:{color};">{strength.upper()}</span></div>
            <div class="terminal-line"><span class="terminal-key">ATTEMPTS   </span> : <span class="terminal-val">{result['attempts']:,}</span></div>
            <div class="terminal-line"><span class="terminal-key">TIME TAKEN </span> : <span class="terminal-val">{result['time_seconds']} seconds</span></div>
            <div class="terminal-line"><span class="terminal-key">SPEED      </span> : <span class="terminal-val">{result['attempts_per_sec']:,} attempts/sec</span></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Save to history ──
        st.session_state.history.append({
            "password"    : password,
            "strength"    : strength,
            "cracked"     : result["cracked"],
            "method"      : method_used,
            "attempts"    : result["attempts"],
            "time_seconds": result["time_seconds"],
        })

    elif run_btn and not password:
        console_placeholder.markdown("""
        <div class="terminal-box">
            <div class="terminal-title">// ERROR</div>
            <div class="terminal-line" style="color:#ff4444;">No password entered. Please type a password to test.</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        console_placeholder.markdown("""
        <div class="terminal-box">
            <div class="terminal-title">// AWAITING TARGET</div>
            <div class="terminal-line">Enter a password on the left and click</div>
            <div class="terminal-line"><span style="color:#00d4ff;">⚡ LAUNCH ATTACK</span> to begin.</div>
            <br>
            <div class="terminal-line" style="color:#4a7a9b;">Suggested demo sequence:</div>
            <div class="terminal-line">  → <span style="color:#ff4444;">abc</span>           Brute forced instantly</div>
            <div class="terminal-line">  → <span style="color:#ff4444;">daniel</span>        Brute forced in seconds</div>
            <div class="terminal-line">  → <span style="color:#ff4444;">123456</span>        In wordlist — instant</div>
            <div class="terminal-line">  → <span style="color:#f1c40f;">danielsahid</span>   Too long for brute force</div>
            <div class="terminal-line">  → <span style="color:#2ecc71;">x9#Lm!qZ2@kP</span> Uncrackable</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SESSION HISTORY & CHARTS
# ─────────────────────────────────────────────
if st.session_state.history:
    st.markdown("<div class='scan-line'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace;color:#00d4ff;letter-spacing:2px;font-size:0.9rem;margin-bottom:1rem;">
    [ SESSION HISTORY & ANALYSIS ]
    </div>
    """, unsafe_allow_html=True)

    h_col1, h_col2 = st.columns([1, 1], gap="large")

    with h_col1:
        df = pd.DataFrame(st.session_state.history)
        df["result"] = df["cracked"].map({True: "⚠ CRACKED", False: "✓ SAFE"})
        df["time_seconds"] = df["time_seconds"].apply(lambda x: f"{x:.4f}s")
        st.dataframe(
            df[["password","strength","result","method","attempts","time_seconds"]].rename(columns={
                "password":"Password","strength":"Strength","result":"Result",
                "method":"Method","attempts":"Attempts","time_seconds":"Time"
            }),
            use_container_width=True,
            hide_index=True,
        )

        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Export Results CSV",
            data=csv_data,
            file_name="cracking_results.csv",
            mime="text/csv",
        )

        if st.button("🗑 Clear History"):
            st.session_state.history = []
            st.rerun()

    with h_col2:
        fig = make_chart(st.session_state.history)
        st.pyplot(fig, use_container_width=True)
        plt.close()