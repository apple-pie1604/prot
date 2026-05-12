from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
from plyer import vibrator
import asyncio

MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', 'А': '.-', 'Б': '-...', 'В': '.--', 'Г': '--.', 'Д': '-..', 'Е': '.', 'Ё': '.',
    'Ж': '...-', 'З': '--..', 'И': '..', 'Й': '.---', 'К': '-.-', 'Л': '.-..',
    'М': '--', 'Н': '-.', 'О': '---', 'П': '.--.', 'Р': '.-.', 'С': '...', 'Т': '-',
    'У': '..-', 'Ф': '..-.', 'Х': '....', 'Ц': '-.-.', 'Ч': '---.', 'Ш': '----',
    'Щ': '--.-', 'Ъ': '--.--', 'Ы': '-.--', 'Ь': '-..-', 'Э': '..-..', 'Ю': '..--',
    'Я': '.-.-', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': ' '
}


class MorseApp(App):
    if platform == 'android':
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
        ])
        except ImportError:
            print("Библиотека android не найдена")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input = None
        self.label = None
        self.layout = None
        self.morse_sequence = ''
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.input = TextInput(hint_text="Введите текст", multiline=False, font_size=32)
        self.label = Label(text="Код появится здесь", halign='center', text_size=(400, None))

        btn_convert = Button(text="Конвертировать", background_color=(0, 0.7, 0.9, 1))
        btn_convert.bind(on_press=self.convert)

        btn_play = Button(text="Вибрировать", background_color=(0.2, 0.8, 0.2, 1))
        btn_play.bind(on_press=self.start_vibration)

        self.layout.add_widget(self.input)
        self.layout.add_widget(btn_convert)
        self.layout.add_widget(self.label)
        self.layout.add_widget(btn_play)

        self.morse_sequence = ""
        return self.layout

    def convert(self, instance):
        text = self.input.text.upper()
        res = [MORSE_DICT.get(char, '') for char in text]
        self.morse_sequence = " ".join(res)
        self.label.text = self.morse_sequence

    def start_vibration(self, instance):
        # Запуск асинхронного цикла в основном потоке через Clock
        Clock.schedule_once(lambda dt: asyncio.ensure_future(self.play_morse()), 0)

    async def play_morse(self):
        for char in self.morse_sequence:
            if char == '.':
                vibrator.vibrate(0.1)
                await asyncio.sleep(0.2)
            elif char == '-':
                vibrator.vibrate(0.4)
                await asyncio.sleep(0.5)
            elif char == ' ':
                await asyncio.sleep(0.3)
            else:
                await asyncio.sleep(0.1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(MorseApp().async_run())