from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
import webbrowser
from datetime import datetime
import json
import os

Window.clearcolor = (0.08, 0.08, 0.12, 1)

class DataManager:
    def __init__(self):
        self.db_file = 'micmac_betting.json'
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    data = json.load(f)
                    self.users = data.get('users', {})
                    self.free_tips = data.get('free_tips', [])
                    self.vip_tips = data.get('vip_tips', {'odds_2': [], 'odds_5': [], 'odds_10': [], 'alf': []})
                    self.subscription_codes = data.get('subscription_codes', {})
            except:
                self.init_empty_data()
        else:
            self.init_empty_data()
        self.current_user = None
        if 'Micmac' not in self.users:
            self.add_user('Micmac', 'Micmac@2025')
    
    def init_empty_data(self):
        self.users = {}
        self.free_tips = []
        self.vip_tips = {'odds_2': [], 'odds_5': [], 'odds_10': [], 'alf': []}
        self.subscription_codes = {}
    
    def save_data(self):
        data = {
            'users': self.users,
            'free_tips': self.free_tips,
            'vip_tips': self.vip_tips,
            'subscription_codes': self.subscription_codes
        }
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_user(self, username, password):
        self.users[username] = {'password': password, 'subscriptions': []}
        self.save_data()
    
    def verify_user(self, username, password):
        if username in self.users:
            return self.users[username]['password'] == password
        return False
    
    def add_subscription(self, username, package, code):
        if username in self.users:
            self.users[username]['subscriptions'].append({'package': package, 'code': code, 'date': datetime.now().strftime('%Y-%m-%d %H:%M')})
            self.save_data()
    
    def verify_code(self, username, package, code):
        if package in self.subscription_codes:
            if code in self.subscription_codes[package]:
                self.subscription_codes[package].remove(code)
                self.save_data()
                return True
        return False
    
    def has_subscription(self, username, package):
        if username in self.users:
            for sub in self.users[username]['subscriptions']:
                if sub['package'] == package:
                    return True
        return False
    
    def add_tip(self, tip_type, tip):
        if tip_type == 'free':
            self.free_tips.append(tip)
        else:
            self.vip_tips[tip_type].append(tip)
        self.save_data()
    
    def delete_tip(self, tip_type, index):
        if tip_type == 'free':
            if 0 <= index < len(self.free_tips):
                del self.free_tips[index]
        else:
            if 0 <= index < len(self.vip_tips[tip_type]):
                del self.vip_tips[tip_type][index]
        self.save_data()

data_manager = DataManager()

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.font_size = '15sp'
        self.bold = True
        self.size_hint_y = None
        self.height = dp(50)
        with self.canvas.before:
            self.rect_color = Color(0.2, 0.7, 0.4, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def set_color(self, r, g, b, a=1):
        self.rect_color.rgba = (r, g, b, a)

class Card(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = dp(15)
        self.spacing = dp(8)
        with self.canvas.before:
            Color(0.15, 0.15, 0.2, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')
        header = BoxLayout(size_hint_y=None, height=dp(80), padding=[dp(20), dp(15)])
        with header.canvas.before:
            Color(0.1, 0.1, 0.15, 1)
            self.header_rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda i, v: setattr(self.header_rect, 'pos', i.pos), size=lambda i, v: setattr(self.header_rect, 'size', i.size))
        logo = Label(text='MB', font_size='28sp', bold=True, color=(0.2, 0.8, 0.5, 1), size_hint_x=0.2)
        title_box = BoxLayout(orientation='vertical', size_hint_x=0.8)
        title = Label(text='MICMAC BETTING', font_size='26sp', bold=True, color=(0.2, 0.8, 0.5, 1), halign='left', size_hint_y=0.6)
        title.bind(size=title.setter('text_size'))
        subtitle = Label(text='Professional Betting Tips', font_size='12sp', color=(0.6, 0.6, 0.6, 1), halign='left', size_hint_y=0.4)
        subtitle.bind(size=subtitle.setter('text_size'))
        title_box.add_widget(title)
        title_box.add_widget(subtitle)
        header.add_widget(logo)
        header.add_widget(title_box)
        self.content_scroll = ScrollView(size_hint_y=0.82)
        self.content_area = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, padding=dp(15))
        self.content_area.bind(minimum_height=self.content_area.setter('height'))
        self.content_scroll.add_widget(self.content_area)
        footer = BoxLayout(size_hint_y=None, height=dp(70), padding=[dp(5), dp(8)], spacing=dp(5))
        with footer.canvas.before:
            Color(0.1, 0.1, 0.15, 1)
            self.footer_rect = Rectangle(pos=footer.pos, size=footer.size)
        footer.bind(pos=lambda i, v: setattr(self.footer_rect, 'pos', i.pos), size=lambda i, v: setattr(self.footer_rect, 'size', i.size))
        btn_free = self.create_footer_button('F', 'Free Tips', (0.2, 0.8, 0.5, 1), lambda x: self.show_section('free'))
        btn_vip = self.create_footer_button('V', 'VIP Tips', (0.9, 0.7, 0.2, 1), lambda x: self.show_section('vip'))
        btn_admin = self.create_footer_button('A', 'Admin', (0.6, 0.4, 0.8, 1), self.go_to_admin)
        footer.add_widget(btn_free)
        footer.add_widget(btn_vip)
        footer.add_widget(btn_admin)
        main_layout.add_widget(header)
        main_layout.add_widget(self.content_scroll)
        main_layout.add_widget(footer)
        self.add_widget(main_layout)
        self.show_section('free')
    
    def create_footer_button(self, icon_text, label_text, color, callback):
        btn_box = BoxLayout(orientation='vertical', spacing=dp(2))
        icon_box = BoxLayout(size_hint_y=0.55)
        icon_label = Label(text=icon_text, font_size='20sp', bold=True, color=color)
        icon_box.add_widget(icon_label)
        btn_text = Button(text=label_text, font_size='11sp', size_hint_y=0.45, background_color=(0, 0, 0, 0), color=color, bold=True)
        btn_text.bind(on_press=callback)
        btn_box.add_widget(icon_box)
        btn_box.add_widget(btn_text)
        return btn_box
    
    def show_section(self, section):
        self.content_area.clear_widgets()
        if section == 'free':
            section_title = Label(text='[b]FREE TIPS[/b]', markup=True, size_hint_y=None, height=dp(50), font_size='22sp', color=(0.2, 0.8, 0.5, 1))
            self.content_area.add_widget(section_title)
            self.load_free_tips()
        elif section == 'vip':
            section_title = Label(text='[b]VIP PACKAGES[/b]', markup=True, size_hint_y=None, height=dp(50), font_size='22sp', color=(0.9, 0.7, 0.2, 1))
            self.content_area.add_widget(section_title)
            self.load_vip_packages()
    
    def on_enter(self):
        self.show_section('free')
    
    def load_free_tips(self):
        if data_manager.free_tips:
            for tip in data_manager.free_tips:
                card = self.create_tip_card(tip)
                self.content_area.add_widget(card)
        else:
            card = Card(height=dp(140))
            no_tips = Label(text='Hakuna free tips kwa sasa\nSubiri updates mpya!', color=(0.5, 0.5, 0.5, 1), font_size='14sp', halign='center')
            no_tips.bind(size=no_tips.setter('text_size'))
            card.add_widget(no_tips)
            self.content_area.add_widget(card)
    
    def create_tip_card(self, tip):
        card = Card(height=dp(120))
        match_label = Label(text=f"[b]{tip['match']}[/b]", markup=True, font_size='16sp', color=(1, 1, 1, 1), size_hint_y=0.4)
        pred_label = Label(text=f"Prediction: {tip['prediction']}", color=(0.7, 0.7, 0.7, 1), size_hint_y=0.3, font_size='14sp')
        odds_label = Label(text=f"Odds: {tip['odds']}", color=(0.2, 0.8, 0.5, 1), bold=True, size_hint_y=0.3, font_size='18sp')
        card.add_widget(match_label)
        card.add_widget(pred_label)
        card.add_widget(odds_label)
        return card
    
    def load_vip_packages(self):
        packages = [
            ('ODDS 2', 'Tsh 3,000', 'odds_2', '2X'),
            ('ODDS 5', 'Tsh 7,000', 'odds_5', '5X'),
            ('ODDS 10', 'Tsh 10,000', 'odds_10', '10X'),
            ('ALF HAKUNA MAMBO', 'Tsh 15,000', 'alf', 'ALL')
        ]
        for name, price, key, icon_text in packages:
            card = self.create_vip_card(name, price, key, icon_text)
            self.content_area.add_widget(card)
    
    def create_vip_card(self, name, price, key, icon_text):
        card = Card(height=dp(220))
        title_label = Label(text=f'[b]{icon_text} {name}[/b]', markup=True, font_size='18sp', color=(0.9, 0.7, 0.2, 1), size_hint_y=0.2)
        price_label = Label(text=price, color=(1, 1, 1, 1), size_hint_y=0.15, font_size='20sp', bold=True)
        if data_manager.vip_tips[key]:
            count_text = f"Available: {len(data_manager.vip_tips[key])} Tips"
            count_color = (0.2, 0.8, 0.5, 1)
        else:
            count_text = "Hakuna tips kwa sasa"
            count_color = (0.5, 0.5, 0.5, 1)
        count_label = Label(text=count_text, color=count_color, size_hint_y=0.15, font_size='12sp')
        btn_subscribe = RoundedButton(text='SUBSCRIBE NOW', size_hint_y=0.22)
        btn_subscribe.set_color(0.8, 0.5, 0)
        btn_subscribe.bind(on_press=lambda x: self.subscribe(name, price, key))
        btn_have_code = RoundedButton(text='NINA CODE', size_hint_y=0.22)
        btn_have_code.set_color(0.2, 0.7, 0.4)
        btn_have_code.bind(on_press=lambda x: self.enter_code_direct(key))
        card.add_widget(title_label)
        card.add_widget(price_label)
        card.add_widget(count_label)
        card.add_widget(btn_subscribe)
        card.add_widget(btn_have_code)
        return card
    
    def subscribe(self, package, price, key):
        self.manager.get_screen('subscription').set_package(package, price, key)
        self.manager.current = 'subscription'
    
    def enter_code_direct(self, package_key):
        self.manager.get_screen('code_entry').set_package_direct(package_key)
        self.manager.current = 'code_entry'
    
    def go_to_admin(self, instance):
        self.manager.current = 'login'

class SubscriptionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.package_name = ''
        self.package_price = ''
        self.package_key = ''
        main_layout = BoxLayout(orientation='vertical')
        header = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(15))
        with header.canvas.before:
            Color(0.1, 0.1, 0.15, 1)
            rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda i, v: setattr(rect, 'pos', i.pos), size=lambda i, v: setattr(rect, 'size', i.size))
        btn_back = Button(text='<', size_hint_x=0.15, font_size='24sp', background_color=(0, 0, 0, 0), color=(1, 1, 1, 1), bold=True)
        btn_back.bind(on_press=self.go_back)
        title = Label(text='Subscription', font_size='22sp', bold=True, size_hint_x=0.85, color=(0.9, 0.7, 0.2, 1))
        header.add_widget(btn_back)
        header.add_widget(title)
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=dp(20), size_hint_y=None, padding=dp(20))
        content.bind(minimum_height=content.setter('height'))
        self.info_card = Card(height=dp(100))
        self.info_label = Label(text='', font_size='18sp', bold=True, color=(0.9, 0.7, 0.2, 1))
        self.info_card.add_widget(self.info_label)
        content.add_widget(self.info_card)
        payment_card = Card(height=dp(150))
        pay_layout = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(5))
        pay_title = Label(text='Malipo ya Airtel Money', size_hint_y=0.25, font_size='16sp', bold=True, color=(1, 1, 1, 1))
        pay_number = Label(text='0689268545', size_hint_y=0.35, font_size='26sp', bold=True, color=(0.2, 0.8, 0.5, 1))
        pay_name = Label(text='Jina: Maiko Maiko', size_hint_y=0.2, font_size='14sp', color=(0.7, 0.7, 0.7, 1))
        pay_note = Label(text='Lipia kwanza kisha endelea', size_hint_y=0.2, font_size='12sp', color=(0.9, 0.7, 0.2, 1))
        pay_layout.add_widget(pay_title)
        pay_layout.add_widget(pay_number)
        pay_layout.add_widget(pay_name)
        pay_layout.add_widget(pay_note)
        payment_card.add_widget(pay_layout)
        content.add_widget(payment_card)
        form_card = Card(height=dp(180))
        form_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        form_title_text = Label(text='Jaza Taarifa Zako', size_hint_y=0.2, font_size='15sp', bold=True, color=(1, 1, 1, 1))
        self.name_input = TextInput(multiline=False, hint_text='Weka jina lako', size_hint_y=0.4, font_size='14sp', background_color=(0.2, 0.2, 0.25, 1), foreground_color=(1, 1, 1, 1), cursor_color=(0.2, 0.8, 0.5, 1), padding=[dp(15), dp(10)])
        self.password_input = TextInput(multiline=False, password=True, hint_text='Chagua password', size_hint_y=0.4, font_size='14sp', background_color=(0.2, 0.2, 0.25, 1), foreground_color=(1, 1, 1, 1), cursor_color=(0.2, 0.8, 0.5, 1), padding=[dp(15), dp(10)])
        form_layout.add_widget(form_title_text)
        form_layout.add_widget(self.name_input)
        form_layout.add_widget(self.password_input)
        form_card.add_widget(form_layout)
        content.add_widget(form_card)
        self.status_label = Label(text='', size_hint_y=None, height=dp(35), font_size='13sp', color=(1, 0.3, 0.3, 1))
        content.add_widget(self.status_label)
        btn_whatsapp = RoundedButton(text='Tuma Screenshot WhatsApp')
        btn_whatsapp.set_color(0.15, 0.6, 0.3)
        btn_whatsapp.bind(on_press=self.open_whatsapp)
        content.add_widget(btn_whatsapp)
        scroll.add_widget(content)
        main_layout.add_widget(header)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)
    
    def set_package(self, name, price, key):
        self.package_name = name
        self.package_price = price
        self.package_key = key
        self.info_label.text = f'{name}\n{price}'
    
    def open_whatsapp(self, instance):
        username = self.name_input.text.strip()
        password = self.password_input.text.strip()
        if not username or not password:
            self.status_label.text = 'Jaza jina na password!'
            return
        data_manager.add_user(username, password)
        message = f"Nimelipia VIP: {self.package_name}%0AJina: {username}%0ANipe code za kufungua"
        whatsapp_url = f"https://wa.me/255689268545?text={message}"
        webbrowser.open(whatsapp_url)
        self.manager.get_screen('code_entry').set_user_package(username, self.package_key)
        self.manager.current = 'code_entry'
    
    def go_back(self, instance):
        self.manager.current = 'home'

class CodeEntryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = ''
        self.package_key = ''
        main_layout = BoxLayout(orientation='vertical')
        header = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(15))
        with header.canvas.before:
            Color(0.1, 0.1, 0.15, 1)
            rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda i, v: setattr(rect, 'pos', i.pos), size=lambda i, v: setattr(rect, 'size', i.size))
        title = Label(text='Enter Code', font_size='22sp', bold=True, color=(0.9, 0.7, 0.2, 1))
        header.add_widget(title)
        content = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(30))
        info = Label(text='Weka code uliyopewa na admin', size_hint_y=0.12, font_size='14sp', color=(0.7, 0.7, 0.7, 1))
        
        form_card = Card(height=dp(150))
        form_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        self.username_input = TextInput(multiline=False, hint_text='Weka jina lako', size_hint_y=0.45, font_size='14sp', background_color=(0.2, 0.2, 0.25, 1), foreground_color=(1, 1, 1, 1), cursor_color=(0.2, 0.8, 0.5, 1), padding=[dp(15), dp(10)])
        self.code_input = TextInput(multiline=False, hint_text='Weka code hapa', size_hint_y=0.45, font_size='16sp', background_color=(0.2, 0.2, 0.25, 1), foreground_color=(1, 1, 1, 1), cursor_color=(0.2, 0.8, 0.5, 1), padding=[dp(15), dp(15)])
        form_layout.add_widget(self.username_input)
        form_layout.add_widget(self.code_input)
        form_card.add_widget(form_layout)
        
        self.status_label = Label(text='', size_hint_y=None, height=dp(40), font_size='13sp')
        btn_verify = RoundedButton(text='Thibitisha Code')
        btn_verify.set_color(0.2, 0.7, 0.4)
        btn_verify.bind(on_press=self.verify_code)
        btn_home = RoundedButton(text='Rudi Home')
        btn_home.set_color(0.3, 0.3, 0.35)
        btn_home.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        content.add_widget(info)
        content.add_widget(form_card)
        content.add_widget(self.status_label)
        content.add_widget(btn_verify)
        content.add_widget(btn_home)
        main_layout.add_widget(header)
        main_layout.add_widget(content)
        self.add_widget(main_layout)
    
    def set_user_package(self, username, package_key):
        self.username = username
        self.package_key = package_key
        self.username_input.text = username
    
    def set_package_direct(self, package_key):
        self.package_key = package_key
        self.username = ''
        self.username_input.text = ''
    
    def verify_code(self, instance):
        username = self.username_input.text.strip()
        code = self.code_input.text.strip()
        if not username or not code:
            self.status_label.text = 'Jaza jina na code!'
            self.status_label.color = (1, 0.3, 0.3, 1)
            return
        if data_manager.verify_code(username, self.package_key, code):
            data_manager.add_subscription(username, self.package_key, code)
            data_manager.current_user = username
            self.status_label.text = 'Code sahihi!'
            self.status_label.color = (0.2, 0.8, 0.5, 1)
            self.manager.get_screen('vip_tips').set_package(self.package_key)
            self.manager.current = 'vip_tips'
        else:
            self.status_label.text = 'Code si sahihi!'
            self.status_label.color = (1, 0.3, 0.3, 1)

class VIPTipsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_package = 'odds_2'
        main_layout = BoxLayout(orientation='vertical')
        header = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(15))
        with header.canvas.before:
            Color(0.1, 0.1, 0.15, 1)
            rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda i, v: setattr(rect, 'pos', i.pos), size=lambda i, v: setattr(rect, 'size', i.size))
        btn_back = Button(text='<', size_hint_x=0.15, font_size='24sp', background_color=(0, 0, 0, 0), color=(1, 1, 1, 1), bold=True)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        self.title_label = Label(text='VIP Tips', font_size='22sp', bold=True, size_hint_x=0.85, color=(0.9, 0.7, 0.2, 1))
        header.add_widget(btn_back)
        header.add_widget(self.title_label)
        scroll = ScrollView()
        self.content = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, padding=dp(15))
        self.content.bind(minimum_height=self.content.setter('height'))
        scroll.add_widget(self.content)
        main_layout.add_widget(header)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)
    
    def set_package(self, package_key):
        self.current_package = package_key
        package_names = {
            'odds_2': 'ODDS 2',
            'odds_5': 'ODDS 5',
            'odds_10': 'ODDS 10',
            'alf': 'ALF'
        }
        self.title_label.text = f'{package_names.get(package_key, "VIP")} Tips'
    
    def on_enter(self):
        self.content.clear_widgets()
        tips = data_manager.vip_tips.get(self.current_package, [])
        if tips:
            for tip in tips:
                card = self.create_vip_tip_card(tip)
                self.content.add_widget(card)
        else:
            card = Card(height=dp(140))
            no_tips = Label(text='Hakuna tips kwa sasa\nkwenye package hii', color=(0.5, 0.5, 0.5, 1), font_size='14sp', halign='center')
            no_tips.bind(size=no_tips.setter('text_size'))
            card.add_widget(no_tips)
            self.content.add_widget(card)
    
    def create_vip_tip_card(self, tip):
        card = Card(height=dp(140))
        badge = Label(text='[b]VIP[/b]', markup=True, font_size='12sp', color=(0.9, 0.7, 0.2, 1), size_hint_y=0.2)
        match_label = Label(text=f"[b]{tip['match']}[/b]", markup=True, font_size='16sp', color=(1, 1, 1, 1), size_hint_y=0.35)
        pred_label = Label(text=f"Prediction: {tip['prediction']}", color=(0.7, 0.7, 0.7, 1), size_hint_y=0.25, font_size='13sp')
        odds_label = Label(text=f"Odds: {tip['odds']}", color=(0.9, 0.7, 0.2, 1), bold=True, size_hint_y=0.2, font_size='20sp')
        card.add_widget(badge)
        card.add_widget(match_label)
        card.add_widget(pred_label)
        card.add_widget(odds_label)
        return card

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')
        header = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(15))
        with header.canvas.before:
            Color(0.1, 0.1, 0.15, 1)
            rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda i, v: setattr(rect, 'pos', i.pos), size=lambda i, v: setattr(rect, 'size', i.size))
        btn_back = Button(text='<', size_hint_x=0.15, font_size='24sp', background_color=(0, 0, 0, 0), color=(1, 1, 1, 1), bold=True)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        title = Label(text='Admin Login', font_size='22sp', bold=True, size_hint_x=0.85, color=(0.6, 0.4, 0.8, 1))
        header.add_widget(btn_back)
        header.add_widget(title)
        content = BoxLayout(orientation='vertical', spacing=dp(25), padding=dp(30))
        form_card = Card(height=dp(200))
        form_layout = BoxLayout(orientation='vertical', spacing=dp(12), padding=dp(12))
        form_title_text = Label(text='Admin Access', size_hint_y=0.2, font_size='16sp', bold=True, color=(1, 1, 1, 1))
        self.username_input = TextInput(multiline=False, hint_text='Enter username', size_hint_y=0.4, font_size='14sp', background_color=(0.2, 0.2, 0.25, 1), foreground_color=(1, 1, 1, 1), cursor_color=(0.6, 0.4, 0.8, 1), padding=[dp(15), dp(10)])
        self.password_input = TextInput(multiline=False, password=True, hint_text='Enter password', size_hint_y=0.4, font_size='14sp', background_color=(0.2, 0.2, 0.25, 1), foreground_color=(1, 1, 1, 1), cursor_color=(0.6, 0.4, 0.8, 1), padding=[dp(15), dp(10)])
        form_layout.add_widget(form_title_text)
        form_layout.add_widget(self.username_input)
        form_layout.add_widget(self.password_input)
        form_card.add_widget(form_layout)
        self.error_label = Label(text='', size_hint_y=None, height=dp(35), font_size='13sp', color=(1, 0.3, 0.3, 1))
        btn_login = RoundedButton(text='Login')
        btn_login.set_color(0.6, 0.4, 0.8)
        btn_login.bind(on_press=self.login)
        content.add_widget(form_card)
        content.add_widget(self.error_label)
        content.add_widget(btn_login)
        main_layout.add_widget(header)
        main_layout.add_widget(content)
        self.add_widget(main_layout)
    
    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        if data_manager.verify_user(username, password) and username == 'Micmac':
            self.manager.current = 'admin'
            self.username_input.text = ''
            self.password_input.text = ''
            self.error_label.text = ''
        else:
            self.error_label.text = 'Username au Password si sahihi!'

class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')
        header = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(15))
        with header.canvas.before:
            Color(0.1, 0.1, 0.15, 1)
            rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda i, v: setattr(rect, 'pos', i.pos), size=lambda i, v: setattr(rect, 'size', i.size))
        title = Label(text='Admin Panel', font_size='22sp', bold=True, color=(0.6, 0.4, 0.8, 1))
        header.add_widget(title)
        tabs = BoxLayout(size_hint_y=None, height=dp(60), padding=dp(10), spacing=dp(8))
        self.btn_tips = RoundedButton(text='Tips', size_hint_x=0.33)
        self.btn_tips.set_color(0.2, 0.7, 0.4)
        self.btn_tips.bind(on_press=lambda x: self.show_section('tips'))
        self.btn_codes = RoundedButton(text='Codes', size_hint_x=0.33)
        self.btn_codes.set_color(0.25, 0.25, 0.3)
        self.btn_codes.bind(on_press=lambda x: self.show_section('codes'))
        self.btn_users = RoundedButton(text='Users', size_hint_x=0.34)
        self.btn_users.set_color(0.25, 0.25, 0.3)
        self.btn_users.bind(on_press=lambda x: self.show_section('users'))
        tabs.add_widget(self.btn_tips)
        tabs.add_widget(self.btn_codes)
        tabs.add_widget(self.btn_users)
        scroll = ScrollView(size_hint_y=0.78)
        self.content_area = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, padding=dp(15))
        self.content_area.bind(minimum_height=self.content_area.setter('height'))
        scroll.add_widget(self.content_area)
        footer = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(10))
        btn_logout = RoundedButton(text='Logout')
        btn_logout.set_color(0.7, 0.2, 0.2)
        btn_logout.bind(on_press=self.logout)
        footer.add_widget(btn_logout)
        main_layout.add_widget(header)
        main_layout.add_widget(tabs)
        main_layout.add_widget(scroll)
        main_layout.add_widget(footer)
        self.add_widget(main_layout)
        self.show_section('tips')
    
    def show_section(self, section):
        self.content_area.clear_widgets()
        self.btn_tips.set_color(0.25, 0.25, 0.3)
        self.btn_codes.set_color(0.25, 0.25, 0.3)
        self.btn_users.set_color(0.25, 0.25, 0.3)
        if section == 'tips':
            self.btn_tips.set_color(0.2, 0.7, 0.4)
            self.content_area.add_widget(self.create_tips_section())
        elif section == 'codes':
            self.btn_codes.set_color(0.8, 0.5, 0)
            self.content_area.add_widget(self.create_codes_section())
        elif section == 'users':
            self.btn_users.set_color(0.3, 0.5, 0.8)
            self.content_area.add_widget(self.create_users_section())
    
    def create_tips_section(self):
        section_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        section_layout.bind(minimum_height=section_layout.setter('height'))
        section_title = Label(text='Ongeza Tip Mpya', size_hint_y=None, height=dp(40), font_size='18sp', bold=True, color=(1, 1, 1, 1))
        form_card = Card(height=dp(300))
        form_box = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        self.match_input = TextInput(multiline=False, hint_text='Match (e.g. Man Utd vs Arsenal)', size_hint_y=None, height=dp(45), font_size='13sp', background_color=(0.2, 0.2, 0.25, 1), foreground_color=(1, 1, 1, 1), padding=[dp(12), dp(12)])
        self.prediction_input = TextInput(multiline=False, hint_text='Prediction (e.g. Over 2.5)', size_hint_y=None, height=dp(45), font_size='13sp', background_color=(0.2, 0.2, 0.25, 1), foreground_color=(1, 1, 1, 1), padding=[dp(12), dp(12)])
        self.odds_input = TextInput(multiline=False, hint_text='Odds (e.g. 1.85)', size_hint_y=None, height=dp(45), font_size='13sp', background_color=(0.2, 0.2, 0.25, 1), foreground_color=(1, 1, 1, 1), padding=[dp(12), dp(12)])
        self.tip_type = 'free'
        self.type_buttons = []
        type_btns = GridLayout(cols=3, spacing=dp(8), size_hint_y=None, height=dp(45))
        btn_free = RoundedButton(text='Free')
        btn_free.set_color(0.2, 0.7, 0.4)
        btn_free.bind(on_press=lambda x: self.select_tip_type('free', btn_free))
        self.type_buttons.append(btn_free)
        btn_odds2 = RoundedButton(text='Odds 2')
        btn_odds2.set_color(0.3, 0.3, 0.35)
        btn_odds2.bind(on_press=lambda x: self.select_tip_type('odds_2', btn_odds2))
        self.type_buttons.append(btn_odds2)
        btn_odds5 = RoundedButton(text='Odds 5')
        btn_odds5.set_color(0.3, 0.3, 0.35)
        btn_odds5.bind(on_press=lambda x: self.select_tip_type('odds_5', btn_odds5))
        self.type_buttons.append(btn_odds5)
        type_btns.add_widget(btn_free)
        type_btns.add_widget(btn_odds2)
        type_btns.add_widget(btn_odds5)
        type_btns2 = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(45))
        btn_odds10 = RoundedButton(text='Odds 10')
        btn_odds10.set_color(0.3, 0.3, 0.35)
        btn_odds10.bind(on_press=lambda x: self.select_tip_type('odds_10', btn_odds10))
        self.type_buttons.append(btn_odds10)
        btn_alf = RoundedButton(text='Alf')
        btn_alf.set_color(0.3, 0.3, 0.35)
        btn_alf.bind(on_press=lambda x: self.select_tip_type('alf', btn_alf))
        self.type_buttons.append(btn_alf)
        type_btns2.add_widget(btn_odds10)
        type_btns2.add_widget(btn_alf)
        form_box.add_widget(self.match_input)
        form_box.add_widget(self.prediction_input)
        form_box.add_widget(self.odds_input)
        form_box.add_widget(type_btns)
        form_box.add_widget(type_btns2)
        form_card.add_widget(form_box)
        self.add_status = Label(text='', size_hint_y=None, height=dp(35), font_size='13sp', color=(0.2, 0.8, 0.5, 1))
        btn_add = RoundedButton(text='Ongeza Tip', size_hint_y=None, height=dp(50))
        btn_add.set_color(0.2, 0.7, 0.4)
        btn_add.bind(on_press=self.add_tip)
        section_layout.add_widget(section_title)
        section_layout.add_widget(form_card)
        section_layout.add_widget(self.add_status)
        section_layout.add_widget(btn_add)
        tips_title = Label(text='Tips Zilizopo:', size_hint_y=None, height=dp(40), font_size='16sp', bold=True, color=(1, 1, 1, 1))
        section_layout.add_widget(tips_title)
        self.tips_container = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        self.tips_container.bind(minimum_height=self.tips_container.setter('height'))
        section_layout.add_widget(self.tips_container)
        self.refresh_tips_list()
        return section_layout
    
    def select_tip_type(self, tip_type, selected_button):
        self.tip_type = tip_type
        for btn in self.type_buttons:
            if btn == selected_button:
                if tip_type == 'free':
                    btn.set_color(0.2, 0.7, 0.4)
                else:
                    btn.set_color(0.8, 0.5, 0)
            else:
                btn.set_color(0.3, 0.3, 0.35)
        self.refresh_tips_list()
    
    def add_tip(self, instance):
        match = self.match_input.text.strip()
        prediction = self.prediction_input.text.strip()
        odds = self.odds_input.text.strip()
        if not match or not prediction or not odds:
            self.add_status.text = 'Jaza sehemu zote!'
            self.add_status.color = (1, 0.3, 0.3, 1)
            return
        tip = {'match': match, 'prediction': prediction, 'odds': odds}
        data_manager.add_tip(self.tip_type, tip)
        self.add_status.text = f'Tip imeongezwa kwenye {self.tip_type.upper()}!'
        self.add_status.color = (0.2, 0.8, 0.5, 1)
        self.match_input.text = ''
        self.prediction_input.text = ''
        self.odds_input.text = ''
        self.refresh_tips_list()
    
    def refresh_tips_list(self):
        self.tips_container.clear_widgets()
        if self.tip_type == 'free':
            tips = data_manager.free_tips
        else:
            tips = data_manager.vip_tips[self.tip_type]
        
        if tips:
            for idx, tip in enumerate(tips):
                tip_card = Card(height=dp(140))
                tip_layout = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(5))
                match_label = Label(text=f"[b]{tip['match']}[/b]", markup=True, size_hint_y=0.35, font_size='14sp', color=(1, 1, 1, 1))
                pred_label = Label(text=f"Pred: {tip['prediction']}", size_hint_y=0.25, font_size='12sp', color=(0.7, 0.7, 0.7, 1))
                odds_label = Label(text=f"Odds: {tip['odds']}", size_hint_y=0.2, font_size='14sp', color=(0.2, 0.8, 0.5, 1), bold=True)
                btn_delete = RoundedButton(text='Futa', size_hint_y=0.2)
                btn_delete.set_color(0.8, 0.2, 0.2)
                btn_delete.bind(on_press=lambda x, i=idx: self.delete_tip(i))
                tip_layout.add_widget(match_label)
                tip_layout.add_widget(pred_label)
                tip_layout.add_widget(odds_label)
                tip_layout.add_widget(btn_delete)
                tip_card.add_widget(tip_layout)
                self.tips_container.add_widget(tip_card)
        else:
            no_tips_card = Card(height=dp(80))
            no_tips = Label(text='Hakuna tips', color=(0.5, 0.5, 0.5, 1))
            no_tips_card.add_widget(no_tips)
            self.tips_container.add_widget(no_tips_card)
    
    def delete_tip(self, index):
        data_manager.delete_tip(self.tip_type, index)
        self.refresh_tips_list()
        self.add_status.text = 'Tip imefutwa!'
        self.add_status.color = (1, 0.5, 0, 1)
    
    def create_codes_section(self):
        section_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        section_layout.bind(minimum_height=section_layout.setter('height'))
        section_title = Label(text='Ongeza VIP Codes', size_hint_y=None, height=dp(40), font_size='18sp', bold=True, color=(1, 1, 1, 1))
        form_card = Card(height=dp(170))
        form_box = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        self.selected_package = 'odds_2'
        self.package_buttons = []
        pkg_btns = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(45))
        btn_o2 = RoundedButton(text='Odds 2')
        btn_o2.set_color(0.8, 0.5, 0)
        btn_o2.bind(on_press=lambda x: self.select_package('odds_2', btn_o2))
        self.package_buttons.append(btn_o2)
        btn_o5 = RoundedButton(text='Odds 5')
        btn_o5.set_color(0.3, 0.3, 0.35)
        btn_o5.bind(on_press=lambda x: self.select_package('odds_5', btn_o5))
        self.package_buttons.append(btn_o5)
        btn_o10 = RoundedButton(text='Odds 10')
        btn_o10.set_color(0.3, 0.3, 0.35)
        btn_o10.bind(on_press=lambda x: self.select_package('odds_10', btn_o10))
        self.package_buttons.append(btn_o10)
        btn_alf = RoundedButton(text='Alf')
        btn_alf.set_color(0.3, 0.3, 0.35)
        btn_alf.bind(on_press=lambda x: self.select_package('alf', btn_alf))
        self.package_buttons.append(btn_alf)
        pkg_btns.add_widget(btn_o2)
        pkg_btns.add_widget(btn_o5)
        pkg_btns.add_widget(btn_o10)
        pkg_btns.add_widget(btn_alf)
        self.code_input = TextInput(multiline=False, hint_text='Code (e.g. VIP2024XYZ)', size_hint_y=None, height=dp(45), font_size='13sp', background_color=(0.2, 0.2, 0.25, 1), foreground_color=(1, 1, 1, 1), padding=[dp(12), dp(12)])
        form_box.add_widget(pkg_btns)
        form_box.add_widget(self.code_input)
        form_card.add_widget(form_box)
        self.code_status = Label(text='', size_hint_y=None, height=dp(35), font_size='13sp', color=(0.2, 0.8, 0.5, 1))
        btn_add_code = RoundedButton(text='Ongeza Code', size_hint_y=None, height=dp(50))
        btn_add_code.set_color(0.8, 0.5, 0)
        btn_add_code.bind(on_press=self.add_code)
        codes_title = Label(text='Codes Zilizopo:', size_hint_y=None, height=dp(35), font_size='15sp', bold=True, color=(1, 1, 1, 1))
        self.codes_list_card = Card(height=dp(200))
        codes_scroll = ScrollView()
        self.codes_list = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None, padding=dp(10))
        self.codes_list.bind(minimum_height=self.codes_list.setter('height'))
        codes_scroll.add_widget(self.codes_list)
        self.codes_list_card.add_widget(codes_scroll)
        section_layout.add_widget(section_title)
        section_layout.add_widget(form_card)
        section_layout.add_widget(self.code_status)
        section_layout.add_widget(btn_add_code)
        section_layout.add_widget(codes_title)
        section_layout.add_widget(self.codes_list_card)
        self.refresh_codes_list()
        return section_layout
    
    def select_package(self, package, selected_button):
        self.selected_package = package
        for btn in self.package_buttons:
            if btn == selected_button:
                btn.set_color(0.8, 0.5, 0)
            else:
                btn.set_color(0.3, 0.3, 0.35)
    
    def add_code(self, instance):
        code = self.code_input.text.strip()
        if not code:
            self.code_status.text = 'Weka code!'
            self.code_status.color = (1, 0.3, 0.3, 1)
            return
        if self.selected_package not in data_manager.subscription_codes:
            data_manager.subscription_codes[self.selected_package] = []
        data_manager.subscription_codes[self.selected_package].append(code)
        data_manager.save_data()
        self.code_status.text = f'Code imeongezwa!'
        self.code_status.color = (0.2, 0.8, 0.5, 1)
        self.code_input.text = ''
        self.refresh_codes_list()
    
    def refresh_codes_list(self):
        self.codes_list.clear_widgets()
        has_codes = False
        for package, codes in data_manager.subscription_codes.items():
            if codes:
                has_codes = True
                pkg_label = Label(text=f'[b]{package.upper()}:[/b]', markup=True, size_hint_y=None, height=dp(30), color=(0.9, 0.7, 0.2, 1), halign='left')
                pkg_label.bind(size=pkg_label.setter('text_size'))
                self.codes_list.add_widget(pkg_label)
                for code in codes:
                    code_label = Label(text=f'  - {code}', size_hint_y=None, height=dp(25), color=(0.7, 0.7, 0.7, 1), halign='left', font_size='12sp')
                    code_label.bind(size=code_label.setter('text_size'))
                    self.codes_list.add_widget(code_label)
        if not has_codes:
            no_codes = Label(text='Hakuna codes bado', size_hint_y=None, height=dp(40), color=(0.5, 0.5, 0.5, 1))
            self.codes_list.add_widget(no_codes)
    
    def create_users_section(self):
        section_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        section_layout.bind(minimum_height=section_layout.setter('height'))
        section_title = Label(text='Registered Users', size_hint_y=None, height=dp(40), font_size='18sp', bold=True, color=(1, 1, 1, 1))
        self.users_container = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        self.users_container.bind(minimum_height=self.users_container.setter('height'))
        section_layout.add_widget(section_title)
        section_layout.add_widget(self.users_container)
        self.refresh_users_list()
        return section_layout
    
    def refresh_users_list(self):
        self.users_container.clear_widgets()
        has_users = False
        for username, user_data in data_manager.users.items():
            if username == 'Micmac':
                continue
            has_users = True
            user_card = Card(height=dp(100))
            user_box = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(10))
            name_label = Label(text=f'User: {username}', size_hint_y=0.4, color=(1, 1, 1, 1), bold=True, font_size='15sp', halign='left')
            name_label.bind(size=name_label.setter('text_size'))
            subs = user_data['subscriptions']
            if subs:
                subs_text = ', '.join([s['package'].upper() for s in subs])
                subs_label = Label(text=f'Subs: {subs_text}', size_hint_y=0.35, color=(0.2, 0.8, 0.5, 1), font_size='12sp', halign='left')
            else:
                subs_label = Label(text='Hakuna subscription', size_hint_y=0.35, color=(0.5, 0.5, 0.5, 1), font_size='12sp', halign='left')
            subs_label.bind(size=subs_label.setter('text_size'))
            if subs:
                date_text = f"Date: {subs[-1]['date']}"
            else:
                date_text = 'N/A'
            date_label = Label(text=date_text, size_hint_y=0.25, color=(0.6, 0.6, 0.6, 1), font_size='11sp', halign='left')
            date_label.bind(size=date_label.setter('text_size'))
            user_box.add_widget(name_label)
            user_box.add_widget(subs_label)
            user_box.add_widget(date_label)
            user_card.add_widget(user_box)
            self.users_container.add_widget(user_card)
        if not has_users:
            no_users_card = Card(height=dp(100))
            no_users = Label(text='Hakuna users bado', color=(0.5, 0.5, 0.5, 1))
            no_users_card.add_widget(no_users)
            self.users_container.add_widget(no_users_card)
    
    def logout(self, instance):
        self.manager.current = 'home'

class MICMACBettingApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SubscriptionScreen(name='subscription'))
        sm.add_widget(CodeEntryScreen(name='code_entry'))
        sm.add_widget(VIPTipsScreen(name='vip_tips'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm

if __name__ == '__main__':
    MICMACBettingApp().run()