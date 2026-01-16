from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.clock import Clock
from urllib.parse import urlparse, parse_qs
import requests

def get_android_launch_url():
    try:
        from jnius import autoclass

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity

        intent = activity.getIntent()
        action = intent.getAction()

        if action == "android.intent.action.VIEW":
            uri = intent.getData()
            if uri:
                return uri.toString()
    except Exception as e:
        print("Erreur Intent:", e)

    return None


def send_params(id_, key):
    url = f"https://www.planete-sciences.org/espace/spock/api.html?object=stabtraj&id={id_}&key={key}"

    DF = {
        "object": "stabtraj",
        "id": id_,
        "key": key,
        "data": {
            "Long_ogive": 120
        }
    }

    try:
        r = requests.put(url, json=DF)
        print("Envoi terminé :", r.status_code)
    except Exception as e:
        print("Erreur request :", e)


def open_website(url):
    try:
        from jnius import autoclass, cast
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')

        intent = Intent(Intent.ACTION_VIEW)
        intent.setData(Uri.parse(url))

        current_activity = PythonActivity.mActivity
        current_activity.startActivity(intent)
    except Exception as e:
        print("Erreur ouverture site :", e)

class MyApp(App):

    def build(self):
        # Layout vertical
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Label
        self.label = Label(text="---- Bienvenue ----\n(En attente de lien...)")
        self.layout.add_widget(self.label)

        # Bouton (caché au début)
        self.button = Button(text="Envoyer à SPOCK", size_hint=(1, 0.3))
        self.button.disabled = True
        self.button.opacity = 0
        self.button.bind(on_press=self.on_button_press)

        self.layout.add_widget(self.button)

         # Nouveau bouton
        self.button_site = Button(text="Ouvrir le site", size_hint=(1, 0.3))
        self.button_site.disabled = True
        self.button_site.opacity = 0
        self.button_site.bind(on_press=self.on_site_press)

        self.layout.add_widget(self.button_site)

        return self.layout


    def on_start(self):
        if platform == "android":
            Clock.schedule_once(self.read_link, 0.6)


    def read_link(self, dt):
        link = get_android_launch_url()

        if link:
            parsed = urlparse(link)

            params = parse_qs(parsed.query)
            self.data = params.get("data", [""])[0]
            self.id_  = params.get("id", [""])[0]
            self.key  = params.get("key", [""])[0]
            self.code  = params.get("code", [""])[0]

            call = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

            self.label.text = (
                f"---- Bienvenue ----\n"
                f"Appel par : {call}\n"
                f"id : {self.id_}\n"
                f"key : {self.key}"
            )

            # Activer bouton
            self.button.disabled = False
            self.button.opacity = 1
            # Activer bouton
            self.button_site.disabled = False
            self.button_site.opacity = 1

        else:
            self.label.text = "---- Bienvenue ----\nAucun lien reçu"


    def on_button_press(self, instance):
        if hasattr(self, "id_") and hasattr(self, "key"):
            send_params(self.id_, self.key)
            self.label.text += "\n\nParamètres envoyés ! (ogive = 120)"
        else:
            self.label.text += "\n\nImpossible : pas de paramètres."

    def on_site_press(self, instance):
        open_website(f"https://www.planete-sciences.org/espace/spock/stabtraj.html?code={self.code}")

if __name__ == "__main__":
    MyApp().run()
