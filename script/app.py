from flask import Flask, request, redirect, url_for, render_template_string
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# === Utilisateurs et codes ===
mdp_utilisateurs = {
    "010":"Thomas",
    "21": "Roberto M.",
    "22": "JEAN-PHILIPPE C",
    "26": "ZACHARY G.",
    "28": "DAPHNE P",
    "33": "TOUPIN CHARLIE",
    "42": "meunier michael",
    "44": "MATHILDE V.",
    "45": "jeremie leblanc",
    "65": "megann d",
    "88": "JP RONALDI",
    "93": "ANGI",
    "97": "marie laurence",
    "98": "alyson trottier",
    "102": "ELOISE G",
    "127": "ELOI B",
    "136": "ALEXANNE M",
    "295": "VICKY",
    "796": "Mario Antonio",
    "797": "Mya M-D",
    "798": "Benjamin C.",
    "799": "LOUKA B.",
    "800": "EVE G.",
    "801": "Jasmine Roof",
    "802": "Aurore N.",
    "803": "Olivier B.",
    "804": "STEPHANIA",
    "805": "DAMIEN BG",
    "806": "Florence De C.",
    "807": "Eli B.",
    "808": "marie lou r",
    "810": "ROBERTO M",
    "811": "JACOB D",
    "815": "SHANIE S",
    "820": "MONGRAIN MYA",
    "823": "FERRON DAVID",
    "828": "Jasmine R",
    "829": "Élodie G",
    "835": "Juliette DB",
    "839": "Franck T",
    "840": "Max-Antoine D",
    "841": "Emerick S.",
    "843": "Pascale B.",
    "847": "Allison S",
    "850": "Madyson V.",
    "851": "Émile T.",
    "852": "Laurence R.",
    "853": "Marie-Joelle R.",
    "854": "Joanie B.",
    "855": "Mégane B.",
    "856": "Juliette B.",
    "858": "Marianne M.",
    "861": "Élie SY",
    "863": "Sandrine N.",
    "869": "Maryane B.",
    "871": "Corina L.",
    "872": "Anthony R.",
    "873": "Marie-Lune S.",
    "878": "Mélissa H.",
    "880": "Isabelle C.",
    "882": "Rose B.",
    "883": "Alexann M.",
    "888": "Lauralie H.",
    "890": "Sharlee M.",
    "891": "Josiane B.",
    "892": "Martine R.",
    "893": "Aurélie C",
    "898": "Maggie Lajoie",
    "8742": "Invité"
}

# === Dossiers et fichiers ===
DATA_DIR = Path(".")
ZONE_FILES = {
    "Bar Simply": DATA_DIR / "reponses_barsimpl.txt",
    "Bar TDD": DATA_DIR / "reponses_barttd.txt",
    "Loges": DATA_DIR / "reponses_loge.txt",
    "Nord": DATA_DIR / "reponses_nord.txt",
    "Poutinerie": DATA_DIR / "reponses_pout.txt",
    "Principale": DATA_DIR / "reponses_princip.txt",
    "Sud": DATA_DIR / "reponses_sud.txt",
    "Zone TDD": DATA_DIR / "reponses_zonetdd.txt"
}

COMPLETED_FILE = DATA_DIR / "commandes_completees.txt"
BACKGROUND_URL = "https://content.sportslogos.net/logos/14/6791/full/trois-rivieres_lions_logo_primary_2022_sportslogosnet-6497.png"

# === Templates ===

PASSWORD_PAGE = """
<!doctype html>
<html>
<head><title>Connexion</title></head>
<body style="position: relative; font-family: Arial;">
<div style="
    background-image: url('{{ background_url }}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    opacity: 0.2;
    z-index: -1;
"></div>

<h2>Connexion</h2>
<form method="post">
<input type="text" name="user_id" placeholder="Entrez votre code" required autofocus><br>
<button type="submit">Valider</button>
</form>
<p style="color:red;">{{ error }}</p>
</body></html>
"""

MENU_PAGE = """
<!doctype html>
<html>
<head><title>Menu</title></head>
<body style="position: relative; font-family: Arial;">
<div style="
    background-image: url('{{ background_url }}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    opacity: 0.2;
    z-index: -1;
"></div>

<h2>Menu - Choisissez une zone</h2>
<ul>
{% for zone in zones %}
    <li><a href="{{ url_for('zone', zone_name=zone) }}">{{ zone }}</a></li>
{% endfor %}
<li><a href="{{ url_for('password') }}">Déconnexion</a></li>
</ul>
</body></html>
"""

ZONE_PAGE = """
<!doctype html>
<html>
<head>
    <title>Commande - {{ zone }}</title>
</head>
<body style="position: relative; font-family: Arial;">
<div style="
    background-image: url('{{ background_url }}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    opacity: 0.2;
    z-index: -1;
"></div>

<h2>Zone: {{ zone }}</h2>

<form method="post">
    <input type="text" name="commande" placeholder="Entrez une commande" required autofocus>
    <label><input type="checkbox" name="urgent"> Urgent</label>
    <button type="submit">Ajouter</button>
</form>

<h3>Commandes en cours</h3>
<ul>
{% for line in commandes %}
    <li style="color:{{ 'red' if '[URGENT]' in line else 'black' }};">
        {% if '[URGENT]' in line %}
            {{ line.replace('[URGENT]', '').strip() }}
        {% else %}
            {{ line }}
        {% endif %}
        <form method="post" action="{{ url_for('zone_delete', zone_name=zone, index=loop.index0) }}" style="display:inline;">
            <button type="submit">🗑️</button>
        </form>
    </li>
{% endfor %}
</ul>

<p>Retour au <a href="{{ url_for('menu') }}">menu</a>.</p>
</body>
</html>
"""

RUNNER_PAGE = """
<!doctype html>
<html>
<head>
<title>Runner</title>
<style>
body { position: relative; font-family: Arial; }
.background {
    background-image: url('{{ background_url }}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    opacity: 0.2;
    z-index: -1;
}
</style>
<script>
function refreshRunner() {
    fetch("/runner_data")
        .then(response => response.text())
        .then(html => {
            document.getElementById("runner-content").innerHTML = html;
        });
}
// Rafraîchissement toutes les 5 secondes
setInterval(refreshRunner, 5000);
</script>
</head>
<body>
<div class="background"></div>

<h2>Accès Runner - Toutes les réponses</h2>
<div id="runner-content">
{% for zone, content in responses.items() %}
<h3>{{ zone }}</h3>
<ul>
{% for line in content.splitlines() %}
<li>
    {% if '[URGENT]' in line %}
        <span style="color:red;">{{ line.replace('[URGENT]', '').strip() }}</span>
    {% else %}
        {{ line }}
    {% endif %}
    <form style="display:inline;" method="post" action="{{ url_for('complete_command', zone_name=zone, index=loop.index0) }}">
        <button type="submit">✅</button>
    </form>
    <form style="display:inline;" method="post" action="{{ url_for('delete_command', zone_name=zone, index=loop.index0) }}">
        <button type="submit">🗑️</button>
    </form>
</li>
{% endfor %}
</ul>
<hr>
{% endfor %}
</div>

<a href="{{ url_for('password') }}">Déconnexion</a>
</body>
</html>
"""

RUNNER_DATA = """
{% for zone, content in responses.items() %}
<h3>{{ zone }}</h3>
<ul>
{% for line in content.splitlines() %}
<li>
    {% if '[URGENT]' in line %}
        <span style="color:red;">{{ line.replace('[URGENT]', '').strip() }}</span>
    {% else %}
        {{ line }}
    {% endif %}
    <form style="display:inline;" method="post" action="{{ url_for('complete_command', zone_name=zone, index=loop.index0) }}">
        <button type="submit">✅</button>
    </form>
    <form style="display:inline;" method="post" action="{{ url_for('delete_command', zone_name=zone, index=loop.index0) }}">
        <button type="submit">🗑️</button>
    </form>
</li>
{% endfor %}
</ul>
<hr>
{% endfor %}
"""

# === Routes ===
@app.route("/", methods=["GET", "POST"])
def password():
    error = ""
    if request.method == "POST":
        user_id = request.form.get("user_id", "").strip()
        if user_id == "2733":
            return redirect(url_for("runner"))
        elif user_id == "1943":
            return redirect(url_for("completed"))
        elif user_id in mdp_utilisateurs:
            response = redirect(url_for("menu"))
            response.set_cookie("user_id", user_id)
            return response
        else:
            error = "Code incorrect"
    return render_template_string(PASSWORD_PAGE, error=error, background_url=BACKGROUND_URL)

@app.route("/menu")
def menu():
    return render_template_string(MENU_PAGE, zones=list(ZONE_FILES.keys()), background_url=BACKGROUND_URL)

@app.route("/zone/<zone_name>", methods=["GET", "POST"])
def zone(zone_name):
    if zone_name not in ZONE_FILES:
        return "Zone inconnue", 404
    file_path = ZONE_FILES[zone_name]
    user_id = request.cookies.get("user_id")
    if not user_id or user_id not in mdp_utilisateurs:
        return redirect(url_for("password"))

    if request.method == "POST":
        commande = request.form.get("commande", "").strip()
        urgent = request.form.get("urgent")
        if commande:
            if urgent:
                commande += " [URGENT]"
            # On n'écrit plus le nom de l'utilisateur
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"{commande}\n")

    commandes = file_path.read_text(encoding="utf-8").splitlines() if file_path.exists() else []
    return render_template_string(ZONE_PAGE, zone=zone_name, commandes=commandes, background_url=BACKGROUND_URL)

@app.route("/zone_delete/<zone_name>/<int:index>", methods=["POST"])
def zone_delete(zone_name, index):
    if zone_name not in ZONE_FILES:
        return "Zone inconnue", 404
    file_path = ZONE_FILES[zone_name]
    if not file_path.exists():
        return redirect(url_for("zone", zone_name=zone_name))
    lines = file_path.read_text(encoding="utf-8").splitlines()
    if 0 <= index < len(lines):
        del lines[index]
    file_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return redirect(url_for("zone", zone_name=zone_name))

@app.route("/runner")
def runner():
    responses = {zone: f.read_text(encoding='utf-8') if f.exists() else "" for zone, f in ZONE_FILES.items()}
    return render_template_string(RUNNER_PAGE, responses=responses, background_url=BACKGROUND_URL)

@app.route("/runner_data")
def runner_data():
    responses = {zone: f.read_text(encoding='utf-8') if f.exists() else "" for zone, f in ZONE_FILES.items()}
    return render_template_string(RUNNER_DATA, responses=responses)

@app.route("/complete/<zone_name>/<int:index>", methods=["POST"])
def complete_command(zone_name, index):
    if zone_name not in ZONE_FILES:
        return "Zone inconnue", 404
    file_path = ZONE_FILES[zone_name]
    if not file_path.exists():
        return redirect(url_for("runner"))
    lines = file_path.read_text(encoding="utf-8").splitlines()
    if 0 <= index < len(lines):
        completed = lines.pop(index)
        completed_clean = completed.replace("[URGENT]", "").strip()
        today_str = datetime.now().strftime("%d %B %Y")
        # Vérifie si la date est déjà dans le fichier pour éviter doublon
        content = COMPLETED_FILE.read_text(encoding="utf-8") if COMPLETED_FILE.exists() else ""
        header = f"=== {today_str} ==="
        if header not in content:
            with open(COMPLETED_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n{header}\n")
        with open(COMPLETED_FILE, "a", encoding="utf-8") as f:
            f.write(f"{zone_name} - {completed_clean}\n")
        file_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return redirect(url_for("runner"))

@app.route("/delete_command/<zone_name>/<int:index>", methods=["POST"])
def delete_command(zone_name, index):
    if zone_name not in ZONE_FILES:
        return "", 404
    file_path = ZONE_FILES[zone_name]
    if not file_path.exists():
        return "", 404
    lines = file_path.read_text(encoding="utf-8").splitlines()
    if 0 <= index < len(lines):
        del lines[index]
    file_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return "", 204

# === Completed page ===
@app.route("/completed", methods=["GET", "POST"])
def completed():
    content = COMPLETED_FILE.read_text(encoding="utf-8") if COMPLETED_FILE.exists() else "Aucune commande complétée"
    jours = []
    if COMPLETED_FILE.exists():
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("===") and line.endswith("==="):
                jours.append(line.strip())
    return render_template_string("""
    <!doctype html>
    <html><head><title>Commandes complétées</title></head>
    <body style="position: relative; font-family: Arial;">
    <div style="
        background-image: url('{{ background_url }}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        opacity: 0.2;
        z-index: -1;
    "></div>

    <h2>Commandes complétées</h2>

    {% for jour in jours %}
        <h3>{{ jour }}</h3>
        <form method="post" action="{{ url_for('delete_day') }}">
            <input type="hidden" name="jour" value="{{ jour }}">
            <button type="submit">🗑️ Supprimer cette journée</button>
        </form>
    {% endfor %}

    <pre>{{ content }}</pre>
    <a href="{{ url_for('password') }}">Déconnexion</a>
    </body></html>
    """, content=content, jours=jours, background_url=BACKGROUND_URL)

@app.route("/delete_day", methods=["POST"])
def delete_day():
    jour = request.form.get("jour")
    if COMPLETED_FILE.exists() and jour:
        lines = COMPLETED_FILE.read_text(encoding="utf-8").splitlines()
        new_lines = []
        skip = False
        for line in lines:
            if line.strip() == jour:
                skip = True
                continue
            if skip and line.startswith("===") and line.endswith("==="):
                skip = False
            if not skip:
                new_lines.append(line)
        COMPLETED_FILE.write_text("\n".join(new_lines) + ("\n" if new_lines else ""), encoding="utf-8")
    return redirect(url_for("completed"))

# === Main ===
if __name__ == "__main__":
    app.run(debug=True)
