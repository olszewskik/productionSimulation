import pandas as pd
import holidays
import csv


def generate_workcenter_availabiity(workcenters_file, output_file):
    # Parametry danych
    start_date = "2025-01-01"
    end_date = "2026-12-31"
    work_hours_per_day = 16  # Łączna dostępność (dwie zmiany)
    shift_start_hour = 6  # Start pierwszej zmiany
    shift_end_hour = 22  # Koniec drugiej zmiany

    # Generowanie kalendarza dni roboczych
    calendar = pd.date_range(start=start_date, end=end_date, freq="B")  # Dni robocze (bez weekendów)
    pl_holidays = holidays.Poland(years=[2025, 2026])
    working_days = [d for d in calendar if d not in pl_holidays]

    # Lista dostępności
    workcenter_availability = []

    # Funkcja pomocnicza do generowania dostępności
    def generate_availability(workcenter_id, workcenter_name):
        for day in working_days:
            workcenter_availability.append({
                "Workcenter ID": workcenter_id,
                "Workcenter Name": workcenter_name,
                "Date": day.strftime("%Y-%m-%d"),
                "From Datetime": f"{day.strftime('%Y-%m-%d')} {shift_start_hour:02d}:00",
                "To Datetime": f"{day.strftime('%Y-%m-%d')} {shift_end_hour:02d}:00",
                "Total Availability (Hours)": work_hours_per_day
            })

    # Ładowanie danych gniazd roboczych
    workcenters = []
    with open(workcenters_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        workcenters = list(reader)

    # Generowanie danych dostępności dla każdego gniazda
    for workcenter in workcenters:
        generate_availability(workcenter["Workcenter ID"], workcenter["Workcenter Name"])

    # Zapis do pliku CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "Workcenter ID", "Workcenter Name", "Date", "From Datetime", "To Datetime", "Total Availability (Hours)"
        ])
        writer.writeheader()
        writer.writerows(workcenter_availability)

    print(f"Daily workcenter availability data has been saved to {output_file}.")
