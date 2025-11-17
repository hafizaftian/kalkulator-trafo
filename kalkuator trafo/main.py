
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout

class TrafoCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        grid = GridLayout(cols=2, spacing=8, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        self.spinner_mva = Spinner(text='20', values=['10','20','30','60'], size_hint_y=None, height=40)
        self.vp = TextInput(text='150', multiline=False)
        self.vs = TextInput(text='20', multiline=False)
        self.isec = TextInput(text='1000', multiline=False)
        self.cosphi = TextInput(text='0.85', multiline=False)
        self.eff = TextInput(text='0.98', multiline=False)
        self.thdi = TextInput(text='3', multiline=False)

        items = [
            ("Kapasitas Trafo (MVA)", self.spinner_mva),
            ("Tegangan Primer (kV)", self.vp),
            ("Tegangan Sekunder (kV)", self.vs),
            ("Arus Sekunder (A)", self.isec),
            ("Faktor Daya (cos phi)", self.cosphi),
            ("Efisiensi Trafo", self.eff),
            ("THDi (%)", self.thdi),
        ]

        for name, widget in items:
            grid.add_widget(Label(text=name))
            grid.add_widget(widget)

        self.add_widget(grid)

        btn = Button(text="Hitung", size_hint_y=None, height=50)
        btn.bind(on_press=self.calculate)
        self.add_widget(btn)

        self.out_ip = Label(text="Arus Primer: -")
        self.out_ipmax = Label(text="Arus Primer Maksimum: -")
        self.out_status = Label(text="Status: -")

        self.add_widget(self.out_ip)
        self.add_widget(self.out_ipmax)
        self.add_widget(self.out_status)

    def calculate(self, instance):
        MVA = float(self.spinner_mva.text)
        VP = float(self.vp.text) * 1000
        VS = float(self.vs.text) * 1000
        Isec = float(self.isec.text)
        cosphi = float(self.cosphi.text)
        eff = float(self.eff.text)
        thdi = float(self.thdi.text) / 100

        Iprim = Isec * (VS / VP) * (cosphi * eff)
        Iprim_final = Iprim * (1 / ((1 + thdi**2)**0.5))
        Iprim_max = (MVA * 1_000_000) / (1.732 * VP)

        if Iprim_final >= Iprim_max:
            status = "[BEBAN PRIMER 100%] — OVERLOAD"
        elif Iprim_final >= 0.85 * Iprim_max:
            status = "Mendekati batas — pantau beban"
        else:
            status = "Aman"

        self.out_ip.text = f"Arus Primer: {Iprim_final:.2f} A"
        self.out_ipmax.text = f"Arus Primer Maksimum: {Iprim_max:.2f} A"
        self.out_status.text = f"Status: {status}"

class TrafoApp(App):
    def build(self):
        return TrafoCalculator()

if __name__ == "__main__":
    TrafoApp().run()
