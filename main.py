# main.py
import json, os, uuid, hashlib, datetime, re
from kivy.metrics import dp
from kivy.utils import platform
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDCheckbox

# =========================
# CONFIG
# =========================
ROXO = " #8a2be2"
LILAS = "#b39ddb"
AZUL = "#81d4fa"

USERS_FILE = "data/usuarios.json"
CRISES_FILE = "data/crises.json"
DIARIO_FILE = "data/diario.json"
MEDS_FILE = "data/medicamentos.json"
CONSULTAS_FILE = "data/consultas.json"
ATIVIDADES_FILE = "data/atividades.json"
ALIMENTACAO_FILE = "data/alimentacao.json"
REGISTROS_FILE = "data/registros.json"

SESSAO = {}

# =========================
# UTIL
# =========================
def ensure_data_dir():
    os.makedirs("data", exist_ok=True)

def load_json(path):
    ensure_data_dir()
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    ensure_data_dir()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def hash_senha(senha, salt=None):
    if not salt:
        salt = uuid.uuid4().hex
    return hashlib.sha256((senha + salt).encode()).hexdigest(), salt

def alerta_palavras(texto):
    palavras = [
        "suicidio","morte","morrer","matar","tirar a vida","acabar com tudo",
        "desistir","sem sentido","inutil","foda-se","não aguento","cortar",
        "ferir","machucar","ódio","raiva","desespero","sofrimento","fim",
        "vontade de morrer","não quero viver","acabou","nada importa",
        "perder a vida","sofrer","desamparo","sem saída","angustia","desolado",
        "desesperado","sem esperança"
    ]
    texto = texto.lower()
    return any(p in texto for p in palavras)

# =========================
# APP
# =========================
class SynapseApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Light"
        self.load_all()

        return Builder.load_file("synapse.kv")

    def load_all(self):
        self.usuarios = load_json(USERS_FILE)
        self.crises = load_json(CRISES_FILE)
        self.diario = load_json(DIARIO_FILE)
        self.meds = load_json(MEDS_FILE)
        self.consultas = load_json(CONSULTAS_FILE)
        self.atividades = load_json(ATIVIDADES_FILE)
        self.alimentacao = load_json(ALIMENTACAO_FILE)
        self.registros = load_json(REGISTROS_FILE)

    def salvar_todos(self):
        save_json(USERS_FILE, self.usuarios)
        save_json(CRISES_FILE, self.crises)
        save_json(DIARIO_FILE, self.diario)
        save_json(MEDS_FILE, self.meds)
        save_json(CONSULTAS_FILE, self.consultas)
        save_json(ATIVIDADES_FILE, self.atividades)
        save_json(ALIMENTACAO_FILE, self.alimentacao)
        save_json(REGISTROS_FILE, self.registros)

    # -------------------
    # LOGIN
    # -------------------
    def login(self):
        u = self.root.ids.login_user.text.strip()
        p = self.root.ids.login_pwd.text.strip()

        if u == "adm" and p == "adm":
            SESSAO["user"] = "adm"
            self.root.ids.screen_manager.current = "admin"
            return

        if u not in self.usuarios:
            self.root.ids.login_msg.text = "Usuário não encontrado"
            return

        h, salt = self.usuarios[u]["senha"], self.usuarios[u]["salt"]
        if hash_senha(p, salt)[0] != h:
            self.root.ids.login_msg.text = "Senha incorreta"
            return

        SESSAO["user"] = u
        self.root.ids.login_msg.text = ""
        self.root.ids.screen_manager.current = "principal"
        self.atualizar_menu()

    # -------------------
    # CADASTRO
    # -------------------
    def cadastrar(self):
        nome = self.root.ids.cad_nome.text.strip()
        idade = self.root.ids.cad_idade.text.strip()
        sexo = self.root.ids.cad_sexo.text.strip()
        motivo = self.root.ids.cad_motivo.text.strip()

        if not nome or not idade or not motivo:
            self.root.ids.cad_msg.text = "Preencha todos os campos obrigatórios"
            return

        if nome in self.usuarios:
            self.root.ids.cad_msg.text = "Usuário já existe"
            return

        h, salt = hash_senha(self.root.ids.cad_pwd.text)
        self.usuarios[nome] = {
            "nome": nome,
            "idade": idade,
            "sexo": sexo,
            "senha": h,
            "salt": salt,
            "motivo": motivo
        }
        self.salvar_todos()
        self.root.ids.screen_manager.current = "login"
        self.root.ids.cad_msg.text = ""

    # -------------------
    # MENU PRINCIPAL
    # -------------------
    def atualizar_menu(self):
        user = SESSAO.get("user")
        if not user:
            return
        motivo = self.usuarios[user]["motivo"]

        # Se for só psicologico, remove registrar crises
        self.root.ids.btn_crises.opacity = 1 if motivo in ["Epilepsia", "Ambos"] else 0
        self.root.ids.btn_crises.disabled = False if motivo in ["Epilepsia", "Ambos"] else True

    # -------------------
    # CRISES
    # -------------------
    def abrir_crises(self):
        self.root.ids.screen_manager.current = "crises"
        self.root.ids.crises_box.clear_widgets()

        CRISES = {
            "Crise Focal": [
                ("Sensorial", "Formigamento, cheiros irreais"),
                ("Motora", "Movimentos involuntários"),
                ("Autonômica", "Náusea, sudorese"),
                ("Psíquica", "Medo, déjà vu, jamais vu")
            ],
            "Crise Focal com Alteração da Consciência": [
                ("Automatismos", "Movimentos repetitivos"),
                ("Confusão", "Desorientação")
            ],
            "Crise Generalizada": [
                ("Tônico-clônica", "Rigidez e abalos"),
                ("Ausência", "Desligamento breve"),
                ("Mioclônica", "Contrações rápidas"),
                ("Atônica", "Perda de força")
            ],
            "Crise Gelástica": [
                ("Riso involuntário", "Riso sem motivo")
            ],
            "Crise Reflexa": [
                ("Fotossensível", "Luz"),
                ("Auditiva", "Som")
            ]
        }

        for crise, subs in CRISES.items():
            btn = MDRaisedButton(text=crise, md_bg_color=(0.72,0.65,1,1))
            btn.bind(on_release=lambda inst, c=crise, s=subs: self.abrir_subcrises(c, s))
            self.root.ids.crises_box.add_widget(btn)

    def abrir_subcrises(self, crise, subs):
        self.root.ids.screen_manager.current = "subcrises"
        self.root.ids.subcrises_title.text = crise
        self.root.ids.subcrises_box.clear_widgets()

        for nome, desc in subs:
            btn = MDRaisedButton(text=nome, md_bg_color=(0.81,0.88,1,1))
            btn.bind(on_release=lambda inst, n=nome: self.registrar_crise(crise, n))
            self.root.ids.subcrises_box.add_widget(btn)

    def registrar_crise(self, crise, sub):
        user = SESSAO.get("user")
        if not user: return

        registro = {
            "data": str(datetime.date.today()),
            "hora": str(datetime.datetime.now().time())[:8],
            "crise": crise,
            "subcrise": sub
        }
        self.registros.setdefault(user, {}).setdefault("crises", []).append(registro)
        self.salvar_todos()
        Snackbar(text="Crise registrada!").open()

    def ver_crises_registradas(self):
        user = SESSAO.get("user")
        if not user: return
        self.root.ids.screen_manager.current = "crises_reg"
        self.root.ids.crises_reg_box.clear_widgets()

        registros = self.registros.get(user, {}).get("crises", [])
        for r in registros:
            self.root.ids.crises_reg_box.add_widget(
                OneLineListItem(text=f"{r['data']} {r['hora']} - {r['crise']} ({r['subcrise']})")
            )

    # -------------------
    # DIARIO
    # -------------------
    def salvar_diario(self):
        user = SESSAO.get("user")
        if not user: return

        texto = self.root.ids.diario_text.text.strip()
        humor = self.root.ids.diario_humor.text.strip()

        if humor not in ["Bom","Neutro","Ruim"]:
            Snackbar(text="Marque o humor: Bom, Neutro ou Ruim").open()
            return

        if alerta_palavras(texto):
            self.dialog_alerta()

        registro = {
            "data": str(datetime.date.today()),
            "humor": humor,
            "texto": texto
        }
        self.registros.setdefault(user, {}).setdefault("diario", []).append(registro)
        self.salvar_todos()
        Snackbar(text="Diário salvo!").open()

    def dialog_alerta(self):
        self.dialog = MDDialog(
            title="Olá, você não parece tão bem hoje...",
            text="Você merece cuidado. Se estiver em risco, ligue para o número de emergência.\n\n📞 188 (CVV Brasil)\n📞 192 / 193",
            buttons=[
                MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()

    # -------------------
    # MEDICAMENTOS
    # -------------------
    def abrir_meds(self):
        self.root.ids.screen_manager.current = "meds"
        self.root.ids.meds_box.clear_widgets()
        user = SESSAO.get("user")
        registros = self.registros.get(user, {}).get("medicamentos", [])
        for m in registros:
            self.root.ids.meds_box.add_widget(
                OneLineListItem(text=f"{m['nome']} - {m['mg']}mg - {m['freq']}x/dia - compra: {m['compra']}")
            )

    def registrar_med(self):
        user = SESSAO.get("user")
        if not user: return

        nome = self.root.ids.med_nome.text.strip()
        mg = self.root.ids.med_mg.text.strip()
        freq = self.root.ids.med_freq.text.strip()
        compra = self.root.ids.med_compra.text.strip()

        registro = {"nome": nome, "mg": mg, "freq": freq, "compra": compra}
        self.registros.setdefault(user, {}).setdefault("medicamentos", []).append(registro)
        self.salvar_todos()
        Snackbar(text="Medicamento registrado!").open()

    # -------------------
    # CONSULTAS
    # -------------------
    def registrar_consulta(self):
        user = SESSAO.get("user")
        if not user: return

        nome = self.root.ids.cons_nome.text.strip()
        esp = self.root.ids.cons_esp.text.strip()
        data = self.root.ids.cons_data.text.strip()
        hora = self.root.ids.cons_hora.text.strip()

        registro = {"nome": nome, "esp": esp, "data": data, "hora": hora}
        self.registros.setdefault(user, {}).setdefault("consultas", []).append(registro)
        self.salvar_todos()
        Snackbar(text="Consulta registrada!").open()

    # -------------------
    # ATIVIDADES
    # -------------------
    def registrar_atividade(self):
        user = SESSAO.get("user")
        if not user: return
        nome = self.root.ids.ativ_nome.text.strip()
        tempo = self.root.ids.ativ_tempo.text.strip()
        intensidade = self.root.ids.ativ_int.text.strip()
        registro = {"nome": nome, "tempo": tempo, "intensidade": intensidade}
        self.registros.setdefault(user, {}).setdefault("atividades", []).append(registro)
        self.salvar_todos()
        Snackbar(text="Atividade registrada!").open()

    # -------------------
    # ALIMENTAÇÃO
    # -------------------
    def abrir_alimentacao(self):
        self.root.ids.screen_manager.current = "alimentacao"
        self.root.ids.alim_box.clear_widgets()

        TIPOS = {
            "Frutas": ["Maçã", "Banana", "Laranja", "Abacate", "Uva", "Melancia", "Pera", "Manga", "Kiwi", "Morango"],
            "Legumes": ["Cenoura", "Batata", "Abóbora", "Brócolis", "Couve", "Espinafre", "Pepino", "Tomate", "Beterraba", "Rabanete"],
            "Proteínas": ["Frango", "Carne", "Peixe", "Ovo", "Tofu", "Feijão", "Grão-de-bico", "Lentilha", "Queijo", "Iogurte"],
            "Carboidratos": ["Arroz", "Macarrão", "Pão", "Batata", "Aveia", "Quinoa", "Milho", "Cuscuz", "Mandioca", "Pão integral"],
            "Laticínios": ["Leite", "Queijo", "Iogurte", "Manteiga", "Requeijão", "Creme de leite", "Kefir", "Ricota", "Coalhada", "Sorvete"],
            "Gorduras": ["Azeite", "Abacate", "Castanhas", "Manteiga", "Óleo de coco", "Margarina", "Sementes", "Nozes", "Amendoim", "Avelã"],
            "Doces": ["Chocolate", "Bolo", "Sorvete", "Balas", "Pudim", "Cookie", "Doce de leite", "Brigadeiro", "Guloseimas", "Churros"],
            "Bebidas": ["Água", "Suco", "Refrigerante", "Café", "Chá", "Leite", "Smoothie", "Vitamina", "Energético", "Água de coco"],
            "Lanches": ["Sanduíche", "Pizza", "Salgadinho", "Pipoca", "Torrada", "Wrap", "Hambúrguer", "Hot dog", "Sushi", "Tapioca"],
            "Sopas": ["Sopa de legumes", "Caldo verde", "Sopa de frango", "Sopa de carne", "Canja", "Creme de milho", "Sopa de abóbora", "Sopa de lentilha", "Sopa de feijão", "Sopa de batata"]
        }

        for tipo, subs in TIPOS.items():
            btn = MDRaisedButton(text=tipo, md_bg_color=(0.72,0.65,1,1))
            btn.bind(on_release=lambda inst, t=tipo, s=subs: self.abrir_sub_alim(t, s))
            self.root.ids.alim_box.add_widget(btn)

    def abrir_sub_alim(self, tipo, subs):
        self.root.ids.screen_manager.current = "sub_alim"
        self.root.ids.sub_alim_title.text = tipo
        self.root.ids.sub_alim_box.clear_widgets()

        for s in subs:
            btn = MDRaisedButton(text=s, md_bg_color=(0.81,0.88,1,1))
            btn.bind(on_release=lambda inst, sub=s: self.registrar_alim(tipo, sub))
            self.root.ids.sub_alim_box.add_widget(btn)

    def registrar_alim(self, tipo, sub):
        user = SESSAO.get("user")
        registro = {"data": str(datetime.date.today()), "tipo": tipo, "sub": sub}
        self.registros.setdefault(user, {}).setdefault("alimentacao", []).append(registro)
        self.salvar_todos()
        Snackbar(text="Alimentação registrada!").open()

    # -------------------
    # ANALISE
    # -------------------
    def abrir_analise(self, dias=7):
        user = SESSAO.get("user")
        self.root.ids.screen_manager.current = "analise"
        self.root.ids.analise_box.clear_widgets()

        data_fim = datetime.date.today()
        data_ini = data_fim - datetime.timedelta(days=dias)

        # mostra resumo simples
        registros = self.registros.get(user, {})
        diario = registros.get("diario", [])
        crises = registros.get("crises", [])
        meds = registros.get("medicamentos", [])

        resumo = f"Resumo últimos {dias} dias:\n"
        resumo += f"Diário: {len([d for d in diario if data_ini <= datetime.date.fromisoformat(d['data']) <= data_fim])}\n"
        resumo += f"Crises: {len([c for c in crises if data_ini <= datetime.date.fromisoformat(c['data']) <= data_fim])}\n"
        resumo += f"Medicamentos: {len(meds)}\n"

        self.root.ids.analise_box.add_widget(MDLabel(text=resumo, theme_text_color="Primary"))

