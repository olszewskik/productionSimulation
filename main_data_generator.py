from data_generator import generate_inventory, generate_bom, generate_workcenter, generate_workcenter_availabiity, generate_routes

generate_inventory(output_file='data/inventory.csv')
generate_bom(inventory_file='data/inventory.csv', output_file='data/bom.csv')
generate_workcenter(output_file='data/workcenters.csv')
generate_workcenter_availabiity(workcenters_file='data/workcenters.csv', output_file='data/workcenter_availabiity.csv')
generate_routes(inventory_file='data/inventory.csv', workcenters_file='data/workcenters.csv', output_file='data/routes.csv')
