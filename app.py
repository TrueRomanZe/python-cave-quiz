"""
🐍 THE PYTHON CAVE - Interactive Quiz
100% Python implementation using Streamlit
"""

import streamlit as st
import base64

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="🐍 The Python Cave",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# GOOGLE ANALYTICS
# ============================================================================

# Reemplaza 'G-XXXXXXXXXX' con tu ID de Google Analytics
GOOGLE_ANALYTICS_ID = "G-RSGTNL6FWR"

st.markdown(f"""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GOOGLE_ANALYTICS_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GOOGLE_ANALYTICS_ID}', {{
    'anonymize_ip': true,
    'allow_google_signals': false,
    'allow_ad_personalization_signals': false
  }});
</script>
""", unsafe_allow_html=True)

# ============================================================================
# CSS PERSONALIZADO
# ============================================================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    .stMarkdown, .stText, p, li {
        color: #00ff00 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    h1, h2, h3 {
        color: #00ff00 !important;
        text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00;
        font-family: 'Courier New', monospace !important;
        text-align: center;
    }
    
    .stButton > button {
        background-color: rgba(0, 150, 0, 0.3) !important;
        border: 2px solid #00aa00 !important;
        color: #00ff00 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 1.1rem !important;
        padding: 15px 30px !important;
        border-radius: 8px !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        background-color: rgba(0, 255, 0, 0.2) !important;
        border-color: #00ff00 !important;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.5) !important;
        transform: scale(1.05) !important;
    }
    
    .stRadio > label {
        color: #ffaa00 !important;
        font-weight: bold !important;
    }
    
    .stRadio > div {
        background-color: rgba(0, 100, 0, 0.2) !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border: 2px solid #00aa00 !important;
    }
    
    code {
        background-color: #0a0a0a !important;
        color: #00ff00 !important;
        padding: 2px 6px !important;
        border-radius: 3px !important;
    }
    
    pre {
        background-color: #0a0a0a !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        padding: 15px !important;
    }
    
    .success-box {
        background-color: rgba(0, 255, 0, 0.2) !important;
        border: 3px solid #00ff00 !important;
        padding: 20px !important;
        border-radius: 10px !important;
        margin: 20px 0 !important;
    }
    
    .error-box {
        background-color: rgba(255, 0, 0, 0.2) !important;
        border: 3px solid #ff0000 !important;
        padding: 20px !important;
        border-radius: 10px !important;
        margin: 20px 0 !important;
    }
    
    audio {
        display: none !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES DE AUDIO
# ============================================================================

def play_audio(file_path, autoplay=True, loop=False):
    """Reproduce audio usando HTML5"""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        
        auto = "autoplay" if autoplay else ""
        lp = "loop" if loop else ""
        
        html = f'<audio {auto} {lp}><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(html, unsafe_allow_html=True)
    except:
        pass

def stop_all_audio():
    """Detiene todos los audios activos"""
    st.markdown("""
    <script>
        // Ejecutar inmediatamente
        var audios = document.querySelectorAll('audio');
        audios.forEach(function(audio) {
            audio.pause();
            audio.currentTime = 0;
            audio.src = '';
        });
        
        // Ejecutar de nuevo después de 100ms por si acaso
        setTimeout(function() {
            var audios = document.querySelectorAll('audio');
            audios.forEach(function(audio) {
                audio.pause();
                audio.currentTime = 0;
                audio.src = '';
            });
        }, 100);
    </script>
    """, unsafe_allow_html=True)

# ============================================================================
# ESTADO
# ============================================================================

if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.current_question = 0
    st.session_state.answered = False
    st.session_state.victory = False
    st.session_state.game_over = False
    st.session_state.muted = False

# ============================================================================
# PREGUNTAS - b, a, b, d, c
# ============================================================================

QUESTIONS = [
    {
        'number': 1,
        'title': 'Question 1 — The Entrance',
        'story': 'The serpent blocks the cave and asks:',
        'question': 'Where does the name "Python" come from?',
        'options': ['a) a snake', 'b) Monty Python', "c) Guido van Rossum's pet"],
        'correct': 1,
        'correct_text': 'The serpent laughs. **"Correct! Finally, a human with a sense of humor."** It moves aside and lets you enter the cave.',
        'wrong_text': 'The serpent sighs. **"No… but I appreciate the ego boost."** Then it casually swallows you whole and posts a sign outside the cave: *"Warning: Adventurer failed basic trivia."*\n\n💀 **Game Over.**'
    },
    {
        'number': 2,
        'title': 'Question 2 — The Talking Stone',
        'story': 'Inside the cave you find a glowing stone with strange symbols.',
        'question': 'Which symbol starts a comment in Python?',
        'options': ['a) #', 'b) //', 'c) /*'],
        'correct': 0,
        'correct_text': 'The stone glows brighter. **"Good. Future programmers will thank you for your comments."**',
        'wrong_text': 'The stone dims. **"Those belong to other languages… traitor."** Suddenly the serpent appears behind you and says: *"Uncommented code is a crime."* It drops a giant syntax error on your head.\n\n💀 **You were crushed by `SyntaxError: invalid answer`.**'
    },
    {
        'number': 3,
        'title': 'Question 3 — The Crack in the Wall',
        'story': 'From a crack in the wall, a tiny dragon pokes its head out.\n\nIt asks:',
        'question': 'Which keyword defines a function in Python?',
        'options': ['a) function', 'b) def', 'c) create'],
        'correct': 1,
        'correct_text': 'The dragon nods proudly. **"Excellent. You have defined your power."**',
        'wrong_text': 'The dragon shrugs. Then accidentally breathes fire on your notes and says: **"Oh… sorry… I think you forgot to define your survival."**\n\n💀 **You were burned by `NameError: life is not defined`.**'
    },
    {
        'number': 4,
        'title': 'Question 4 — The Suspicious Chest',
        'story': 'You discover a treasure chest labeled "Data Structures".\n\nIt asks before opening:',
        'question': 'Which structure is ordered and mutable?',
        'options': ['a) tuple', 'b) set', 'c) dict', 'd) list'],
        'correct': 3,
        'correct_text': 'The chest opens. **"Correct! Lists change easily. Unlike my password."**',
        'wrong_text': 'The chest stays shut… then suddenly sprouts teeth.\n**"Wrong container,"** it says.\n\n💀 **You were eaten by a `MutableChestError`.**'
    },
    {
        'number': 5,
        'title': 'Question 5 — The Chamber of Infinite Loops',
        'story': 'You reach the deepest part of the cave. The giant serpent descends from above, its eyes blazing with electric blue light.\n\nThe serpent speaks:\n\n**"This is my TRUE test. Answer wisely."**',
        'question': 'What is the output of this code?',
        'code': '''x = 0
while x < 5:
    x += 1
    if x == 3:
        continue
    print(x)''',
        'options': ['a) 1 2 3 4 5', 'b) 0 1 2 4 5', 'c) 1 2 4 5', 'd) The code runs forever'],
        'correct': 2,
        'correct_text': "The serpent's eyes widen. The chamber explodes with golden light.\n\n**\"YESSSSS… You understand `continue`! You are no mere adventurer—you are a PYTHONISTA.\"**\n\nThe serpent transforms into a majestic dragon and opens a portal of light.",
        'wrong_text': "The serpent's expression darkens. It ROARS.\n\n**\"YOU DO NOT UNDERSTAND `continue`! Your punishment… INFINITE LOOP.\"**\n\nThe world resets. You're back at the cave entrance. The serpent blocks the way again.\n\nYou realize with horror: **You're stuck in a `while True` loop with no `break`.**\n\n💀 **You were consumed by `RuntimeError: maximum recursion depth exceeded`.**"
    }
]

# ============================================================================
# PANTALLAS
# ============================================================================

def show_intro():
    # Background suena desde el inicio
    if not st.session_state.muted and not st.session_state.game_over:
        play_audio("assets/background_music.mp3", autoplay=True, loop=True)
    
    st.markdown("# 🐍 The Python Cave")
    st.markdown("### *An Interactive Coding Adventure*")
    st.markdown("---")
    st.markdown("""
    **Welcome, adventurer.** A massive serpent guards the entrance of a dark cave.
    
    It whispers: *"Answer my riddles and you may enter my cave. Fail… and I'll assume you code in Java without indentation."*
    """)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚪 Enter the Cave", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()

def show_question():
    q = QUESTIONS[st.session_state.current_question]
    
    # Background suena continuamente - EXCEPTO si ya respondiste mal
    if st.session_state.answered and st.session_state.get('user_answer') != q['correct']:
        # Ya respondiste mal - NO reproducir background
        pass
    elif not st.session_state.game_over and not st.session_state.muted:
        # Reproducir background normalmente
        play_audio("assets/background_music.mp3", autoplay=True, loop=True)
    
    st.markdown(f"### Question {q['number']} of 5")
    st.progress((q['number'] - 1) / 5)
    st.markdown("---")
    st.markdown(f"#### {q['title']}")
    st.markdown(q['story'])
    st.markdown("")
    st.markdown(f"**{q['question']}**")
    
    if 'code' in q:
        st.code(q['code'], language='python')
    
    st.markdown("")
    
    if not st.session_state.answered:
        answer = st.radio(
            "Choose your answer:",
            options=range(len(q['options'])),
            format_func=lambda x: q['options'][x],
            key=f"q_{st.session_state.current_question}"
        )
        
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit Answer", use_container_width=True):
                st.session_state.answered = True
                st.session_state.user_answer = answer
                st.rerun()
    
    if st.session_state.answered:
        user_answer = st.session_state.user_answer
        
        if user_answer == q['correct']:
            # RESPUESTA CORRECTA
            if not st.session_state.muted:
                play_audio("assets/success.mp3", autoplay=True, loop=False)
            
            st.markdown(f"""
            <div class="success-box">
                <p style="font-size: 1.2rem; line-height: 1.8;">{q['correct_text']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                btn_text = "Reveal Your Destiny ✨" if st.session_state.current_question >= len(QUESTIONS) - 1 else "Continue ➡️"
                
                if st.button(btn_text, use_container_width=True):
                    st.session_state.answered = False
                    st.session_state.current_question += 1
                    
                    if st.session_state.current_question >= len(QUESTIONS):
                        st.session_state.victory = True
                        st.session_state.game_over = True
                    
                    st.rerun()
        else:
            # GAME OVER
            st.session_state.game_over = True
            stop_all_audio()
            
            # Reproducir gameover con pequeño delay para asegurar que background se detuvo
            if not st.session_state.muted:
                st.markdown("""
                <script>
                    setTimeout(function() {
                        // Primero detener TODOS los audios de nuevo
                        document.querySelectorAll('audio').forEach(function(audio) {
                            audio.pause();
                            audio.currentTime = 0;
                        });
                    }, 50);
                </script>
                """, unsafe_allow_html=True)
                play_audio("assets/gameover.mp3", autoplay=True, loop=False)
            
            st.markdown(f"""
            <div class="error-box">
                <p style="font-size: 1.2rem; line-height: 1.8; color: #ff6666 !important;">{q['wrong_text']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Try Again", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()

def show_victory():
    # Detener background
    stop_all_audio()
    
    # Reproducir victoria con delay para asegurar que background se detuvo
    if not st.session_state.muted:
        st.markdown("""
        <script>
            setTimeout(function() {
                // Primero detener TODOS los audios de nuevo
                document.querySelectorAll('audio').forEach(function(audio) {
                    audio.pause();
                    audio.currentTime = 0;
                });
            }, 50);
        </script>
        """, unsafe_allow_html=True)
        play_audio("assets/final_victory.mp3", autoplay=True, loop=True)
    
    st.markdown("# 🏆 VICTORY")
    st.markdown("---")
    st.markdown("""
    <div class="success-box">
        <p style="font-size: 1.3rem; line-height: 2;">
            <strong>"Remember, brave coder: Life is like a loop—it keeps going until you <code>break</code>. 
            Sometimes you must <code>continue</code> past obstacles. And always, ALWAYS comment your code… 
            because the person reading it in six months will be you."</strong>
        </p>
        <p style="margin-top: 20px; font-size: 1.2rem;">
            The dragon winks. <strong>"Also, everyone uses Stack Overflow. Even me."</strong>
        </p>
        <p style="margin-top: 30px; font-size: 1.5rem; color: #ffff00 !important; text-align: center;">
            🎉 You exit the cave as a PYTHON MASTER. 🐍
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Play Again", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# ============================================================================
# MAIN
# ============================================================================

def main():
    # Botón mute/unmute
    col1, col2, col3 = st.columns([5, 1, 1])
    with col3:
        mute_icon = "🔇" if st.session_state.muted else "🔊"
        if st.button(mute_icon, key="mute_btn"):
            st.session_state.muted = not st.session_state.muted
            if st.session_state.muted:
                stop_all_audio()
            st.rerun()
    
    # Mostrar pantalla
    if not st.session_state.game_started:
        show_intro()
    elif st.session_state.victory:
        show_victory()
    else:
        show_question()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <p style="text-align: center; font-size: 0.9rem; color: #ffaa00 !important;">
        Made with 🐍 Python & Streamlit | 
        <a href="https://github.com/TrueRomanZe/python-cave-quiz" style="color: #00ff00;">View Source Code</a>
    </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
