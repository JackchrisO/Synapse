import json
import os
import hashlib
import uuid

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window
from kivy.utils import platform

# ================= CONFIG =================
Window.size = (360, 640)
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
    path = caminho_app(USERS_FILE)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
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

# ================= BOTÃO PREMIUM =================
class BotaoPremium(ButtonBehavior, Widget):
    def __init__(self, texto="", **kw):
        super().__init__(**kw)
        self.size_hint = (0.9, None)
        self.height = 48
        self.radius = 22

        with self.canvas.before:
            Color(0, 0, 0, 0.15)
            self.sombra = RoundedRectangle(radius=[self.radius])
            self.bg_color = Color(*ROXO_CLARO)
            self.bg = RoundedRectangle(radius=[self.radius])
            Color(1, 1, 1, 0.9)
            self.borda = Line(width=1.2)

        self.label = Label(text=texto, color=PRETO, bold=True,
                           font_size=18, halign="center", valign="middle")
        self.label.bind(size=lambda s, *_: setattr(s, "text_size", (s.width, s.height)))
        self.add_widget(self.label)

        self.bind(pos=self.update, size=self.update)

    def update(self, *args):
        self.sombra.pos = (self.x + 2, self.y - 2)
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

# ================= INPUT PREMIUM =================
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
            Color(1, 1, 1, 0.9)
            self.borda = Line(width=1.2)

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

# ================= RADIO OPÇÃO =================
class RadioOpcao(ButtonBehavior, Widget):
    def __init__(self, texto, grupo, **kw):
        super().__init__(**kw)
        self.texto = texto
        self.grupo = grupo
        self.ativo = False
        self.size_hint = (0.9, None)
        self.height = 44
        self.radius = 22

        with self.canvas.before:
            self.bg_color = Color(*CINZA)
            self.bg = RoundedRectangle(radius=[self.radius])

        self.label = Label(text=texto, color=PRETO, font_size=16,
                           halign="center", valign="middle")
        self.label.bind(size=lambda s, *_: setattr(s, "text_size", (s.width, s.height)))
        self.add_widget(self.label)

        self.bind(pos=self.update, size=self.update)

    def update(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.label.pos = self.pos
        self.label.size = self.size

    def on_press(self):
        for o in self.grupo:
            o.bg_color.rgba = CINZA
            o.ativo = False
        self.bg_color.rgba = ROXO_CLARO
        self.ativo = True

# ================= TELAS =================
class Login(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        box = BoxLayout(orientation="vertical", padding=20, spacing=15)
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

        box.add_widget(Label(
            text="Não deixe o sistema nervoso",
            font_size=14,
            color=(0, 0, 0, 0.5),
            halign="center"
        ))

    def login(self, *_):
        usuarios = carregar_usuarios()
        u = self.user.input.text.strip()
        p = self.pwd.input.text

        if u == "adm" and p == "adm":
            SESSAO["user"] = u
            self.manager.current = "principal"
            return

        if u not in usuarios:
            self.msg.text = "Usuário não encontrado"
            return

        h, salt = usuarios[u]["senha"], usuarios[u]["salt"]
        if hash_senha(p, salt)[0] != h:
            self.msg.text = "Senha incorreta"
            return

        SESSAO["user"] = u
        self.manager.current = "principal"

class Cadastro(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        box = BoxLayout(orientation="vertical", padding=20, spacing=15)
        self.add_widget(box)

        box.add_widget(label_central("CADASTRO", 28))
        self.user = InputPremium("Nome")
        self.nascimento = InputPremium("Nascimento (DD/MM/AAAA)")
        self.sexo = InputPremium("Sexo (Opcional)")
        self.pwd = InputPremium("Senha", password=True)
        self.conf = InputPremium("Confirmar senha", password=True)
        self.msg = label_central("", 14, (0.8, 0, 0, 1))

        box.add_widget(self.user)
        box.add_widget(self.nascimento)
        box.add_widget(self.sexo)
        box.add_widget(self.pwd)
        box.add_widget(self.conf)
        box.add_widget(label_central("Motivo do uso do app:", 16))

        self.opcoes = []
        for t in ["Epilepsia", "Cuidado psicológico", "Ambos"]:
            op = RadioOpcao(t, self.opcoes)
            self.opcoes.append(op)
            box.add_widget(op)

        box.add_widget(self.msg)

        salvar = BotaoPremium("Salvar")
        salvar.bind(on_release=self.salvar)
        box.add_widget(salvar)

        voltar = BotaoPremium("Voltar")
        voltar.bind(on_release=lambda *_: setattr(self.manager, "current", "login"))
        box.add_widget(voltar)

        box.add_widget(Label(
            text="Não deixe o sistema nervoso",
            font_size=14,
            color=(0, 0, 0, 0.5),
            halign="center"
        ))

    def salvar(self, *_):
        if self.pwd.input.text != self.conf.input.text:
            self.msg.text = "As senhas não coincidem"
            return

        motivo = next((o.texto for o in self.opcoes if o.ativo), None)
        if not motivo:
            self.msg.text = "Selecione um motivo"
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
        usuarios[u] = {
            "nome": u,
            "nascimento": self.nascimento.input.text,
            "sexo": self.sexo.input.text,
            "senha": h,
            "salt": salt,
            "motivo": motivo
        }

        salvar_usuarios(usuarios)
        self.manager.current = "login"

class Principal(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        scroll = ScrollView(size_hint=(1, 1))
        box = BoxLayout(orientation="vertical", padding=20, spacing=15, size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))
        scroll.add_widget(box)
        self.add_widget(scroll)

        box.add_widget(label_central("MENU PRINCIPAL", 28))
        box.add_widget(Label(
            text="Não deixe o sistema nervoso",
            font_size=14,
            color=(0, 0, 0, 0.5),
            halign="center"
        ))

        botoes = {
            "Registrar Crises": "registrar_crise",
            "Diário": "principal_diario",
            "Alimentação": "principal_alimentos",
            "Atividades Físicas": "atividades",
            "Consultas": "consultas",
            "Medicamentos": "principal_med",
            "Análise": "analise"
        }

        for txt, tela in botoes.items():
            btn = BotaoPremium(txt)
            btn.bind(on_release=lambda *_ , t=tela: setattr(self.manager, "current", t))
            box.add_widget(btn)
            box.add_widget(Widget(size_hint_y=None, height=8))
            class TelaSimples(Screen):
    def __init__(self, titulo="", **kw):
        super().__init__(**kw)
        box = BoxLayout(orientation="vertical", padding=20)
        box.add_widget(label_central(titulo, 26))
        self.add_widget(box)


# ================= APP =================
class AppMain(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Login(name="login"))
        sm.add_widget(Cadastro(name="cadastro"))
        sm.add_widget(Principal(name="principal"))

        sm.add_widget(TelaSimples("Registrar Crises", name="registrar_crise"))
        sm.add_widget(TelaSimples("Diário", name="principal_diario"))
        sm.add_widget(TelaSimples("Alimentação", name="principal_alimentos"))
        sm.add_widget(TelaSimples("Atividades", name="atividades"))
        sm.add_widget(TelaSimples("Consultas", name="consultas"))
        sm.add_widget(TelaSimples("Medicamentos", name="principal_med"))
        sm.add_widget(TelaSimples("Análise", name="analise"))

        return sm


if __name__ == "__main__":
    AppMain().run()

