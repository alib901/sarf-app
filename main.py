
import random
import arabic_reshaper
from bidi.algorithm import get_display
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

Window.clearcolor = get_color_from_hex('#EFEFEF')
FONT_NAME = 'Vazir.ttf'

def f(text):
    try:
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    except:
        return text

CURRICULUM_DATA = {
    "1": {
        "title": "ادغام (Idgham)",
        "description": "ادغام به معنی داخل کردن یک حرف در حرف دیگر است، طوری که مشدد تلفظ شود.",
        "rules": "قاعده ۱: هرگاه دو حرف هم‌جنس کنار هم باشند و اولی ساکن و دومی متحرک باشد، ادغام واجب است.\n(مَدْدَ -> مَدَّ)\n\nقاعده ۲: اگر هر دو حرف متحرک باشند، اولی ساکن شده و در دومی ادغام می‌شود.\n(مَدَدَ -> مَدَّ)",
        "quiz": [
            {"q": "در کلمه 'مَدَدَ' چه نوع تغییری رخ می‌دهد؟", "a": "ادغام", "options": ["ادغام", "اعلال", "تخفیف"]},
            {"q": "شرط اصلی ادغام چیست؟", "a": "هم‌جنس بودن دو حرف", "options": ["هم‌جنس بودن دو حرف", "وجود حرف عله", "وجود همزه"]}
        ]
    },
    "2": {
        "title": "اعلال (I'lal)",
        "description": "تغییراتی که روی حروف عله (و، ی، ا) رخ می‌دهد تا تلفظ آسان‌تر شود.",
        "rules": "انواع اعلال:\n۱. اعلال به قلب: تبدیل حرف عله به حرف دیگر. (قَوَلَ -> قالَ)\n\n۲. اعلال به اسکان: ساکن کردن حرف عله متحرک. (یَقُولُ -> یَقُوْلُ)\n\n۳. اعلال به حذف: حذف حرف عله در برخورد با ساکن. (قُولْ -> قُلْ)",
        "quiz": [
            {"q": "تبدیل 'قَوَلَ' به 'قالَ' چه نوع اعلالی است؟", "a": "اعلال به قلب", "options": ["اعلال به قلب", "اعلال به حذف", "اعلال به اسکان"]},
            {"q": "در فعل امر 'قُلْ' چه اتفاقی افتاده است؟", "a": "اعلال به حذف", "options": ["ادغام", "اعلال به حذف", "تخفیف همزه"]}
        ]
    },
    "3": {
        "title": "تخفیف همزه",
        "description": "تغییراتی که برای آسان کردن تلفظ همزه انجام می‌شود.",
        "rules": "قاعده ۱ (ابدال): تبدیل همزه ساکن به حرف مدی هم‌جنس حرکت ماقبل. (بُؤْس -> بُوس)\n\nقاعده ۲ (حذف): حذف همزه در برخی افعال کثیرالاستعمال. (أَخَذَ -> خُذْ)\n\nقاعده ۳ (تسهیل): تلفظ همزه بین همزه و حرف مدی.",
        "quiz": [
            {"q": "تبدیل 'بُؤْس' به 'بُوس' نمونه کدام قاعده است؟", "a": "ابدال", "options": ["ادغام", "ابدال", "نقل"]}
        ]
    }
}

class ScrollableLabel(ScrollView):
    def __init__(self, text="", font_size=18, color=(0,0,0,1), **kwargs):
        super().__init__(**kwargs)
        self.label = Label(text=f(text), font_name=FONT_NAME, font_size=font_size, color=color, size_hint_y=None, halign='right', valign='top', padding=(20, 20))
        self.label.bind(texture_size=self.label.setter('size'))
        self.add_widget(self.label)
    def update_text(self, new_text):
        self.label.text = f(new_text)

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(text=f("آموزش صرف عربی"), font_name=FONT_NAME, font_size=32, color=(0,0,0,1), size_hint_y=0.3))
        btn_idgham = Button(text=f("۱. ادغام و قواعد آن"), font_name=FONT_NAME, background_color=get_color_from_hex('#3498db'))
        btn_idgham.bind(on_press=lambda x: self.go_to_topic("1"))
        btn_ilal = Button(text=f("۲. اعلال و قواعد آن"), font_name=FONT_NAME, background_color=get_color_from_hex('#e67e22'))
        btn_ilal.bind(on_press=lambda x: self.go_to_topic("2"))
        btn_hamza = Button(text=f("۳. تخفیف همزه"), font_name=FONT_NAME, background_color=get_color_from_hex('#9b59b6'))
        btn_hamza.bind(on_press=lambda x: self.go_to_topic("3"))
        btn_quiz = Button(text=f("۴. آزمون جامع"), font_name=FONT_NAME, background_color=get_color_from_hex('#27ae60'))
        btn_quiz.bind(on_press=self.go_to_quiz)
        layout.add_widget(btn_idgham); layout.add_widget(btn_ilal); layout.add_widget(btn_hamza); layout.add_widget(Label(size_hint_y=0.1)); layout.add_widget(btn_quiz)
        self.add_widget(layout)
    def go_to_topic(self, topic_id):
        self.manager.get_screen('topic').load_lesson(topic_id)
        self.manager.current = 'topic'
    def go_to_quiz(self, instance):
        self.manager.get_screen('quiz').start_new_quiz()
        self.manager.current = 'quiz'

class TopicScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.title_label = Label(text="", font_name=FONT_NAME, font_size=28, color=get_color_from_hex('#2c3e50'), size_hint_y=0.15)
        layout.add_widget(self.title_label)
        self.content_scroll = ScrollableLabel(text="", font_size=20)
        layout.add_widget(self.content_scroll)
        back_btn = Button(text=f("بازگشت به منو"), font_name=FONT_NAME, size_hint_y=0.15, background_color=get_color_from_hex('#7f8c8d'))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(back_btn)
        self.add_widget(layout)
    def load_lesson(self, topic_id):
        data = CURRICULUM_DATA[topic_id]
        self.title_label.text = f(data['title'])
        self.content_scroll.update_text(f"تعریف:\n{data['description']}\n\nقواعد و مثال‌ها:\n{data['rules']}")

class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = []; self.current_q_index = 0; self.score = 0
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.status_label = Label(text="", font_name=FONT_NAME, font_size=18, color=(0.3,0.3,0.3,1), size_hint_y=0.1)
        layout.add_widget(self.status_label)
        self.question_label = Label(text="", font_name=FONT_NAME, font_size=24, color=(0,0,0,1), size_hint_y=0.3)
        layout.add_widget(self.question_label)
        self.option_buttons = []
        for i in range(3):
            btn = Button(text="", font_name=FONT_NAME, font_size=20, background_color=get_color_from_hex('#34495e'))
            btn.bind(on_press=self.check_answer)
            self.option_buttons.append(btn)
            layout.add_widget(btn)
        self.feedback_label = Label(text="", font_name=FONT_NAME, font_size=20, size_hint_y=0.2, color=(1,0,0,1))
        layout.add_widget(self.feedback_label)
        self.action_btn = Button(text=f("شروع"), font_name=FONT_NAME, size_hint_y=0.15, background_color=get_color_from_hex('#27ae60'))
        self.action_btn.bind(on_press=self.next_action)
        layout.add_widget(self.action_btn)
        self.add_widget(layout)
    def start_new_quiz(self):
        self.questions = []
        for key in CURRICULUM_DATA: self.questions.extend(CURRICULUM_DATA[key]["quiz"])
        random.shuffle(self.questions)
        self.current_q_index = 0; self.score = 0; self.is_finished = False; self.feedback_label.text = ""
        self.action_btn.text = f("سوال بعدی"); self.action_btn.background_color = get_color_from_hex('#27ae60')
        self.load_question()
    def load_question(self):
        if self.current_q_index < len(self.questions):
            q_data = self.questions[self.current_q_index]
            self.status_label.text = f(f"سوال {self.current_q_index + 1} از {len(self.questions)}")
            self.question_label.text = f(q_data['q'])
            self.feedback_label.text = ""
            opts = q_data['options'].copy(); random.shuffle(opts)
            for i, btn in enumerate(self.option_buttons):
                btn.text = f(opts[i]); btn.disabled = False; btn.background_color = get_color_from_hex('#34495e')
        else: self.finish_quiz()
    def check_answer(self, instance_btn):
        selected_ans = instance_btn.text; correct_ans = f(self.questions[self.current_q_index]['a'])
        if selected_ans == correct_ans:
            self.score += 1; self.feedback_label.text = f("✅ صحیح است!"); self.feedback_label.color = (0, 1, 0, 1)
        else:
            self.feedback_label.text = f(f"❌ غلط."); self.feedback_label.color = (1, 0, 0, 1)
        for btn in self.option_buttons: btn.disabled = True
        self.current_q_index += 1
    def finish_quiz(self):
        self.is_finished = True; self.status_label.text = f("پایان آزمون")
        self.question_label.text = f(f"امتیاز: {self.score} از {len(self.questions)}")
        self.feedback_label.text = ""; self.action_btn.text = f("بازگشت به منو"); self.action_btn.background_color = get_color_from_hex('#c0392b')
    def next_action(self, instance):
        if self.is_finished: self.manager.current = 'menu'
        else: self.load_question()

class ArabicSarfApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu')); sm.add_widget(TopicScreen(name='topic')); sm.add_widget(QuizScreen(name='quiz'))
        return sm

if __name__ == '__main__': ArabicSarfApp().run()
