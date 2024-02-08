from flask import Flask, request, redirect, url_for
import threading
import app  # This imports your Discord bot module

app = Flask(__name__)

# Define routes for starting and stopping the bot
@app.route('/')
def home():
    return '''
        <h1>Discord Bot Control Panel</h1>
        <form action="/start" method="post"><button type="submit">Start Bot</button></form>
        <form action="/stop" method="post"><button type="submit">Stop Bot</button></form>
    '''

@app.route('/start', methods=['POST'])
def start_bot():
    global bot_thread
    if 'bot_thread' not in globals() or not bot_thread.is_alive():
        bot_thread = threading.Thread(target=app.start_bot, daemon=True)
        bot_thread.start()
        return 'Bot is starting...', 202
    return 'Bot is already running.', 400

@app.route('/stop', methods=['POST'])
def stop_bot():
    if 'bot_thread' in globals() and bot_thread.is_alive():
        app.stop_bot()  # Call the stop function you defined in your bot module
        return 'Bot is stopping...', 202
    return 'Bot is not running.', 400

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)