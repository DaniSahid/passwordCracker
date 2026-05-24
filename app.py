import streamlit as st
import time
import string
import itertools
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

st.set_page_config(
    page_title="Password Cracking Simulator",
    page_icon="🔐",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0a0e1a; color: #c8d8e8; }
.stApp { background-color: #0a0e1a; }

.header {
    background: linear-gradient(135deg, #0d1220, #0a0e1a);
    border: 1px solid #1e3a5f; border-radius: 12px;
    padding: 2rem; text-align: center; margin-bottom: 1.5rem;
}
.header h1 { font-family: 'Share Tech Mono', monospace; color: #00d4ff; font-size: 1.9rem; margin: 0; letter-spacing: 2px; }
.header p  { color: #4a7a9b; margin: 0.4rem 0 0; font-size: 0.85rem; }
.header .warn {
    display: inline-block; margin-top: 0.6rem;
    background: rgba(255,100,0,0.1); border: 1px solid #ff6400;
    color: #ff6400; padding: 0.2rem 0.8rem; border-radius: 4px;
    font-size: 0.75rem; font-family: 'Share Tech Mono', monospace;
}
.card {
    background: #0d1220; border: 1px solid #1e3a5f;
    border-radius: 10px; padding: 1.2rem 1.5rem; margin: 0.8rem 0;
}
.card-title {
    font-family: 'Share Tech Mono', monospace; color: #00d4ff;
    font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 0.8rem;
    border-bottom: 1px solid #1e3a5f; padding-bottom: 0.4rem;
}
.result-cracked {
    background: rgba(231,76,60,0.1); border: 2px solid #e74c3c;
    border-radius: 10px; padding: 1rem; text-align: center;
    color: #e74c3c; font-family: 'Share Tech Mono', monospace;
    font-size: 1.2rem; letter-spacing: 2px; margin: 1rem 0;
}
.result-tooslow {
    background: rgba(255,170,0,0.1); border: 2px solid #ffaa00;
    border-radius: 10px; padding: 1rem; text-align: center;
    color: #ffaa00; font-family: 'Share Tech Mono', monospace;
    font-size: 1.1rem; letter-spacing: 2px; margin: 1rem 0;
}
.result-safe {
    background: rgba(46,204,113,0.1); border: 2px solid #2ecc71;
    border-radius: 10px; padding: 1rem; text-align: center;
    color: #2ecc71; font-family: 'Share Tech Mono', monospace;
    font-size: 1.2rem; letter-spacing: 2px; margin: 1rem 0;
}
.info-row {
    background: #050810; border-left: 3px solid #00d4ff;
    border-radius: 0 6px 6px 0; padding: 0.5rem 1rem;
    margin: 0.35rem 0; font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem; color: #7ab3d0;
}
.info-row b   { color: #4a7a9b; }
.info-val     { color: #00d4ff; }
.info-crack   { color: #e74c3c; font-weight: bold; }
.info-warn    { color: #ffaa00; font-weight: bold; }
.info-safe    { color: #2ecc71; font-weight: bold; }
.gpu-box {
    background: rgba(255,170,0,0.07); border: 1px solid #ffaa00;
    border-radius: 8px; padding: 0.8rem 1rem; margin: 0.5rem 0;
    font-family: 'Share Tech Mono', monospace; font-size: 0.82rem; color: #ffaa00;
}
.strength-wrap { background: #111827; border-radius: 6px; height: 10px; margin: 0.4rem 0 0.8rem; overflow: hidden; }
.strength-fill { height: 100%; border-radius: 6px; }
.tip { background: #0d1220; border-left: 3px solid #f39c12; border-radius: 0 6px 6px 0; padding: 0.5rem 1rem; margin: 0.3rem 0; font-size: 0.88rem; color: #c8d8e8; }
.divider { height: 1px; background: linear-gradient(to right, transparent, #1e3a5f, transparent); margin: 1.2rem 0; }

.stTextInput input {
    background: #050810 !important; color: #00d4ff !important;
    border: 1px solid #1e3a5f !important; border-radius: 6px !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stTextInput input:focus { border-color: #00d4ff !important; box-shadow: 0 0 8px rgba(0,212,255,0.2) !important; }
label { color: #4a7a9b !important; font-size: 0.85rem !important; }
.stButton > button {
    background: linear-gradient(135deg, #0066aa, #0044cc) !important;
    color: white !important; border: 1px solid #00d4ff !important;
    border-radius: 6px !important; font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 1px !important; width: 100% !important;
}
.stButton > button:hover { background: linear-gradient(135deg, #0088cc, #0055ee) !important; box-shadow: 0 0 12px rgba(0,212,255,0.3) !important; }
[data-testid="stSidebar"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FUNCTIONS
# ─────────────────────────────────────────────

@st.cache_data
def load_wordlist():
    combined = set()
    loaded = []
    for filename in ["malaysia_wordlist.txt", "password-wordlist.txt", "Malaysia.txt", "rockyou.txt", "common-students.txt"]:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                words = {line.strip() for line in f if line.strip()}
                combined.update(words)
                loaded.append(f"{filename} ({len(words):,})")
    return list(combined), set(combined), loaded


def generate_mutations(word: str) -> list:
    mutations = [word, word.lower(), word.upper(), word.capitalize()]
    for suffix in ["1","12","123","1234","12345","0","01","2024","2023","2022","99","00","007"]:
        mutations.append(word + suffix)
        mutations.append(word.capitalize() + suffix)
    leet = word.lower().replace("a","@").replace("e","3").replace("i","1").replace("o","0").replace("s","$").replace("t","7")
    mutations += [leet, leet.capitalize()]
    for sym in ["!","@","#","."]:
        mutations += [word + sym, word.capitalize() + sym]
    mutations += [word+"!", word+"@123", word+"123!", "123"+word]
    seen, unique = set(), []
    for m in mutations:
        if m not in seen:
            seen.add(m)
            unique.append(m)
    return unique


def classify_strength(password: str):
    has_upper  = any(c.isupper() for c in password)
    has_lower  = any(c.islower() for c in password)
    has_digit  = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    length     = len(password)
    score      = sum([has_upper, has_lower, has_digit, has_symbol])
    if length < 6:                    return "Very Weak",  "#e74c3c", 10
    elif score == 1 and length <= 8:  return "Very Weak",  "#e74c3c", 10
    elif length < 8 or score <= 1:    return "Weak",       "#e67e22", 28
    elif length < 10 or score == 2:   return "Medium",     "#f39c12", 55
    elif length >= 12 and score >= 3: return "Strong",     "#2ecc71", 85
    elif score >= 4 and length >= 10: return "Strong",     "#2ecc71", 80
    else:                             return "Medium",     "#f39c12", 55


def estimate_crack_time(password: str) -> dict:
    """Returns estimated crack time at different hardware speeds."""
    charset = 0
    if any(c.islower() for c in password): charset += 26
    if any(c.isupper() for c in password): charset += 26
    if any(c.isdigit() for c in password): charset += 10
    if any(c in string.punctuation for c in password): charset += 32
    combos = charset ** len(password)

    def fmt(secs):
        if secs < 1:           return "< 1 second"
        elif secs < 60:        return f"{secs:.1f} seconds"
        elif secs < 3600:      return f"{secs/60:.1f} minutes"
        elif secs < 86400:     return f"{secs/3600:.1f} hours"
        elif secs < 31536000:  return f"{secs/86400:.0f} days"
        else:                  return f"{secs/31536000:.1f} years"

    return {
        "combinations"    : combos,
        "Python (laptop)" : fmt(combos / 1_000_000),
        "RTX 4090 (GPU)"  : fmt(combos / 164_000_000_000),
        "8x GPU Cluster"  : fmt(combos / 1_000_000_000_000),
    }


# BF_DEMO_LIMIT: max attempts before we give up and show estimate instead
BF_DEMO_LIMIT = 3_000_000   # ~3 seconds in Python — good for live demo

def run_attack(target, words, wset, mode, max_dict, bf_length):
    """
    Returns result dict. If brute force would take too long,
    sets 'too_slow': True and includes time estimates instead.
    """
    attempts = 0
    start    = time.perf_counter()

    # ── Phase 1: Dictionary ──
    if mode in ["Dictionary Attack", "Dictionary → then Brute Force"]:
        if target in wset:
            elapsed = time.perf_counter() - start
            return {"cracked": True, "found_as": target, "attempts": 1,
                    "time_seconds": round(elapsed, 4), "method": "Dictionary (direct match)",
                    "too_slow": False}

        for word in words:
            for mutated in generate_mutations(word):
                attempts += 1
                if mutated == target:
                    elapsed = time.perf_counter() - start
                    return {"cracked": True, "found_as": mutated, "attempts": attempts,
                            "time_seconds": round(elapsed, 4), "method": "Dictionary + Mutations",
                            "too_slow": False}
                if attempts >= max_dict:
                    break
            if attempts >= max_dict:
                break

    # ── Phase 2: Brute Force ──
    if mode in ["Brute Force Attack", "Dictionary → then Brute Force"]:

        # Check first: is the password all-lowercase only?
        # If it has uppercase/digits/symbols, pure a-z BF won't find it
        is_lowercase_only = all(c.islower() for c in target)

        # Estimate how many combos needed for this password length
        total_combos = sum(26 ** l for l in range(1, len(target) + 1))

        # If it would take too long, skip and show estimate instead
        if total_combos > BF_DEMO_LIMIT or not is_lowercase_only:
            elapsed = time.perf_counter() - start
            estimates = estimate_crack_time(target)
            return {
                "cracked"     : False,
                "found_as"    : "N/A",
                "attempts"    : attempts,
                "time_seconds": round(elapsed, 4),
                "method"      : "Brute Force (exceeded demo limit)",
                "too_slow"    : True,
                "estimates"   : estimates,
            }

        # Actually brute force it (only runs if fast enough)
        charset  = string.ascii_lowercase
        bf_att   = 0
        bf_start = time.perf_counter()
        for length in range(1, len(target) + 1):
            for combo in itertools.product(charset, repeat=length):
                bf_att += 1
                guess = "".join(combo)
                if guess == target:
                    elapsed = time.perf_counter() - bf_start
                    return {"cracked": True, "found_as": guess,
                            "attempts": attempts + bf_att,
                            "time_seconds": round(elapsed, 4),
                            "method": f"Brute Force (a-z, {len(target)} chars)",
                            "too_slow": False}

    elapsed = time.perf_counter() - start
    return {"cracked": False, "found_as": "N/A", "attempts": attempts,
            "time_seconds": round(elapsed, 4), "method": mode,
            "too_slow": False}


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="header">
    <h1>🔐 PASSWORD CRACKING SIMULATOR</h1>
    <p>CSC662 Computer Security - Assignment</p>
    <span class="warn">⚠ EDUCATIONAL USE ONLY</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD WORDLIST
# ─────────────────────────────────────────────
words, wset, loaded_files = load_wordlist()
st.markdown(f"""
<div class="info-row">
    <b>WORDLIST</b> &nbsp;→&nbsp;
    <span class="info-val">{len(words):,} words loaded</span>
    &nbsp;|&nbsp; {" + ".join(loaded_files) if loaded_files else "No wordlist files found in folder"}
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INPUT
# ─────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">// TARGET PASSWORD</div>', unsafe_allow_html=True)

show_pw  = st.checkbox("Show password while typing", value=False)
password = st.text_input(
    "Password:", type="default" if show_pw else "password",
    placeholder="Type any password to test...",
    label_visibility="collapsed",
)

if password:
    label, color, pct = classify_strength(password)
    has_u = any(c.isupper() for c in password)
    has_l = any(c.islower() for c in password)
    has_d = any(c.isdigit() for c in password)
    has_s = any(c in string.punctuation for c in password)
    n     = len(password)
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;font-family:'Share Tech Mono',monospace;font-size:0.8rem;margin-top:0.5rem;">
        <span style="color:#4a7a9b;">STRENGTH</span>
        <span style="color:{color};font-weight:bold;">{label.upper()}</span>
    </div>
    <div class="strength-wrap">
        <div class="strength-fill" style="width:{pct}%;background:{color};"></div>
    </div>
    <div style="display:flex;gap:1rem;font-family:'Share Tech Mono',monospace;font-size:0.78rem;flex-wrap:wrap;">
        <span style="color:{'#2ecc71' if n>=8 else '#e74c3c'}">{'✓' if n>=8 else '✗'} {n} chars</span>
        <span style="color:{'#2ecc71' if has_u else '#e74c3c'}">{'✓' if has_u else '✗'} UPPER</span>
        <span style="color:{'#2ecc71' if has_l else '#e74c3c'}">{'✓' if has_l else '✗'} lower</span>
        <span style="color:{'#2ecc71' if has_d else '#e74c3c'}">{'✓' if has_d else '✗'} 123</span>
        <span style="color:{'#2ecc71' if has_s else '#e74c3c'}">{'✓' if has_s else '✗'} @#!</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SETTINGS
# ─────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">// ATTACK SETTINGS</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    attack_mode = st.selectbox("Attack Mode", [
        "Dictionary → then Brute Force",
        "Dictionary Attack",
        "Brute Force Attack",
    ])
with col2:
    max_cap = st.slider("Dictionary Max Attempts", 10_000, 500_000, 100_000, step=10_000)
st.markdown("""
<div style="font-family:'Share Tech Mono',monospace;color:#4a7a9b;font-size:0.78rem;margin-top:0.5rem;">
ℹ️  Brute Force automatically handles passwords up to ~6 lowercase chars in demo time.
Longer passwords will show estimated crack time on real hardware instead.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LAUNCH
# ─────────────────────────────────────────────
if st.button("⚡  LAUNCH ATTACK", use_container_width=True):
    if not password:
        st.warning("Please enter a password first.")
    else:
        with st.spinner("Attacking..."):
            result = run_attack(password, words, wset, attack_mode, max_cap, bf_length=7)

        label, color, pct = classify_strength(password)

        # ── Result banner ──
        if result["cracked"]:
            st.markdown('<div class="result-cracked">⚠️  PASSWORD CRACKED</div>', unsafe_allow_html=True)
        elif result.get("too_slow"):
            st.markdown('<div class="result-tooslow">⏱️  TOO SLOW FOR DEMO — SEE GPU ESTIMATE BELOW</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-safe">✅  PASSWORD NOT CRACKED</div>', unsafe_allow_html=True)

        # ── Details ──
        vc = "info-crack" if result["cracked"] else "info-warn" if result.get("too_slow") else "info-safe"
        status_str = "CRACKED ⚠️" if result["cracked"] else "DEMO LIMIT REACHED ⏱️" if result.get("too_slow") else "NOT CRACKED ✅"

        st.markdown(f"""
        <div class="info-row"><b>STATUS  &nbsp;&nbsp;&nbsp;</b> <span class="{vc}">{status_str}</span></div>
        <div class="info-row"><b>METHOD  &nbsp;&nbsp;&nbsp;</b> <span class="info-val">{result["method"]}</span></div>
        {"<div class='info-row'><b>FOUND AS &nbsp;</b> <span class='info-crack'>" + result["found_as"] + "</span></div>" if result["cracked"] else ""}
        <div class="info-row"><b>STRENGTH &nbsp;</b> <span style="color:{color};font-weight:bold;">{label.upper()}</span></div>
        <div class="info-row"><b>ATTEMPTS &nbsp;</b> <span class="info-val">{result["attempts"]:,}</span></div>
        <div class="info-row"><b>TIME &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b> <span class="info-val">{result["time_seconds"]} seconds</span></div>
        """, unsafe_allow_html=True)

        # ── GPU Estimate box — shows for ALL results ──
        estimates = result.get("estimates") or estimate_crack_time(password)
        st.markdown(f"""
        <div class="gpu-box">
            ⚡ ESTIMATED BRUTE FORCE CRACK TIME ({estimates["combinations"]:,} combinations)<br><br>
            🖥️  Python &nbsp;&nbsp;→ <b>{estimates["Python (laptop)"]}</b><br>
            🎮  RTX 4090 Gaming GPU &nbsp;&nbsp;&nbsp;→ <b>{estimates["RTX 4090 (GPU)"]}</b><br>
            🖥️  8× GPU Cluster &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ <b>{estimates["8x GPU Cluster"]}</b>
        </div>
        """, unsafe_allow_html=True)

        # Save to history
        hist_entry = {
            "Password" : password,
            "Strength" : label,
            "Cracked"  : "Yes ⚠️" if result["cracked"] else "No ✅",
            "Method"   : result["method"],
            "Attempts" : result["attempts"],
            "Time (s)" : result["time_seconds"],
            "GPU (RTX 4090)" : estimates["RTX 4090 (GPU)"],
        }
        st.session_state.history.append(hist_entry)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SECURITY TIPS
# ─────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">// SECURITY TIPS</div>', unsafe_allow_html=True)
for tip in [
    "Use at least 12 characters — length is your best defence",
    "Mix UPPERCASE, lowercase, numbers and symbols",
    "Use a passphrase: PurpleTiger$RunsFast! is strong and memorable",
    "Never use your name, IC number, or 'uitm123' as a password",
    "Enable Multi-Factor Authentication (MFA) on all accounts",
    "Use a Password Manager — never reuse passwords across sites",
    "Even a strong password can be stolen in a server breach — MFA is essential",
]:
    st.markdown(f'<div class="tip">💡 {tip}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HISTORY & CHARTS
# ─────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="card-title" style="font-family:\'Share Tech Mono\',monospace;color:#00d4ff;letter-spacing:2px;font-size:0.8rem;">// SESSION HISTORY & ANALYSIS</div>', unsafe_allow_html=True)

    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True, hide_index=True)

    fig, axes = plt.subplots(1, 2, figsize=(10, 3))
    fig.patch.set_facecolor("#0a0e1a")
    colors = ["#e74c3c" if r["Cracked"] == "Yes ⚠️" else "#2ecc71" for r in st.session_state.history]
    labels = [r["Password"][:10] for r in st.session_state.history]

    for ax in axes:
        ax.set_facecolor("#0d1220")
        ax.tick_params(colors="#4a7a9b", labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor("#1e3a5f")

    axes[0].bar(labels, [r["Time (s)"] for r in st.session_state.history], color=colors, edgecolor="#1e3a5f")
    axes[0].set_title("Time to Crack (seconds)", color="#00d4ff", fontsize=9, pad=8)
    axes[0].tick_params(axis="x", rotation=20)

    axes[1].bar(labels, [r["Attempts"] for r in st.session_state.history], color=colors, edgecolor="#1e3a5f")
    axes[1].set_title("Number of Attempts", color="#00d4ff", fontsize=9, pad=8)
    axes[1].tick_params(axis="x", rotation=20)
    axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))

    legend = [mpatches.Patch(color="#e74c3c", label="Cracked"),
              mpatches.Patch(color="#2ecc71", label="Not Cracked")]
    fig.legend(handles=legend, loc="upper right", framealpha=0, labelcolor="white", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    c1, c2 = st.columns(2)
    with c1:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Export CSV", csv, "results.csv", "text/csv", use_container_width=True)
    with c2:
        if st.button("🗑 Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
