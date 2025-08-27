from flask import Flask, render_template, redirect, url_for, request
import google.generativeai as genai
import os

app = Flask(__name__)

# --- Configuration de l'IA ---
genai.configure(api_key="AIzaSyA8L4VKSW5rYsH48MRCbmilGHnv8bZ3uVA")

# Définition de l'IA Elion
instructions_ia = """
Bonjour (nom de l'utilisateur), je me nomme Elion. Je suis là pour parler avec vous sur Sonic.

Actuellement, je peux :
- Raconter 120 blagues
- 20 histoires
- Générer du texte
- Faire des notes
- Vous donner des solutions grâce aux recherches google
"""

model = genai.GenerativeModel('models/gemini-1.5-flash-8b-latest')
chat = model.start_chat(history=[])
chat.send_message(instructions_ia)

# --- Routes du Site Web ---

@app.route("/")
def home():
    return redirect(url_for("login"))

# Page de connexion
@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            error = "Pour continuer, veuillez remplir tous les champs."
        else:
            return redirect(url_for("chat_page"))
    return render_template("login.html", error=error)

# Page d'inscription
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not username or not email or not password:
            error = "Pour continuer, veuillez remplir tous les champs."
        else:
            return redirect(url_for("chat_page"))
    return render_template("Signup.html", error=error)

# Page de chat avec l'IA
@app.route("/chat", methods=["GET", "POST"])
def chat_page():
    message_utilisateur = ""
    reponse_ia = ""
    if request.method == "POST":
        message_utilisateur = request.form.get("message")
        try:
            reponse_ia = chat.send_message(message_utilisateur).text
        except Exception as e:
            reponse_ia = "ouh la !.j'ai rencontré un problème peux-tu réessayer ta question ?."
    return render_template("Chat.html", reponse_ia=reponse_ia)

import os

import os # Ajoutez cette ligne en haut de votre fichier si elle n'y est pas

# ... Votre code ...

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
