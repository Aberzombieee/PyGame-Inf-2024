import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
BREITE, HOEHE = 800, 600
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
GRAU = (169, 169, 169)
ROT = (255, 0, 0)
BLAU = (0, 0, 255)
GRUEN = (0, 255, 0)
GELB = (255, 255, 0)
LILA = (128, 0, 128)
FARBEN = [ROT, BLAU, GRUEN, GELB, LILA]
FARBEN_NAME = ['Red', 'Blue', 'Green', 'Yellow', 'Purple']
TITLE_TEXT = "PUSH"
MIN_SPIELER = 2
MAX_SPIELER = 6
grundwert_spieler = 2

# Deck erstellen
def erstelle_deck():
    deck = []
    # 18 Karten pro Farbe, 1-6 jeweils dreimal
    for farbe in FARBEN_NAME:
        for zahl in range(1, 7):
            for _ in range(3):
                deck.append((farbe, zahl))
    # 18 Roll-Karten
    for _ in range(18):
        deck.append(("Roll", None))
    # 12 Switch-Karten
    for _ in range(12):
        deck.append(("Switch", None))
    random.shuffle(deck)
    return deck

deck = erstelle_deck()

# Set up the display in windowed borderless fullscreen mode
fenster = pygame.display.set_mode((0, 0), pygame.NOFRAME | pygame.FULLSCREEN)
BREITE, HOEHE = fenster.get_size()
pygame.display.set_caption("PUSH")

# Load fonts
titel_schriftart = pygame.font.Font(None, 74)
knopf_schriftart = pygame.font.Font(None, 36)
kleine_knopf_schriftart = pygame.font.Font(None, 24)
karte_schriftart_gross = pygame.font.Font(None, 48)
karte_schriftart_klein = pygame.font.Font(None, 24)
karte_schriftart_titel = pygame.font.Font(None, 36)

# Define columns
columns = [[], [], []]
switch_column = []
handkarten = [[] for _ in range(MAX_SPIELER)]  # Handkarten für jeden Spieler

def zeichne_text(mittelpunkt_x, mittelpunkt_y, text, farbe, schriftart):
    text_flaeche = schriftart.render(text, True, farbe)
    text_rechteck = text_flaeche.get_rect(center=(mittelpunkt_x, mittelpunkt_y))
    fenster.blit(text_flaeche, text_rechteck)

def zeichne_knopf(text, mittelpunkt_x, mittelpunkt_y, breite, hoehe, schriftart=knopf_schriftart):
    knopf_rechteck = pygame.Rect(0, 0, breite, hoehe)
    knopf_rechteck.center = (mittelpunkt_x, mittelpunkt_y)
    pygame.draw.rect(fenster, SCHWARZ, knopf_rechteck)
    zeichne_text(mittelpunkt_x, mittelpunkt_y, text, WEISS, schriftart)
    return knopf_rechteck

def zeichne_karte(x, y, breite, hoehe, zahl, farbe, farbe_rgb):
    karte_rechteck = pygame.Rect(x, y, breite, hoehe)
    pygame.draw.rect(fenster, WEISS, karte_rechteck, 5, border_radius=10)
    pygame.draw.rect(fenster, farbe_rgb, karte_rechteck, border_radius=10)
    if zahl is not None:
        zeichne_text(x + breite // 2, y + hoehe // 2, str(zahl), WEISS, karte_schriftart_gross)
        zeichne_text(x + 20, y + 20, str(zahl), WEISS, karte_schriftart_klein)
        zeichne_text(x + breite - 20, y + hoehe - 20, str(zahl), WEISS, karte_schriftart_klein)
    elif farbe == "Roll":
        for index, buchstabe in enumerate("ROLL"):
            buchstabe_farbe = FARBEN[index % len(FARBEN)]
            zeichne_text(x + breite // 2, y + 30 + index * 30, buchstabe, buchstabe_farbe, karte_schriftart_titel)
    elif farbe == "Switch":
        for index, buchstabe in enumerate("SWITCH"):
            buchstabe_farbe = FARBEN[index % len(FARBEN)]
            zeichne_text(x + breite // 2, y + 20 + index * 20, buchstabe, buchstabe_farbe, karte_schriftart_titel)

def zeichne_leeres_feld(x, y, breite, hoehe):
    feld_rechteck = pygame.Rect(x, y, breite, hoehe)
    pygame.draw.rect(fenster, GRAU, feld_rechteck, 5, border_radius=10)

def ziehe_karte():
    if len(deck) > 0:
        return deck.pop()
    return None

def karte_in_spalte(karte, spalte):
    farbe, zahl = karte
    for k in columns[spalte]:
        if k[0] == farbe or k[1] == zahl:
            return False
    columns[spalte].append(karte)
    return True

def frage_anzahl_spieler():
    global grundwert_spieler
    eingabe_aktiv = True
    fehlermeldung = ""

    while eingabe_aktiv:
        fenster.fill(WEISS)
        zeichne_text(BREITE // 2, HOEHE // 3, "Anzahl der Spieler (2-6):", SCHWARZ, knopf_schriftart)
        zeichne_text(BREITE // 2, HOEHE // 2, str(grundwert_spieler), SCHWARZ, knopf_schriftart)
        
        # Zeichne die Knöpfe für Erhöhung und Verringerung
        erhoehen_knopf = zeichne_knopf("+", BREITE // 2 + 100, HOEHE // 2, 50, 50)
        verringern_knopf = zeichne_knopf("-", BREITE // 2 - 100, HOEHE // 2, 50, 50)
        weiter_knopf = zeichne_knopf("Weiter", BREITE // 2, HOEHE // 2 + 100, 100, 50)

        if fehlermeldung:
            zeichne_text(BREITE // 2, HOEHE // 2 + 150, fehlermeldung, ROT, knopf_schriftart)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if erhoehen_knopf.collidepoint(event.pos) and grundwert_spieler < MAX_SPIELER:
                    grundwert_spieler += 1
                    fehlermeldung = ""
                elif verringern_knopf.collidepoint(event.pos) and grundwert_spieler > MIN_SPIELER:
                    grundwert_spieler -= 1
                    fehlermeldung = ""
                elif weiter_knopf.collidepoint(event.pos):
                    if MIN_SPIELER <= grundwert_spieler <= MAX_SPIELER:
                        return grundwert_spieler
                    else:
                        fehlermeldung = "Ungültige Spieleranzahl! Bitte wähle zwischen 2 und 6."

def spielfeld(anzahl_spieler):
    global columns, switch_column, handkarten
    aktueller_spieler = 1
    spiel_aktiv = True
    gezogene_karte = None
    text_anzeige = f"Spieler {aktueller_spieler} ist am Zug"
    switch_count = 0
    wahl_reihenfolge = []
    karte_ziehen_erlaubt = True  # Variable hinzugefügt

    def aktualisiere_wahl_reihenfolge():
        nonlocal wahl_reihenfolge
        if switch_count % 2 == 0:
            wahl_reihenfolge = [(aktueller_spieler + i - 1) % anzahl_spieler + 1 for i in range(anzahl_spieler)]
        else:
            wahl_reihenfolge = [(aktueller_spieler - i - 1) % anzahl_spieler + 1 for i in range(anzahl_spieler)]
    
    def handkarten_sortieren(spieler):
        handkarten[spieler - 1].sort(key=lambda x: FARBEN_NAME.index(x[0]))

    while spiel_aktiv:
        fenster.fill(WEISS)
        
        # Anzeige des aktuellen Spielers oder Fehlermeldung
        zeichne_text(BREITE // 2, HOEHE * 3 // 4, text_anzeige, SCHWARZ, knopf_schriftart)

        # Zeichne den Kartenstapel mit PUSH-Schriftzug
        zeichne_karte(BREITE * 3 // 4 - 50, HOEHE // 2 - 75, 100, 150, None, TITLE_TEXT, SCHWARZ)

        # Zeichne Platzhalter für die Karten der Spieler am linken Spielrand
        for i in range(anzahl_spieler):
            zeichne_text(50, 50 + i * 100, f"Spieler {i + 1} Karten", SCHWARZ, kleine_knopf_schriftart)

        # Zeichne leere Felder für die drei Stapel in der Mitte
        feld_breite, feld_hoehe = 100, 150
        abstand = 20
        x_start = (BREITE - 3 * feld_breite - 2 * abstand) // 2
        for i in range(3):
            zeichne_leeres_feld(x_start + i * (feld_breite + abstand), HOEHE // 2 - feld_hoehe // 2, feld_breite, feld_hoehe)
        
        # Zeichne Karten in den Spalten
        for spalte in range(3):
            x_pos = x_start + spalte * (feld_breite + abstand)
            for j, karte in enumerate(columns[spalte]):
                farbe, zahl = karte
                if farbe == "Roll" or farbe == "Switch":
                    zeichne_karte(x_pos, HOEHE // 2 - feld_hoehe // 2 + j * 30, feld_breite, feld_hoehe, None, farbe, SCHWARZ)
                else:
                    zeichne_karte(x_pos, HOEHE // 2 - feld_hoehe // 2 + j * 30, feld_breite, feld_hoehe, zahl, farbe, FARBEN[FARBEN_NAME.index(farbe)])

        # Zeichne leeres Feld für das Zwischenlagern von Switch-Karten
        zeichne_leeres_feld((BREITE - feld_breite) // 2, HOEHE // 2 + feld_hoehe // 2 + abstand, feld_breite, feld_hoehe)
        
        # Zeichne Karten in der Switch-Spalte
        for j, karte in enumerate(switch_column):
            zeichne_karte((BREITE - feld_breite) // 2, HOEHE // 2 + feld_hoehe // 2 + abstand + j * 30, feld_breite, feld_hoehe, None, karte[0], SCHWARZ)

        # Zeichne Felder für gesicherte Karten unten links
        gesicherte_karten_y = HOEHE - feld_hoehe - 120
        for i in range(5):
            zeichne_leeres_feld(50 + i * (feld_breite + abstand), gesicherte_karten_y, feld_breite, feld_hoehe)
        zeichne_text(50 + 2 * (feld_breite + abstand), gesicherte_karten_y + feld_hoehe + 20, "Gesicherte Karten", SCHWARZ, kleine_knopf_schriftart)

        # Zeichne Felder für Handkarten rechts unten
        handkarten_y = HOEHE - feld_hoehe - 120
        for i in range(5):
            zeichne_leeres_feld(BREITE - (50 + i * (feld_breite + abstand) + feld_breite), handkarten_y, feld_breite, feld_hoehe)
        zeichne_text(BREITE - (50 + 2 * (feld_breite + abstand) + feld_breite), handkarten_y + feld_hoehe + 20, "Handkarten", SCHWARZ, kleine_knopf_schriftart)

        # Zeichne gezogene Karte neben den Stapel
        if gezogene_karte:
            farbe, zahl = gezogene_karte
            if farbe == "Roll" or farbe == "Switch":
                zeichne_karte(BREITE * 3 // 4 + 100, HOEHE // 2 - 75, 100, 150, None, farbe, SCHWARZ)
            else:
                zeichne_karte(BREITE * 3 // 4 + 100, HOEHE // 2 - 75, 100, 150, zahl, farbe, FARBEN[FARBEN_NAME.index(farbe)])

        # Zeichne die neuen Knöpfe
        karte_ziehen_knopf = zeichne_knopf("Karte ziehen", 100, HOEHE - 50, 100, 40, kleine_knopf_schriftart)
        karte_sichern_knopf = zeichne_knopf("Karte sichern", 250, HOEHE - 50, 100, 40, kleine_knopf_schriftart)
        spielzug_beenden_knopf = zeichne_knopf("Spielzug beenden", BREITE - 150, HOEHE - 50, 150, 40, kleine_knopf_schriftart)
        spiel_schliessen_knopf = zeichne_knopf("Spiel schließen", BREITE - 100, 50, 150, 40, kleine_knopf_schriftart)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if karte_ziehen_erlaubt and karte_ziehen_knopf.collidepoint(event.pos):
                    gezogene_karte = ziehe_karte()
                    print(f"Karte gezogen: {gezogene_karte}")
                    if gezogene_karte[0] == "Switch":
                        switch_column.append(gezogene_karte)
                        switch_count += 1
                        gezogene_karte = None
                    text_anzeige = f"Spieler {aktueller_spieler} ist am Zug"
                elif gezogene_karte:
                    placed = False
                    for spalte in range(3):
                        x_pos = x_start + spalte * (feld_breite + abstand)
                        spalte_rechteck = pygame.Rect(x_pos, HOEHE // 2 - feld_hoehe // 2, feld_breite, feld_hoehe)
                        if spalte_rechteck.collidepoint(event.pos):
                            if karte_in_spalte(gezogene_karte, spalte):
                                gezogene_karte = None
                                placed = True
                                break
                    if not placed and all(not karte_in_spalte(gezogene_karte, spalte) for spalte in range(3)):
                        text_anzeige = f"Spieler {aktueller_spieler} hat sein Glück überschätzt. Der nächste Spieler ist am Zug"
                        aktueller_spieler = (aktueller_spieler % anzahl_spieler) + 1
                        gezogene_karte = None
                elif spielzug_beenden_knopf.collidepoint(event.pos):
                    karte_ziehen_erlaubt = False  # Karte ziehen deaktivieren
                    aktualisiere_wahl_reihenfolge()
                    for spieler in wahl_reihenfolge:
                        text_anzeige = f"Spieler {spieler} wählt seine Karte"
                        pygame.display.flip()
                        pygame.time.wait(1000)  # Simuliert die Wartezeit für den Spieler
                    aktueller_spieler = (aktueller_spieler % anzahl_spieler) + 1
                    text_anzeige = f"Spieler {aktueller_spieler} ist am Zug"
                elif not karte_ziehen_erlaubt:
                    for spalte in range(3):
                        x_pos = x_start + spalte * (feld_breite + abstand)
                        spalte_rechteck = pygame.Rect(x_pos, HOEHE // 2 - feld_hoehe // 2, feld_breite, feld_hoehe)
                        if spalte_rechteck.collidepoint(event.pos):
                            handkarten[aktueller_spieler - 1].extend(columns[spalte])
                            columns[spalte] = []
                            handkarten_sortieren(aktueller_spieler)
                            text_anzeige = f"Spieler {aktueller_spieler} hat Karten genommen. Der nächste Spieler ist am Zug"
                            aktueller_spieler = (aktueller_spieler % anzahl_spieler) + 1
                            karte_ziehen_erlaubt = True  # Ermöglicht wieder das Ziehen einer Karte im nächsten Spielzug
                            break
                elif spiel_schliessen_knopf.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def main():
    while True:
        fenster.fill(WEISS)
        
        # Zeichne den Titel
        titel_laenge = len(TITLE_TEXT) * 40
        start_x = (BREITE - titel_laenge) // 2 + 20  # Adjusted to center
        for index, buchstabe in enumerate(TITLE_TEXT):
            farbe = FARBEN[index % len(FARBEN)]
            zeichne_text(start_x + index * 40, 100, buchstabe, farbe, titel_schriftart)
        
        # Zeichne die Knöpfe
        starten_knopf = zeichne_knopf("Spiel Starten", BREITE // 2, HOEHE // 2, 200, 50)
        verlassen_knopf = zeichne_knopf("Spiel Verlassen", BREITE // 2, HOEHE // 2 + 100, 200, 50)
        
        # Event-Schleife
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if starten_knopf.collidepoint(event.pos):
                    anzahl_spieler = frage_anzahl_spieler()
                    if anzahl_spieler:
                        spielfeld(anzahl_spieler)
                elif verlassen_knopf.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
