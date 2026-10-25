import flet as ft
from flet import IconButton
from flet.controls import alignment

from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Handlers per la gestione dei pulsanti
    def pulsante_piu(e):
        currentVal = int(txt_costo.value)
        txt_costo.value = str(currentVal + 1)
        txt_costo.update()

    def pulsante_meno(e):
        currentVal = int(txt_costo.value)
        txt_costo.value = str(currentVal - 1)
        txt_costo.update()




    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    txt_tipo = ft.TextField(label="Tipo", expand = True)
    txt_marca = ft.TextField(label = "Marca", expand = True)
    txt_anno = ft.TextField(label = "Anno di acquisto", expand = True)
    txt_costo = ft.TextField(value = "0", expand = True, text_align = ft.TextAlign.CENTER)

    bott_piu = ft.IconButton(
        icon = ft.Icons.ADD,
        icon_color = "green",
        on_click = pulsante_piu
    )

    bott_meno = ft.IconButton(
        icon = ft.Icons.REMOVE,
        icon_color = "red",
        on_click = pulsante_meno
    )


    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def aggiunta_strumento(e):
        try:
            anno = int(txt_anno.value)
            costo = float(txt_costo.value)
        except ValueError:
            alert.show_alert("inserisci valori numerici validi per anno e/o prezzo")
            return

        try:
            s = deposito.aggiungi_strumento(txt_tipo.value, txt_marca.value, anno, costo)
            aggiorna_lista_strumenti()
        except Exception as error:
            alert.show_alert("Errore durante l'aggiunta")
            return


        txt_marca.value = ""
        txt_anno.value = ""
        txt_costo.value = "0"
        txt_tipo.value = ""

        page.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    bott_agg = ft.Button(content = "Aggiungi Strumento", on_click = aggiunta_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Text("Aggiungi Strumento", size=20),

        ft.Row(controls = [txt_tipo, txt_marca, txt_anno,bott_meno, txt_costo, bott_piu],
               alignment = ft.MainAxisAlignment.CENTER
               ),
        ft.Row(controls = [bott_agg],
               alignment = ft.MainAxisAlignment.CENTER
               ),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti
    )
    aggiorna_lista_strumenti()

ft.run(main)
