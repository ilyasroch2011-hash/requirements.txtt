from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <title>Contrôle Complet - PC & Appareil</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: #e0e0e0; text-align: center; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: #1e1e1e; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h2, h3 { color: #00ffcc; }
        button, input[type="text"] { padding: 10px 15px; margin: 8px 0; border-radius: 5px; border: none; font-size: 15px; }
        button { background: #00ffcc; color: #121212; font-weight: bold; cursor: pointer; transition: 0.2s; }
        button:hover { background: #00b399; }
        .btn-danger { background: #ff4d4d; color: white; }
        .btn-danger:hover { background: #cc0000; }
        .grid-pad { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; max-width: 250px; margin: 15px auto; }
        .output { background: #2d2d2d; padding: 15px; border-radius: 5px; text-align: left; margin-top: 20px; font-family: monospace; white-space: pre-wrap; color: #00ffcc; }
        input[type="text"] { background: #2d2d2d; color: #fff; width: 60%; }
    </style>
</head>
<body>
  <div class="container">
    <h2>Panneau de Contrôle à Distance</h2>

    <!-- Section Alimentation -->
    <h3>Alimentation</h3>
    <form method="post">
        <button type="submit" name="action" value="eteindre" class="btn-danger">🔴 Éteindre l'appareil</button>
    </form>

    <hr style="border-color: #333; margin: 20px 0;">

    <!-- Section Contrôle du Curseur (Souris) -->
    <h3>Contrôle du Curseur</h3>
    <form method="post">
        <div class="grid-pad">
            <div></div>
            <button type="submit" name="action" value="souris_haut">⬆️ Haut</button>
            <div></div>
            <button type="submit" name="action" value="souris_gauche">⬅️ Gauche</button>
            <button type="submit" name="action" value="souris_clic">🖱️ Clic</button>
            <button type="submit" name="action" value="souris_droite">➡️ Droite</button>
            <div></div>
            <button type="submit" name="action" value="souris_bas">⬇️ Bas</button>
            <div></div>
        </div>
    </form>

    <hr style="border-color: #333; margin: 20px 0;">

    <!-- Section Commande Libre -->
    <h3>Commande Personnalisée</h3>
    <form method="post">
        <input type="text" name="command" placeholder="ex: ls,whoami...">
        <button type="submit">Exécuter</button>
    </form>

    {% if output %}
      <div class="output"><b>Résultat :</b>\n{{ output }}</div>
    {% endif %}
  </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        action = request.form.get('action')
        command = request.form.get('command')

        # Gestion du bouton Éteindre
        if action == "eteindre":
            # Sur Linux/Kali : 'sudo shutdown -h now' (attention à bien configurer le sudo sans mot de passe si besoin)
            result = subprocess.run("echo 'Simulation: Ordinateur éteint'", shell=True, capture_output=True, text=True)
            output = "Signal d'extinction envoyé."

        # Gestion du mouvement de la souris (nécessite l'outil xdotool sur Linux)
        elif action and action.startswith("souris_"):
            try:
                if action == "souris_haut":
                    subprocess.run("xdotool mousemove_relative -- 0 -50", shell=True)
                    output = "Curseur déplacé vers le haut."
                elif action == "souris_bas":
                    subprocess.run("xdotool mousemove_relative -- 0 50", shell=True)
                    output = "Curseur déplacé vers le bas."
                elif action == "souris_gauche":
                    subprocess.run("xdotool mousemove_relative -- -50 0", shell=True)
                    output = "Curseur déplacé vers la gauche."
                elif action == "souris_droite":
                    subprocess.run("xdotool mousemove_relative -- 50 0", shell=True)
                    output = "Curseur déplacé vers la droite."
                elif action == "souris_clic":
                    subprocess.run("xdotool click 1", shell=True)
                    output = "Clic de souris effectué."
            except Exception as e:
                output = f"Erreur xdotool (installez-le avec apt install xdotool) : {e}"

        # Gestion des commandes libres
        elif command:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout or result.stderr

    return render_template_string(HTML, output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)