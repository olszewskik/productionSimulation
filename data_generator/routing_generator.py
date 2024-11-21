import pandas as pd
import random


def generate_routes(inventory_file, workcenters_file, output_file):
    # Parametry czasów dla operacji
    setup_time_ranges = {
        "Assembly": (10, 30),
        "Welding": (10, 30),
        "Machining": (20, 75),
        "Painting": (15, 30),
        "Packaging": (0, 0)
    }
    run_time_ranges = {
        "Assembly": (120, 360),
        "Welding": (120, 360),
        "Machining_SFG": (60, 120),
        "Machining_FG": (90, 240),
        "Painting": lambda total_assembly_welding_time: int(total_assembly_welding_time * random.uniform(0.07, 0.12)),
        "Packaging": {
            "Structures": 30,
            "Beams": 20,
            "Plates": 25,
            "Modules": 40
        }
    }

    # Wczytanie zapasów i gniazd roboczych
    items_df = pd.read_csv(inventory_file)
    workcenters_df = pd.read_csv(workcenters_file)

    # Podział gniazd roboczych na departamenty
    departments = ["Welding", "Machining", "Assembly", "Painting", "Packaging"]
    department_workcenters = {
        department: workcenters_df[workcenters_df["Department"] == department]["Workcenter ID"].tolist()
        for department in departments
    }

    # Funkcja generująca marszrutę
    def generate_routing(item_id, item_type, group):
        routing = []
        operation_number = 1
        total_assembly_welding_time = 0

        # Kolejność dla marszrut FG i SFG
        if item_type == "FG":
            steps = ["Assembly", "Welding"] * random.randint(2, 4) + (
                ["Machining"] if random.choice([True, False]) else []) + ["Painting", "Packaging"]
        else:  # SFG
            steps = ["Assembly", "Welding"] * random.randint(1, 2) + (
                ["Machining"] if random.choice([True, False]) else [])

        # Generowanie operacji
        for step in steps:
            workcenter_id = random.choice(department_workcenters[step])
            setup_time = random.randint(*setup_time_ranges[step])

            if step == "Machining":
                run_time = random.randint(*run_time_ranges[f"Machining_{item_type}"])
            elif step == "Painting":
                run_time = run_time_ranges["Painting"](total_assembly_welding_time)
            elif step == "Packaging":
                run_time = run_time_ranges["Packaging"][group]
            else:
                run_time = random.randint(*run_time_ranges[step])
                if step in ["Assembly", "Welding"]:
                    total_assembly_welding_time += run_time

            routing.append({
                "Item ID": item_id,
                "Operation Number": operation_number,
                "Operation Name": f"{step} {sum(1 for op in routing if op['Operation Name'].startswith(step)) + 1}",
                "Workcenter ID": workcenter_id,
                "Setup Time (min)": setup_time,
                "Run Time (min)": run_time,
                "Next Operation": operation_number + 1 if operation_number < len(steps) else None,
                "Previous Operation": operation_number - 1 if operation_number > 1 else None
            })
            operation_number += 1

        return routing

    # Generowanie marszrut
    routings = []

    for _, item in items_df.iterrows():
        if item["Item Type"] in ["FG", "SFG"]:
            item_routing = generate_routing(item["Item ID"], item["Item Type"], item["Group"])
            routings.extend(item_routing)

    # Konwersja na DataFrame i zapis do pliku CSV
    routings_df = pd.DataFrame(routings)
    routings_df.to_csv(output_file, index=False)

    print(f"Routing data has been generated and saved to {output_file}.")
