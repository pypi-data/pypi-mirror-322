from flask import Flask, request, jsonify
import os
import pyspiel
from agt_arena.game.go.go_search_problem import GoState


def create_bot_server(bot_factory, board_size):
    """Factory function to create a Flask server for any bot"""
    app = Flask(__name__)
    bot = bot_factory(board_size)
    print(f"BOT IN BOT SERVER AHHHHHHH {bot}")
    game = pyspiel.load_game("go", {"board_size": board_size})

    @app.route('/get_move', methods=['POST'])
    def get_move():
        serialized_state = request.json['game_state']
        time_remaining = request.json['time_remaining']
        game_state = GoState.deserialize(serialized_state, game)
        move = bot.get_move(game_state, time_remaining)
        return jsonify({'move': move})
        
    @app.route('/setup', methods=['POST'])
    def setup():
        player_data = request.json
        bot.on_start(player_data)
        return jsonify({'status': 'ready'})

    @app.route('/update', methods=['POST'])
    def update():
        serialized_state = request.json['game_state']
        game_state = GoState.deserialize(serialized_state, game)
        bot.on_update(game_state)
        return jsonify({'status': 'updated'})

    @app.route('/health', methods=['GET'])
    def health_check():
        print(str(bot))
        if str(bot) is None:
            return jsonify({'status': 'unhealthy'}), 100
        else:
            return jsonify({'status': 'healthy', 'name': str(bot)}), 200

    return app


def run_bot_server(bot_factory, board_size, port):
    """Convenience function to create and run a bot server"""
    print(f"Running bot server for {bot_factory.__name__} with board size {board_size}")
    app = create_bot_server(bot_factory, board_size)
    app.run(host='0.0.0.0', port=port, debug=True)