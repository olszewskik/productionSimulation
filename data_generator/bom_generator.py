import csv
import random

def generate_bom(inventory_file, output_file):
    # Wczytaj dane zapasów z pliku
    inventory_data = []
    with open(inventory_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        inventory_data = [row for row in reader]

    # Podział zapasów na typy
    fg_items = [item for item in inventory_data if item["Item Type"] == "FG"]
    sfg_items = [item for item in inventory_data if item["Item Type"] == "SFG"]
    rm_items = [item for item in inventory_data if item["Item Type"] == "RM"]

    # Zbiór przypisanych SFG
    assigned_sfg = set()

    # Lista danych BOM
    bom_data = []

    # Funkcja generująca BOM
    def add_bom_entry(parent_id, component_id, quantity, unit):
        bom_data.append({
            "BOM ID": parent_id,
            "Component ID": component_id,
            "Quantity per Unit": quantity,
            "Unit of Measure": unit
        })


    # Generowanie BOM dla FG
    for fg in fg_items:
        fg_id = fg["Item ID"]
        fg_unit = fg["Unit of Measure"]

        # Dodaj SFG do BOM FG
        fg_sfg_components = random.sample(sfg_items, random.randint(3, 6))
        for sfg in fg_sfg_components:
            add_bom_entry(fg_id, sfg["Item ID"], random.randint(1, 4), fg_unit)
            assigned_sfg.add(sfg["Item ID"])

        # Dodaj RM do BOM FG
        fg_rm_components = random.sample(rm_items, random.randint(2, 4))
        for rm in fg_rm_components:
            add_bom_entry(fg_id, rm["Item ID"], random.randint(1, 4), rm["Unit of Measure"])

    # Generowanie BOM dla SFG (nie wchodzących w BOM FG)
    unassigned_sfg = [sfg for sfg in sfg_items if sfg["Item ID"] not in assigned_sfg]
    for sfg in unassigned_sfg:
        sfg_id = sfg["Item ID"]
        sfg_unit = sfg["Unit of Measure"]
        # Dodaj pojedynczy RM do BOM SFG
        rm = random.choice(rm_items)
        add_bom_entry(sfg_id, rm["Item ID"], random.randint(1, 4), rm["Unit of Measure"])

    # Generowanie BOM dla pozostałych SFG
    for sfg in assigned_sfg:
        sfg_id = sfg
        sfg_unit = "PCS"
        # Dodaj 3-6 RM do BOM SFG
        sfg_rm_components = random.sample(rm_items, random.randint(3, 6))
        for rm in sfg_rm_components:
            add_bom_entry(sfg_id, rm["Item ID"], random.randint(1, 4), rm["Unit of Measure"])

    # Zapis BOM do pliku CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["BOM ID", "Component ID", "Quantity per Unit", "Unit of Measure"])
        writer.writeheader()
        writer.writerows(bom_data)

    print(f"BOM data has been saved to {output_file}.")
