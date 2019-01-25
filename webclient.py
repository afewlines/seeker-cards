
from random import shuffle

from flask import Flask, redirect, render_template, request, url_for
from flask_socketio import SocketIO, emit, join_room

from cards import DeckManager

app = Flask(__name__)
socketio = SocketIO(app)
decks = DeckManager()
players = {}  # {"drongle": [0, []], "dingle": [4, []]}
global chooser_ordered
chooser_ordered = []  # ["drongle", "dingle"]
global card_pot
card_pot = []
current_prompt = None
chooser = ""


@app.route('/', methods=['GET', 'POST'])
def index():
    global chooser_ordered
    if request.method == 'POST':
        username = request.form['username'].lower()
        print("\n\nADDING", username)
        players[username] = [0, []]
        chooser_ordered.append(username)
        for idx in range(10):
            players[username][1].append(decks.get_card('response'))
        return redirect("/play/{}".format(username))

    return render_template('index.html')


@app.route('/play')
def play():
    return redirect(url_for('index'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        global chooser_ordered
        username = request.form['target']
        print("\n\nREMOVING", username)
        players.pop(username)
        chooser_ordered = [
            user for user in chooser_ordered if user != username]

    return render_template('admin.html', players=players)


@app.route('/play/<username>', methods=['GET', 'POST'])
def play_user(username):
    return render_template('play.html', username=username[:32].lower())


# SOCKET I/O

@socketio.on('user connect')
def user_connect(username):
    print("\n\nCONNECTING", username['data'])
    update_leaderboard()


@socketio.on('get hand')
def update_hand(username):
    username = username['data']
    hand = cards_to_string(players[username][1])
    emit('update hand', hand)


@socketio.on('get sub')
def update_subs():
    for sub in card_pot:
        subs = sub[0]
        for card in sub[1]:
            subs = "{}|{}".format(subs, decks.find_id(card))
        emit('recv sub', subs)


@socketio.on('winner')
def get_winner(username):
    print("\n\nWINNER", username['data'])
    players[username['data']][0] += 1
    emit('winner', username['data'], broadcast=True)
    start_game()


@socketio.on('submit cards')
def submit_cards(submission):
    global card_pot
    card_pot.append(submission['data'])
    socketio.emit('ping out', room='admin')
    # update hand
    temp = submission['data'][1]
    for i in range(len(temp)):
        players[submission['data'][0]][1] = [
            crd for crd in players[submission['data'][0]][1] if str(crd.id) != temp[i]]
        players[submission['data'][0]][1].append(decks.get_card('response'))
    if len(card_pot) == (len(players) - 1):
        shuffle(card_pot)
        emit('all in', broadcast=True)


@socketio.on('start game')
def start_game():
    global chooser_ordered
    global card_pot
    card_pot = []
    chooser = chooser_ordered.pop(0)
    chooser_ordered = chooser_ordered + [chooser]
    current_prompt = decks.get_card('prompt')
    emit('starting', chooser, broadcast=True)
    emit('update prompt', "{}{}".format(
        current_prompt.difference, current_prompt.text), broadcast=True)
    update_leaderboard()


@socketio.on('ping in')
def get_ping():
    print("\n\nRECV PING")


@socketio.on('room')
def room(target):
    join_room(target)

# HELPER FUNCTIONS


def update_leaderboard():
    leaderboard = ["{}: {}".format(player, players[player][0])
                   for player in players]
    emit('update leaderboard', "|".join(leaderboard), broadcast=True)


def cards_to_string(cards):
    out = ""
    for card in cards:
        out += "|{}".format(card.to_string())

    return out


if __name__ == '__main__':
    decks.load_cards("cards_master.csv")
    decks.form_decks()
    app.run(debug=True, host='156.12.226.2', port=8080)
