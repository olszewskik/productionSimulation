import random
import csv


# Funkcja do generowania klientów
def generate_customers(output_file):
    # Ustawienia krajów
    countries = {
        "Poland": {"code": "PL", "count": 3, "cities": ["Warsaw", "Krakow", "Gdansk"]},
        "Germany": {"code": "DE", "count": 5, "cities": ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt"]},
        "Sweden": {"code": "SE", "count": 4, "cities": ["Stockholm", "Gothenburg", "Malmo", "Uppsala"]}
    }

    # Przykładowe nazwy ulic
    streets = [
        "Main Street", "Oak Avenue", "Maple Road", "Elm Street",
        "River Lane", "High Street", "Church Road", "Park Avenue"
    ]

    # Funkcja do generowania adresów
    def generate_address(city, country_code):
        street = random.choice(streets)
        house_number = random.randint(1, 200)
        postal_code = f"{random.randint(10, 99)}-{random.randint(100, 999)}" if country_code == "PL" else f"{random.randint(10000, 99999)}"
        return f"{street} {house_number}, {postal_code} {city}, {country_code}"

    customers = []
    customer_id = 1
    generated_names = set()  # Zbiór unikalnych nazw

    for country, details in countries.items():
        for _ in range(details["count"]):
            # Generowanie unikalnej nazwy klienta
            while True:
                customer_name = f"{random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Sigma'])} " \
                                f"{random.choice(['Industries', 'Solutions', 'Systems', 'Logistics', 'Technologies'])}"
                if customer_name not in generated_names:
                    generated_names.add(customer_name)
                    break

            city = random.choice(details["cities"])
            address = generate_address(city, details["code"])
            customers.append({
                "Customer ID": f"CUST-{customer_id:03d}",
                "Customer Name": customer_name,
                "Country Code": details["code"],
                "Address": address
            })
            customer_id += 1

    # Zapis do pliku CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Customer ID", "Customer Name", "Country Code", "Address"])
        writer.writeheader()
        writer.writerows(customers)
    print(f"Customers data generated successfully in {output_file}.")


