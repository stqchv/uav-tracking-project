import cv2
import os
import time
from communication.video_receiver import start_video_stream, receive_frame

def main():
    # Folder docelowy o który prosiłeś
    save_dir = "training_dataset/images"
    os.makedirs(save_dir, exist_ok=True)
    
    print(f"Folder docelowy: {save_dir}/")
    print("Program automatycznie zapisuje klatki wideo jako zdjęcia.")
    print("Wciśnij 'q' aby zakończyć nagrywanie.")

    video_stream = start_video_stream(port=5000)
    if video_stream is None: return
    time.sleep(0.5)

    saved_count = 0
    
    # --- KONFIGURACJA ZAPISU ---
    # Ile sekund odczekać przed zapisaniem kolejnej klatki?
    # 0.2s = 5 klatek na sekundę (idealne dla powolnego lotu)
    # Zmień na 0.5s jeśli nagrywasz statyczne sceny
    save_interval = 0.5
    last_save_time = time.time()

    try:
        while True:
            ret, frame = receive_frame(video_stream)
            if not ret or frame is None:
                continue

            current_time = time.time()

            # --- AUTOMATYCZNY ZAPIS ---
            # Jeśli upłynął zadany czas od ostatniego zdjęcia, zapisz nowe
            if current_time - last_save_time >= save_interval:
                timestamp = int(current_time * 1000)
                filename = os.path.join(save_dir, f"frame_{timestamp}.jpg")
                
                # Zapisujemy czysty obraz z drona
                cv2.imwrite(filename, frame)
                saved_count += 1
                last_save_time = current_time

            # --- PODGLĄD DLA OPERATORA ---
            display_frame = frame.copy()
            
            # Migający, czerwony napis "REC" i licznik zdjęć
            if int(current_time * 2) % 2 == 0:  # Miga co pół sekundy
                cv2.circle(display_frame, (25, 30), 10, (0, 0, 255), -1) # Czerwona kropka
            
            cv2.putText(display_frame, f"REC | Zapisano: {saved_count}", (45, 38), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Automatyczna Rejestracja Datasetu", display_frame)

            # Wyjście awaryjne
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print(f"\nNagrywanie zakończone. Zebrano {saved_count} klatek.")
                break
    finally:
        video_stream.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()