import re

# Define keyword-to-category mapping
# Order matters: more specific keywords should come before general ones.
# Added plurals and more specific items based on initial test run.
KEYWORD_CATEGORIES = [
    # Most specific multi-word phrases first
    ("Ceramic OE Equivalent Pad", "Automotive > Brakes > Brake Pads"),
    ("Low-Met OE Equivalent Pad", "Automotive > Brakes > Brake Pads"),
    ("Drum Brake Shoe", "Automotive > Brakes > Brake Shoes"),
    ("Narrow Ape", "Powersports > Motorcycle Parts > Handlebars & Controls > Handlebars"),
    ("Carrillo Rod", "Automotive > Engine Components > Connecting Rods"),

    # Brakes (specific kits first)
    ("Brake Pad and Rotor Kit", "Automotive > Brakes > Brake Kits"), # More specific than just pad or rotor
    ("Brake Kit", "Automotive > Brakes > Brake Kits"),
    ("Brake Pads", "Automotive > Brakes > Brake Pads"), # Plural
    ("Brake Pad", "Automotive > Brakes > Brake Pads"),
    ("Brake Shoe", "Automotive > Brakes > Brake Shoes"), # General Brake Shoe
    ("Brake Rotors", "Automotive > Brakes > Brake Rotors"), # Plural
    ("Brake Rotor", "Automotive > Brakes > Brake Rotors"),
    ("Rotors", "Automotive > Brakes > Brake Rotors"), # General rotors, assuming brake
    ("Rotor", "Automotive > Brakes > Brake Rotors"), # Singular

    # Suspension & Steering (specific kits first)
    ("Suspension System", "Automotive > Suspension > Complete Suspension Kits"),
    ("Coilover Kit", "Automotive > Suspension > Coilover Kits"),
    ("Shock Absorber", "Automotive > Suspension > Shocks & Struts"),
    ("Strut Assembly", "Automotive > Suspension > Shocks & Struts"),
    ("Strut Mounts", "Automotive > Suspension > Strut Mounts"), # Plural
    ("Strut Mount", "Automotive > Suspension > Strut Mounts"),
    ("Lowering Kit", "Automotive > Suspension > Lowering Kits"), # For Burly Brand Springer Fork Lowering Kit
    ("Springs", "Automotive > Suspension > Springs"),
    ("Roll Bar Cover", "Automotive > Interior Accessories > Roll Bar Covers"),

    # Engine Components (gaskets, specific parts first)
    ("Intake Manifold Gasket", "Automotive > Engine Components > Gaskets > Intake Manifold Gaskets"),
    ("Head Gasket", "Automotive > Engine Components > Gaskets > Head Gaskets"),
    ("Valve Cover Set", "Automotive > Engine Components > Gaskets > Valve Cover Gaskets"),
    ("Exhaust Gasket", "Automotive > Exhaust Systems > Gaskets & Hardware"), # Moved to be with other gaskets
    ("Piston Set", "Automotive > Engine Components > Pistons & Rings"),
    ("Connecting Rod", "Automotive > Engine Components > Connecting Rods"),
    ("Con Rod Bearing Set", "Automotive > Engine Components > Bearings > Connecting Rod Bearings"),
    ("Bearing Set", "Automotive > Engine Components > Bearings"), # General bearing set
    ("Bearing", "Automotive > Engine Components > Bearings"), # General bearing
    ("Aircharger Performance Intake", "Automotive > Engine Components > Air Intakes > Performance Intake Kits"),
    ("Intake", "Automotive > Engine Components > Air Intakes"), # General intake
    ("Valve Cover", "Automotive > Engine Components > Valve Covers"),
    ("Camshaft", "Automotive > Engine Components > Camshafts & Valvetrain"),
    ("Cylinder Kit", "Automotive > Engine Components > Cylinders & Cylinder Heads"),
    ("Radiator", "Automotive > Cooling System > Radiators"),
    ("Motor Oil", "Automotive > Oils & Fluids > Motor Oils"),
    ("Injectors", "Automotive > Fuel System > Fuel Injectors & Parts"), # Plural
    ("Injector", "Automotive > Fuel System > Fuel Injectors & Parts"), # Singular

    # Performance & Tuning
    ("Power Commander", "Automotive > Performance Parts > Engine Management & Tuning"),
    ("Power Vision", "Automotive > Performance Parts > Engine Management & Tuning"),
    ("Cat-Back", "Automotive > Exhaust Systems > Cat-Back Exhaust Kits"),
    ("Heat Screen", "Automotive > Performance Parts > Heat Shields & Insulation"),

    # Drivetrain
    ("Clutch Kit", "Automotive > Drivetrain > Clutches & Parts > Clutch Kits"),
    ("Flywheel Insert", "Automotive > Drivetrain > Flywheels & Parts"),
    ("Flywheel", "Automotive > Drivetrain > Flywheels & Parts"),
    ("LSD", "Automotive > Drivetrain > Differentials & Parts"),
    ("Differential", "Automotive > Drivetrain > Differentials & Parts"),
    ("Transmission Mount", "Automotive > Drivetrain > Transmission Mounts"), # Specific for "Trans Mount"
    ("Trans Mount", "Automotive > Drivetrain > Transmission Mounts"),


    # Wheels & Tires
    ("Lug Nuts", "Automotive > Wheels & Tires > Lug Nuts & Accessories"), # Plural
    ("Lug Nut", "Automotive > Wheels & Tires > Lug Nuts & Accessories"),
    ("Wheel", "Automotive > Wheels & Tires > Wheels"),

    # Exterior Accessories
    ("Hood Shield", "Automotive > Exterior Accessories > Hood Protection & Deflectors"),
    ("Flares", "Automotive > Exterior Accessories > Fender Flares"),
    ("Rail Caps", "Automotive > Exterior Accessories > Truck Bed Accessories > Bed Rail Caps"),
    ("Tailgate Assist", "Automotive > Exterior Accessories > Truck Bed Accessories > Tailgate Assists"),
    ("Bed Mat", "Automotive > Exterior Accessories > Truck Bed Accessories > Bed Liners & Mats"),
    ("Tool Box", "Automotive > Truck Bed Accessories > Tool Boxes"),

    # Interior Accessories
    ("Audio Kit", "Automotive > Interior Accessories > Car Audio Systems"),
    ("Headliner", "Automotive > Interior Accessories > Headliners"),
    ("Air Freshener", "Automotive > Interior Accessories > Air Fresheners"),
    ("Harness Pass Through Bezel", "Automotive > Interior Accessories > Seat & Seat Cover Accessories"),
    ("Racing Harnesses", "Automotive > Safety > Racing Harnesses"), # More specific
    ("Harness", "Automotive > Safety > Harnesses"), # General harness
    ("Center Console Molle Panel", "Automotive > Interior Accessories > Consoles & Organizers"),
    ("Device Mount", "Automotive > Interior Accessories > Phone & GPS Mounts"),

    # Lighting
    ("LED Headlight Bulbs", "Automotive > Lights & Lighting > Bulbs > LED Headlight Bulbs"), # More specific
    ("Headlight Bulb", "Automotive > Lights & Lighting > Bulbs > Headlight Bulbs"),
    ("LED Headlight", "Automotive > Lights & Lighting > Headlights & Assemblies"), # Assembly or kit

    # Motorcycle Specific (Grouping under Powersports now for clarity)
    ("Fairing", "Powersports > Motorcycle Parts > Bodywork > Fairings"),
    ("Brake Lever", "Powersports > Motorcycle Parts > Controls > Levers"),
    ("Clutch Lever", "Powersports > Motorcycle Parts > Controls > Levers"),
    ("Boot", "Powersports > Protective Gear > Footwear > Boots"), # For Gaerne SG12 Boot
    ("Fork Lowering Kit", "Powersports > Motorcycle Parts > Suspension > Fork Components"), # For Springer Fork Lowering Kit
    ("Fork", "Powersports > Motorcycle Parts > Suspension > Forks & Triple Trees"), # General fork
    ("Ape Hangers", "Powersports > Motorcycle Parts > Handlebars & Controls > Handlebars"), # For "Narrow Ape"
    ("Handlebar", "Powersports > Motorcycle Parts > Handlebars & Controls > Handlebars"), # General Handlebar
    ("Control Kit", "Powersports > Motorcycle Parts > Handlebars & Controls > Control Kits"),


    # General / Fallback (less specific, should be tried last)
    ("Suspension", "Automotive > Suspension"), # General suspension catch-all
    ("Gasket", "Automotive > Engine Components > Gaskets"), # General gasket
    ("Tool Bag", "Automotive > Tools & Equipment > Tool Storage"),
    ("Cover", "Automotive > Accessories > Covers"), # Generic cover
]

DEFAULT_CATEGORY = "Automotive > Miscellaneous Parts" # Keeps a general automotive fallback

def get_category_for_product(product_name):
    """
    Determines the category for a given product name based on keywords.
    """
    for keyword, category in KEYWORD_CATEGORIES:
        # Using \b for word boundaries to avoid partial matches (e.g., 'ring' in 'bearing')
        # Making keyword search case-insensitive
        if re.search(r"\b" + re.escape(keyword) + r"\b", product_name, re.IGNORECASE):
            return category
    return DEFAULT_CATEGORY

def main():
    input_filename = "categories1.txt"
    output_filename = "output_product_categories.txt" # New output file

    categorized_products = []

    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            product_names = [line.strip() for line in infile if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return

    for name in product_names:
        category = get_category_for_product(name)
        categorized_products.append(f"{name}|{category}")

    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for item in categorized_products:
                outfile.write(item + "\n")
        print(f"Successfully processed products and saved to '{output_filename}'")
    except IOError:
        print(f"Error: Could not write to output file '{output_filename}'.")

if __name__ == "__main__":
    main()
