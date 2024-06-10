# Projekt: Hotelreservierungssystem

Anna Heldstab, Chiara Mamie, Naara Rivera, Dennis Langer, Luca Lenherr

### Überblick

Blabla Erklärung Hotelreservationssystem...

### Funktionalitäten

Unser Hotelreservierungssystem deckt die vorgegebenen User Stories ab und besteht aus mehreren Managern, die spezifische Aufgaben erfüllen und vom main_combined_console.py verwendet werden:

- **HotelManager**: Verwalten von Hotelinformationen und Zimmern
- **UserManager**: Verwalten von Benutzerinformationen und Authentifizierung
- **SearchManager**: Suchen von Hotels und Zimmern
- **ReservationManager**: Verwalten von Buchungen

### Anwendung des Codes:

1. **Datenbank einrichten:**
   Beim ersten Start wird die Datenbank automatisch generiert, falls sie nicht vorhanden ist.

2. **Starten des Systems:**
   Das Hauptskript `main_combined_console.py` starten, um die Benutzeroberfläche der Konsole zu öffnen.

3. **Navigation durch das System:**
   - **Gastnutzer** können Hotels durchsuchen und Zimmer buchen.
   - **Registrierte Nutzer** haben die gleichen Optionen wie Gastnutzer, können aber zusätzlich ihre Buchungshistorie einsehen, Buchungen verwalten sowie auch Accountinformationen ansehen und bearbeiten.
   - **Admin-Nutzer** können Hotelinformationen pflegen (Hotel hinzufügen, bearbeiten und löschen) und alle Hotels sowie Buchungen einsehen.

4. **Interaktive Eingaben:**
   Das System fordert den Nutzer auf, Eingaben zu machen (mittels Zahlen für die Navigation im Menü), um verschiedene Aktionen durchzuführen (z.B. Hotel suchen, Zimmer buchen, etc.).

### Besonderheiten
- Das eingegeben Datum wird auf Korrektheit geprüft.
- Wenn zwei Daten eingegeben werden, wird sichergestellt, dass das Startdatum immer kleiner ist wie das Enddatum.
- Accountinformationen können angepasst werden.
- Räume können nachträglich zu Hotels hinzugefügt werden.
- Die Anzahl der Loginversuche ist beschränkt (bei 3 Fehlversucher besteht nur noch die Option, sich neu zu Registrieren oder als Gast fortzufahren).
- Buchungen können im Nachhinein angepasst werden (allerdings nur jene in der Zukunft).
- Usernames und Zimmernummern (pro Hotel) werden auf Duplikate geprüft, damit diese Werte nicht doppelt auf der Datenbank existieren.


### Unser Vorhehen

Zu Beginn unseres Projekts haben wir uns eine Projektumgebung auf Github eingerichtet, damit wir alle zusammen am gleichen Code arbeiten konnten. Dabei traten allerdings regelmässig Probleme mit der Verknüpfung von GitHub und PyCharm auf, die wir durch Anpassungen in den VCS-Einstellungen von PyCharm versuchten zu lösen. Nachdem die Umgebung endlich funktionierte, haben wir uns in PyCharm umgesehen und einen Überblick über die eigentliche Projektarbeit sowie in die vorgegebene Projektstruktur samt Manager und Konsolenfunktionen verschafft.

Anschliessend haben wir die User Stories analysiert und diese in einer Excel-Liste den jeweiligen Managern zugeordnet. Unsere Gruppe besteht aus fünf Mitgliedern, daher haben wir die Manager unter uns aufgeteilt, sodass jeder für einen Manager verantwortlich war. Während der Entwicklung halfen wir uns gegenseitig und nutzten auch ChatGPT für Unterstützung.

Nachdem die Grundfunktionen implementiert waren, versuchten wir, die einzelnen Manager in einer kombinierten Konsole zusammenzuführen. Zur besseren Orientierung erstellten wir ein Flussdiagramm, welches die Pfade unseres Menüs visuell darstellt und uns beim Umsetzten in Python eine grosse Hilfe war.

Unseren Code haben wir regelmässig gemeinsam getestet und weitere Funktionen und Methoden hinzugefügt, um alle Anforderungen der User Stories zu erfüllen. In weiteren Tests und Korrekturen stellten wir sicher, dass das System einwandfrei funktionierte.

### Zusammenarbeit als Gruppe

Wir haben uns mehrmals wöchentlich als Gruppe getroffen, vorzugsweise an der Fachhochschule oder bei jemandem von uns zuhause. Wenn wir uns nicht persönlich treffen konnten, erfolgte die Kommunikation online über  Microsoft Teams. Zusätzlich haben wir ein Kanban-Board erstellt, um alle Funktionalitäten und Aufgaben zu organisieren und zu verfolgen. Aufgrund der Schwierigkeiten mit dem Push und Pull vom GitHub-Repository haben wir hauptsächlich in gemeinsamen Sessions in PyCharm gearbeitet.


