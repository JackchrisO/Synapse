import json, os, hashlib, uuid
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

# ================= CONFIG =================
Window.clearcolor = (0.96, 0.96, 1, 1)
USERS_FILE = "usuarios.json"
SESSAO = {}

# ================= CORES =================
ROXO = (0.55, 0.45, 0.95, 1)
ROXO_CLARO = (0.72, 0.65, 1, 1)
PRETO = (0.12, 0.12, 0.18, 1)
CINZA = (0.85, 0.85, 0.88, 1)

# ================= ANDROID PATH =================
def caminho_app(arquivo):
    if platform == "android":
        from android.storage import app_storage_path
        return os.path.join(app_storage_path(), arquivo)
    return arquivo

# ================= UTIL =================
def carregar_usuarios():
    try:
        path = caminho_app(USERS_FILE)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def salvar_usuarios(dados):
    path = caminho_app(USERS_FILE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def hash_senha(senha, salt=None):
    if not salt:
        salt = uuid.uuid4().hex
    return hashlib.sha256((senha + salt).encode()).hexdigest(), salt

# ================= LABEL CENTRAL =================
def label_central(texto, tamanho=22, cor=PRETO):
    lbl = Label(text=texto, font_size=tamanho, color=cor,
                halign="center", valign="middle")
    lbl.bind(size=lambda s, *_: setattr(s, "text_size", (s.width, s.height)))
    return lbl

# ================= BOTÃO =================
class BotaoPremium(ButtonBehavior, Widget):
    def __init__(self, texto="", **kw):
        super().__init__(**kw)
        self.size_hint = (0.9, None)
        self.height = 56
        self.radius = 28

        with self.canvas.before:
            Color(0, 0, 0, 0.2)
            self.sombra = RoundedRectangle(radius=[self.radius])
            self.bg_color = Color(*ROXO)
            self.bg = RoundedRectangle(radius=[self.radius])
            Color(1, 1, 1, 0.9)
            self.borda = Line(width=1.2)

        self.label = Label(text=texto, color=PRETO, bold=True,
                           font_size=18, halign="center", valign="middle")
        self.label.bind(size=lambda s, *_: setattr(s, "text_size", (s.width, s.height)))
        self.add_widget(self.label)
        self.bind(pos=self.update, size=self.update)

    def update(self, *args):
        self.sombra.pos = (self.x + 3, self.y - 4)
        self.sombra.size = self.size
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.borda.rounded_rectangle = (self.x, self.y, self.width, self.height, self.radius)
        self.label.pos = self.pos
        self.label.size = self.size

    def on_press(self):
        self.bg_color.rgba = ROXO_CLARO

    def on_release(self):
        self.bg_color.rgba = ROXO

# ================= INPUT =================
class InputPremium(Widget):
    def __init__(self, hint="", password=False, **kw):
        super().__init__(**kw)
        self.size_hint = (0.9, None)
        self.height = 48

        with self.canvas.before:
            Color(0, 0, 0, 0.15)
            self.sombra = RoundedRectangle(radius=[14])
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(radius=[14])
            Color(0.7, 0.7, 0.75, 1)
            self.borda = Line(width=1)

        self.input = TextInput(
            hint_text=hint,
            password=password,
            multiline=False,
            background_color=(0, 0, 0, 0),
            foreground_color=PRETO,
            cursor_color=PRETO,
            padding=(12, 12)
        )

        self.add_widget(self.input)
        self.bind(pos=self.update, size=self.update)

    def update(self, *args):
        self.sombra.pos = (self.x + 2, self.y - 2)
        self.sombra.size = self.size
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.borda.rounded_rectangle = (self.x, self.y, self.width, self.height, 14)
        self.input.pos = self.pos
        self.input.size = self.size

# ================= TELAS =================
class Login(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        box = BoxLayout(orientation="vertical", padding=30, spacing=15)
        self.add_widget(box)

        box.add_widget(label_central("LOGIN", 32))
        self.user = InputPremium("Usuário")
        self.pwd = InputPremium("Senha", password=True)
        self.msg = label_central("", 14, (0.8, 0, 0, 1))

        box.add_widget(self.user)
        box.add_widget(self.pwd)
        box.add_widget(self.msg)

        entrar = BotaoPremium("Entrar")
        entrar.bind(on_release=self.login)
        box.add_widget(entrar)

        cad = BotaoPremium("Cadastrar")
        cad.bind(on_release=lambda *_: setattr(self.manager, "current", "cadastro"))
        box.add_widget(cad)

    def login(self, *_):
        usuarios = carregar_usuarios()
        u = self.user.input.text.strip()
        p = self.pwd.input.text

        if u == "adm" and p == "adm":
            self.manager.current = "principal"
            return

        if u not in usuarios:
            self.msg.text = "Usuário não encontrado"
            return

        h, salt = usuarios[u]["senha"], usuarios[u]["salt"]
        if hash_senha(p, salt)[0] != h:
            self.msg.text = "Senha incorreta"
            return

        self.manager.current = "principal"

class Cadastro(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        box = BoxLayout(orientation="vertical", padding=20, spacing=15)
        self.add_widget(box)

        box.add_widget(label_central("CADASTRO", 28))
        self.user = InputPremium("Nome")
        self.pwd = InputPremium("Senha", password=True)
        self.conf = InputPremium("Confirmar senha", password=True)
        self.msg = label_central("", 14, (0.8, 0, 0, 1))

        box.add_widget(self.user)
        box.add_widget(self.pwd)
        box.add_widget(self.conf)
        box.add_widget(self.msg)

        salvar = BotaoPremium("Salvar")
        salvar.bind(on_release=self.salvar)
        box.add_widget(salvar)

    def salvar(self, *_):
        if self.pwd.input.text != self.conf.input.text:
            self.msg.text = "As senhas não coincidem"
            return

        usuarios = carregar_usuarios()
        u = self.user.input.text.strip()

        if not u:
            self.msg.text = "Nome inválido"
            return

        if u in usuarios:
            self.msg.text = "Usuário já existe"
            return

        h, salt = hash_senha(self.pwd.input.text)
        usuarios[u] = {"senha": h, "salt": salt}
        salvar_usuarios(usuarios)
        self.manager.current = "login"

class Principal(Screen):
    pass

# ================= APP =================
class AppMain(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Login(name="login"))
        sm.add_widget(Cadastro(name="cadastro"))
        sm.add_widget(Principal(name="principal"))
        return sm
