import csv
import random


# Funkcje pomocnicze
def generate_inventory_id(group_code, item_type, unique_number):
    return f"INV-{group_code}-{item_type}-{unique_number:04d}"


def generate_model_code(group_code, model_number):
    return f"MDL-{group_code}-{model_number:02d}"


def generate_description(item_type, unique_suffix):
    base_descriptions = {
        "Finished Product": ["Steel Frame", "Metal Beam", "Structural Bracket", "Steel Plate", "Construction Module"],
        "Semi-Finished": ["Processed Component", "Intermediate Frame", "Partially Welded Plate", "Fabricated Section"],
        "Raw Material": ["Raw Steel", "Welding Rods", "Bolts and Screws", "Metal Sheets", "Industrial Paint"]
    }
    return f"{random.choice(base_descriptions[item_type])} {unique_suffix}"


def generate_inventory(output_file):
    # Parametry danych
    groups = {
        "STRC": "Structures",
        "BEAM": "Beams",
        "PLTE": "Plates",
        "MODL": "Modules"
    }
    finished_products_range = (50, 100)
    semi_products_range = (3, 6)
    purchase_items_range = (100, 150)

    # Lista zapasów
    inventory_data = []
    fg_counter = 1
    sfg_counter = 1
    rm_counter = 1

    # Generowanie zapasów dla każdej grupy
    for group_code, group_name in groups.items():
        model_count = random.randint(8, 15)
        models = [generate_model_code(group_code, i + 1) for i in range(model_count)]
        finished_products_count = random.randint(*finished_products_range)

        for _ in range(finished_products_count):
            # Wyroby gotowe (Finished Goods)
            finished_id = generate_inventory_id(group_code, "FG", fg_counter)
            finished_description = generate_description("Finished Product", fg_counter)
            model = random.choice(models)
            inventory_data.append([finished_id, finished_description, "PCS", group_name, "FG", model])
            fg_counter += 1

            # Półprodukty (Semi-Finished Goods)
            semi_products_count = random.randint(*semi_products_range)
            for _ in range(semi_products_count):
                semi_id = generate_inventory_id(group_code, "SFG", sfg_counter)
                semi_description = generate_description("Semi-Finished", sfg_counter)
                inventory_data.append([semi_id, semi_description, "PCS", group_name, "SFG", model])
                sfg_counter += 1

    # Dodanie zapasów zakupowych (Raw Materials)
    purchase_items_count = random.randint(*purchase_items_range)
    for _ in range(purchase_items_count):
        purchase_id = generate_inventory_id("RM", "RM", rm_counter)
        purchase_description = generate_description("Raw Material", rm_counter)
        inventory_data.append([purchase_id, purchase_description, "PCS", "NULL", "RM", "NULL"])
        rm_counter += 1

    # Zapis do pliku CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Item ID", "Item Description", "Unit of Measure", "Group", "Item Type", "Model"])
        writer.writerows(inventory_data)

    print(f"Data has been saved to {output_file}.")


