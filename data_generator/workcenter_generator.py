import csv
import random


def generate_workcenter(output_file):
    # Parametry danych
    departments = ["Welding", "Machining", "Assembly", "Painting", "Packaging"]
    workcenters_range = (40, 45)
    workstation_capacity_range = (1, 10)
    efficiency_range = (75, 90)
    shifts = 2
    shift_hours = 8
    total_hours = shifts * shift_hours

    # Lista gniazd roboczych
    workcenters = []

    # Funkcja pomocnicza do generowania nazw
    def generate_workcenter_name(department, index):
        return f"{department[:3].upper()}-{index:02d}"

    # Generowanie gniazd roboczych
    total_workcenters = random.randint(*workcenters_range)
    department_distribution = [random.randint(5, 12) for _ in departments]
    department_distribution[-1] = total_workcenters - sum(department_distribution[:-1])

    workcenter_id = 1
    for department, count in zip(departments, department_distribution):
        for _ in range(count):
            name = generate_workcenter_name(department, workcenter_id)
            capacity = random.randint(*workstation_capacity_range)
            employees_per_station = random.choices([1, 2, 3], weights=[80, 15, 5])[0]
            efficiency = random.randint(*efficiency_range)
            workcenters.append({
                "Workcenter ID": f"WC-{workcenter_id:03d}",
                "Workcenter Name": name,
                "Department": department,
                "Workstation Capacity": capacity,
                "Employees per Station": employees_per_station,
                "Efficiency (%)": efficiency,
                "Shifts": shifts,
                "Availability (Hours)": total_hours
            })
            workcenter_id += 1

    # Zapis do pliku CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "Workcenter ID", "Workcenter Name", "Department",
            "Workstation Capacity", "Employees per Station",
            "Efficiency (%)", "Shifts", "Availability (Hours)"
        ])
        writer.writeheader()
        writer.writerows(workcenters)

    print(f"Workcenter data has been saved to {output_file}.")
