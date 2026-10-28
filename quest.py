import sys

class Character:
    def __init__(self, name, hp=100, energy=100):
        self.name = name
        self.max_hp = 100
        self.max_energy = 100

        self._hp = hp
        self._energy = energy
        self.status = "Нейтральный"

        self.update_status()
    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self.max_hp))
        self.update_status()

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = max(0, min(value, self.max_energy))
        self.update_status()

    def update_status(self):
        if self._hp <= 0:
            self.status = "Убит"
            return
        if self._hp < 50:
            self.status = "Раненый"
            return

        if self._energy >= 90:
            self.status = "Бодрый"
        elif self._energy >= 45:
            self.status = "Нейтральный"
        elif self._energy >= 15:
            self.status = "Уставший"
        else:
            self.status = "Сонливый"

    def display_stats(self):
        print(f"\n=== Персонаж - {self.name} ===")
        print(f"Здоровье: {self._hp}/{self.max_hp}")
        print(f"Энергия: {self._energy}/{self.max_energy}")
        print(f"Состояние: [{self.status}]")
        print("="*(20 + len(self.name)))

    def change_stats(self, hp_change=0, energy_change=0):
        if hp_change:
            self.hp += hp_change
        if energy_change:
            self.energy += energy_change

class GameEngine:
    def __init__(self, character):
        self.character = character

    def play_scene(self, scene_text, choices):
        if self.character.status == "Убит":
            print("\nИгра окончена. Вы мертвы")
            sys.exit()
        self.character.display_stats()
        print(f"\n{scene_text}\n")

        for idx, choice in enumerate(choices, 1):
            print(f"{idx}. {choice['text']}")

        while True:
            try:
                user_input = int(input("\nВыберите действие/фразу: "))
                if 1 <= user_input <= len(choices):
                    chosen_action = choices[user_input - 1]
                    break
                print("Неверный номер. Попробуйте ещё раз.")
            except ValueError:
                print("Пожалуйста, введите число.")

        print(f"\n-> {chosen_action['result_text']}")
        self.character.change_stats(
            hp_change=chosen_action.get('hp_effect', 0),
            energy_change=chosen_action.get('energy_effect', 0)
        )
        return chosen_action.get('next_scene', None)

if __name__ == "__main__":
    player = Character(name="")
    engine = GameEngine(player)

    scene_1 = {
        "text": "Вы просыпаетесь в заброшенном бункере. Сквозь щели в потолке пробивается свет, но вокруг сыро и холодно. Слышен странный шорох.",
        "choices": [
            {
                "text": "Резко вскочить и побежать на звук",
                "result_text": "Вы резко сорвались с места. Вы потратили прилично сил, так ещё и споткнулисьв темноте об арматуру.",
                "hp_effect": -15,
                "energy_effect": -30,
                "next_scene": "room_dark"
            },
            {
                "text": "Медленно осмотреться и прислушаться",
                "result_text": "Вы аккуратно оцениваете обстановку, экономя силы. Шорох прекратился.",
                "hp_effect": 0,
                "energy_effect": -2,
                "next_scene": "room_safe"
            },
            {
                "text": "Продолжить лежать и попытаться подремать",
                "result_text": "Вы проигнорировали звук, посчитва что это мало вероятно что-то серьёзное или опасное. Вы вздремнули на 20 минут",
                "hp_effect": 0,
                "energy_effect": 25,
                "next_scene": "room_sleep"
            }
        ]
    }

    next_step = engine.play_scene(scene_1["text"], scene_1["choices"])
    print(f"\n[Система] Переход к сцене: {next_step}")
    player.display_stats()