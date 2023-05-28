from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

from base import Arena
from classes import unit_classes
from equipment import Equipment
from unit import PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": None,
    "enemy": None,
}

arena = Arena()


@app.route('/')
def menu_page():
    return render_template('index.html')


@app.route('/fight/')
def start_fight():
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route('/fight/hit')
def hit():
    """
    Кнопка нанесения удара
    обновляем экран боя (нанесение удара) (шаблон fight.html)
    если игра идет - вызываем метод player.hit() экземпляра класса арены
    если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    """
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route('/fight/use-skill')
def use_skill():
    """
    Кнопка использования скилла
    """
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route('/fight/pass-turn')
def pass_turn():
    """
    Кнопка пропуск хода
    вызываем здесь функцию следующий ход (arena.next_turn())
    """
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route('/fight/end-fight')
def end_fight():
    """
    Кнопка завершения игры - переход в главное меню
    """
    arena.stop_game()
    return render_template('index.html', heroes=heroes)


@app.route('/choose-hero/', methods=['post', 'get'])
def choose_hero():
    """
    Кнопка выбор героя. 2 метода GET и POST
    на GET отрисовываем форму.
    на POST отправляем форму и делаем редирект на эндпоинт choose enemy
    """
    if request.method == 'GET':
        equipment = Equipment()

        header = 'Выберите героя'
        weapons = equipment.get_weapon_names()
        armors = equipment.get_armor_names()
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes,
        }

        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class_name = request.form['unit_class']

        # Проверить что класс с таким именем существует
        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class_name))

        player.equip_armor((Equipment().get_armor(armor_name)))
        player.equip_weapon((Equipment().get_weapon(weapon_name)))

        heroes['player'] = player
        return redirect(url_for('choose_enemy'))


@app.route('/choose-enemy/', methods=['post', 'get'])
def choose_enemy():
    """
    Кнопка выбор соперников. 2 метода GET и POST
    также на GET отрисовываем форму.
    а на POST отправляем форму и делаем редирект на начало битвы
    """
    if request.method == 'GET':
        header = "Выберите противника"
        equipment = Equipment()
        weapons = equipment.get_weapon_names()
        armors = equipment.get_armor_names()
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes,
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class_name = request.form['unit_class']

        # Проверить что класс с таким именем существует
        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class_name))

        enemy.equip_armor((Equipment().get_armor(armor_name)))
        enemy.equip_weapon((Equipment().get_weapon(weapon_name)))

        heroes['enemy'] = enemy
        return redirect(url_for('start_fight'))


if __name__ == '__main__':
    app.run()
