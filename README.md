# README Pythonprojekt
In diesem README zeigen wir zu erst, wo welche UserStories abgedeckt werden.
Anschliessend befindet sich eine kurze Projektdokumentation. 

## UserStories

---

**User Story 1.1:**

*Als Gastnutzer möchte ich die verfügbaren Hotels durchsuchen, damit ich dasjenige auswählen kann, welches meinen Wünschen entspricht.*

**Abgedeckt durch:**
- `show_hotels` in `main_combined_console.py`
- `get_hotels` in `SearchManager.py`
- `get_available_rooms` in `SearchManager.py`

---

**User Story 1.1.1:**

*Ich möchte alle Hotels in einer Stadt durchsuchen, damit ich das Hotel nach meinem bevorzugten Standort (Stadt) auswählen kann.*

**Abgedeckt durch:**
- `show_hotels` in `main_combined_console.py`
- `get_hotels` in `SearchManager.py`

---

**User Story 1.1.2:**

*Ich möchte alle Hotels in einer Stadt nach der Anzahl der Sterne durchsuchen.*

**Abgedeckt durch:**
- `show_hotels` in `main_combined_console.py`
- `get_hotels` in `SearchManager.py`

---

**User Story 1.1.3:**

*Ich möchte alle Hotels in einer Stadt durchsuchen, die Zimmer haben, die meiner Gästezahl entsprechen (nur 1 Zimmer pro Buchung), entweder mit oder ohne Anzahl der Sterne.*

**Abgedeckt durch:**
- `show_hotels` in `main_combined_console.py`
- `get_hotels` in `SearchManager.py`

---

**User Story 1.1.4:**

*Ich möchte alle Hotels in einer Stadt durchsuchen, die während meines Aufenthaltes Zimmer für meine Gästezahl zur Verfügung haben, entweder mit oder ohne Anzahl der Sterne.*

**Abgedeckt durch:**
- `show_hotels` in `main_combined_console.py`
- `get_hotels` in `SearchManager.py`

---

**User Story 1.1.5:**

*Ich möchte die folgenden Informationen pro Hotel sehen: Name, Adresse, Anzahl der Sterne.*

**Abgedeckt durch:**
- `show_hotels` in `main_combined_console.py`
- `get_hotels` in `SearchManager.py`

---

**User Story 1.1.6:**

*Ich möchte ein Hotel auswählen, um die Details zu sehen (z.B. verfügbare Zimmer).*

**Abgedeckt durch:**
- `show_hotels` in `main_combined_console.py`
- `get_available_rooms` in `SearchManager.py`

---

**User Story 1.2:**

*Als Gastnutzer möchte ich Details zu verschiedenen Zimmertypen (EZ, DZ, Familienzimmer), die in einem Hotel verfügbar sind, sehen, einschliesslich der maximalen Anzahl von Gästen für dieses Zimmer, Beschreibung, Preis und Ausstattung.*

**Abgedeckt durch:**
- `show_hotels` in `main_combined_console.py`
- `get_available_rooms` in `SearchManager.py`

---

**User Story 1.2.2:**

*Ich möchte nur die verfügbaren Zimmer sehen.*

**Abgedeckt durch:**
- `get_available_rooms` in `SearchManager.py`

---

**User Story 1.3:**

*Als Gastbenutzer möchte ich ein Zimmer in einem bestimmten Hotel buchen, um meinen Urlaub zu planen.*

**Abgedeckt durch:**
- `search_and_book_hotel` in `main_combined_console.py`
- `book_room_registered` in `ReservationManager.py`
- `book_room_guest` in `ReservationManager.py`

---

**User Story 1.4:**

*Als Gastnutzer möchte ich möglichst wenig Informationen über mich preisgeben, damit meine Daten privat bleiben.*

**Abgedeckt durch:**
- `book_room_guest` in `ReservationManager.py`

---

**User Story 1.5:**

*Als Gastnutzer möchte ich die Details meiner Reservierung in einer lesbaren Form erhalten (z.B. die Reservierung in einer dauerhaften Datei speichern), damit ich meine Buchung später überprüfen kann.*

**Abgedeckt durch:**
- `search_and_book_hotel` in `main_combined_console.py`
- `create_booking_confirmation_file` in `ReservationManager.py`

---

**User Story 1.6:**

*Als Gastbenutzer möchte ich mich mit meiner E-Mail-Adresse und einer persönlichen Kennung (Passwort) registrieren können, um weitere Funktionalitäten nutzen zu können.*

**Abgedeckt durch:**
- `add_user` in `UserManager.py`

---

**User Story 2:**

*Als registrierter Nutzer möchte ich alle Funktionalitäten eines Gastnutzers nutzen können und zusätzlich auf meine Buchungshistorie zugreifen, um meine kommenden Reservierungen zu verwalten.*

**Abgedeckt durch:**
- `user_menu` in `main_combined_console.py`
- `get_user_info` in `UserManager.py`
- `get_bookings_by_user` in `ReservationManager.py`
- `get_user_future_bookings` in `ReservationManager.py`

---

**User Story 2.1:**

*Als registrierter Benutzer möchte ich mich in mein Konto einloggen, um auf meine Buchungshistorie zuzugreifen.*

**Abgedeckt durch:**
- `login` in `UserManager.py`
- `get_user_info` in `UserManager.py`

---

**User Story 2.1.1:**

*Die Anwendungsfälle für meine Buchungen sind "neu/erstellen", "ändern/aktualisieren", "stornieren/löschen".*

**Abgedeckt durch:**
- `update_booking` in `ReservationManager.py`
- `confirm_update_booking` in `ReservationManager.py`
- `rollback_update_booking` in `ReservationManager.py`
- `delete_booking` in `ReservationManager.py`
- `get_user_future_bookings` in `ReservationManager.py`

---

**User Story 3.1:**

*Als Admin-Nutzer des Buchungssystems möchte ich die Möglichkeit haben, Hotelinformationen zu pflegen, um aktuelle Informationen im System zu haben.*

**Abgedeckt durch:**
- `admin_menu` in `main_combined_console.py`
- `add_hotel` in `HotelManager.py`
- `delete_hotel` in `HotelManager.py`
- `update_hotel_name` in `HotelManager.py`
- `update_hotel_stars` in `HotelManager.py`
- `update_hotel_address` in `HotelManager.py`

---

**User Story 3.1.1:**

*Ich möchte neue Hotels zum System hinzufügen.*

**Abgedeckt durch:**
- `add_hotel` in `HotelManager.py`

---

**User Story 3.1.2:**

*Ich möchte Hotels aus dem System entfernen.*

**Abgedeckt durch:**
- `delete_hotel` in `HotelManager.py`

---

**User Story 3.1.3:**

*Ich möchte die Informationen bestimmter Hotels aktualisieren, z.B. den Namen, die Sterne usw.*

**Abgedeckt durch:**
- `update_hotel_name` in `HotelManager.py`
- `update_hotel_stars` in `HotelManager.py`
- `update_hotel_address` in `HotelManager.py`

---

**User Story 3.2:**

*Als Admin-Nutzer des Buchungssystems möchte ich alle Buchungen aller Hotels sehen können, um eine Übersicht zu erhalten.*

**Abgedeckt durch:**
- `show_all_bookings` in `ReservationManager.py`

---

**User Story 3.4:**

*Ich möchte in der Lage sein, die Zimmerverfügbarkeit zu verwalten und die Preise in Echtzeit im Backend-System der Anwendung zu aktualisieren.*

**Abgedeckt durch:**
- `update_room` in `HotelManager.py`
- `add_rooms_to_hotel` in `HotelManager.py`

---