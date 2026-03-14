print("Project Started")

from graph import Graph

g = Graph()

g.add_user("A")

print(g.graph)

from graph import Graph

g = Graph()

g.add_user("A")
g.add_user("B")

g.add_friend("A","B")

print(g.graph)

from graph import Graph

g = Graph()

g.add_user("A")
g.add_user("B")
g.add_user("C")
g.add_user("D")
g.add_user("E")

g.add_friend("A","B")
g.add_friend("A","C")
g.add_friend("B","D")
g.add_friend("C","E")

print(g.suggest_friends("A"))

from flask import Flask, render_template, request, redirect, session, jsonify
from graph import Graph

app = Flask(__name__)
app.secret_key = "supersecretkey123"  # Required for sessions

g = Graph()  # Our social network graph

#  LOGIN PAGE 
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        if username:
            session['username'] = username
            g.add_user(username)  # Auto-add user to graph
            return redirect('/home')
    return render_template("login.html")


#  MAIN APP PAGE 
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect('/')
    return render_template("index.html", graph=g.graph, suggestions={}, current_user=session['username'])


# ADD USE
@app.route('/add_user', methods=['POST'])
def add_user_route():
    if 'username' not in session:
        return redirect('/')
    user = request.form['user'].strip()
    if user:
        g.add_user(user)
    return redirect('/home')


#  ADD FRIEND 
@app.route('/add_friend', methods=['POST'])
def add_friend_route():
    if 'username' not in session:
        return redirect('/')
    user1 = request.form['user1'].strip()
    user2 = request.form['user2'].strip()
    if user1 and user2:
        g.add_user(user1)
        g.add_user(user2)
        g.add_friend(user1, user2)
    return redirect('/home')


# SUGGEST FRIENDS 
@app.route('/suggestions', methods=['POST'])
def suggestions():
    if 'username' not in session:
        return redirect('/')
    user = request.form['user'].strip()
    ranked = g.ranked_suggestions(user) if user else []
    return render_template("index.html", graph=g.graph, suggestions=ranked, current_user=session['username'])


#  LOGOUT 
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


#  GRAPH DATA FOR VISUALIZATION 
@app.route('/graph_data')
def graph_data():
    nodes = [{"id": u, "label": u} for u in g.graph]
    edges = []
    for u in g.graph:
        for v in g.graph[u]:
            edges.append({"from": u, "to": v})
    return jsonify({"nodes": nodes, "edges": edges})


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()