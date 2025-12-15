from flask import Flask, render_template, request, session, redirect, url_for
from game_logic import ValueJourneyGame

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_for_session'


@app.before_request
def make_session_permanent():
    session.permanent = True


# --- 辅助函数：处理 Session 存取 ---
def get_game_from_session():
    """从 session 中读取数据并重建游戏对象"""
    game_data = session.get('game_data')
    game = ValueJourneyGame()  # 创建一个新实例
    if game_data:
        game.load_from_dict(game_data)  # 将数据填入实例
    return game


def save_game_to_session(game):
    """将游戏对象转换为字典并存入 session"""
    session['game_data'] = game.to_dict()


# --------------------------------

@app.route('/')
def index():
    # 清空 session，准备新游戏
    session.pop('game_data', None)
    return render_template('start.html')


@app.route('/start_game', methods=['POST'])
def start_game():
    game = ValueJourneyGame()  # 新游戏
    player_name = request.form.get('player_name', '匿名同学').strip()
    game.player_name = player_name

    save_game_to_session(game)  # 保存状态
    return redirect(url_for('play'))


@app.route('/play')
def play():
    game = get_game_from_session()  # 读取状态

    current_data = game.get_current_data()

    # 这里的保存其实不是必须的，但为了保险起见，如果有状态变更则保存
    save_game_to_session(game)

    if current_data['type'] == 'summary':
        return render_template('summary.html', summary=current_data)

    return render_template('play_scene.html', data=current_data)


@app.route('/submit', methods=['POST'])
def submit():
    game = get_game_from_session()  # 读取状态

    try:
        choice_index = int(request.form.get('choice_index'))
    except (ValueError, TypeError):
        return redirect(url_for('play'))

    current_data = game.get_current_data()

    if current_data['type'] == 'scene':
        feedback_data = game.handle_scene_choice(choice_index)

    elif current_data['type'] == 'knowledge':
        feedback_data = game.handle_knowledge_choice(choice_index)

    else:
        return redirect(url_for('play'))

    save_game_to_session(game)  # 关键：处理完逻辑后，将更新后的状态存回 session

    return render_template('feedback.html', feedback=feedback_data, mode=current_data['type'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)