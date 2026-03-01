from frappe import _
from frappe.desk.page.setup_wizard.setup_wizard import make_records


def make_fixtures():
    records = [
        # Pest Type
        {
            "doctype": "Pest Type",
            "pest_name": _("All Pest Types"),
            "is_group": 1,
            "name": _("All Pest Types"),
            "parent_pest_type": "",
            "standard_rate": 0.0,
            "description": _("All types of pests including flying, crawling, rodents, and reptiles")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("All Flying Pests"),
            "is_group": 1,
            "name": _("All Flying Pests"),
            "parent_pest_type": "All Pest Types",
            "standard_rate": 0.0,
            "description": _("All types of flying pests including flies, mosquitoes, and beetles")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("All Crawling Pests"),
            "is_group": 1,
            "name": _("All Crawling Pests"),
            "parent_pest_type": "All Pest Types",
            "standard_rate": 0.0,
            "description": _("All types of crawling pests including ants, spiders, and cockroaches")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Rodents"),
            "is_group": 1,
            "name": _("Rodents"),
            "parent_pest_type": "All Pest Types",
            "standard_rate": 0.0,
            "description": _("All types of rodents including rats, mice, and squirrels")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Reptiles"),
            "is_group": 1,
            "name": _("Reptiles"),
            "parent_pest_type": "All Pest Types",
            "standard_rate": 0.0,
            "description": _("All types of reptiles including geckos, snakes, and vipers")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Gecko"),
            "is_group": 0,
            "name": _("Gecko"),
            "parent_pest_type": "Reptiles",
            "standard_rate": 0.0,
            "description": _("Geckos are small to medium-sized lizards found in warm climates")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Snakes"),
            "is_group": 0,
            "name": _("Snakes"),
            "parent_pest_type": "Reptiles",
            "standard_rate": 0.0,
            "description": _("Snakes are elongated, legless, carnivorous reptiles of the suborder Serpentes")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Vipers"),
            "is_group": 0,
            "name": _("Vipers"),
            "parent_pest_type": "Reptiles",
            "standard_rate": 0.0,
            "description": _("Vipers are a family of venomous snakes found in most parts of the world")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Flies"),
            "is_group": 0,
            "name": _("Flies"),
            "parent_pest_type": "All Flying Pests",
            "standard_rate": 0.0,
            "description": _("Flies are insects of the order Diptera, characterized by a single pair of wings and compound eyes")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Drain Flies"),
            "is_group": 0,
            "name": _("Drain Flies"),
            "parent_pest_type": "All Flying Pests",
            "standard_rate": 0.0,
            "description": _("Drain Flies are small flies that breed in stagnant water and organic matter")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Mosquitoes"),
            "is_group": 0,
            "name": _("Mosquitoes"),
            "parent_pest_type": "All Flying Pests",
            "standard_rate": 0.0,
            "description": _("Mosquitoes are small, flying insects known for their biting and bloodsucking behavior")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Chironomus"),
            "is_group": 0,
            "name": _("Chironomus"),
            "parent_pest_type": "All Flying Pests",
            "standard_rate": 0.0,
            "description": _("Chironomus, also known as non-biting midges, are small flies that resemble mosquitoes but do not bite")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Beetles"),
            "is_group": 0,
            "name": _("Beetles"),
            "parent_pest_type": "All Crawling Pests",
            "standard_rate": 0.0,
            "description": _("Beetles are a group of insects that form the order Coleoptera, characterized by their hard exoskeleton and forewings")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Flour Beetle"),
            "is_group": 0,
            "name": _("Flour Beetle"),
            "parent_pest_type": "All Crawling Pests",
            "standard_rate": 0.0,
            "description": _("Flour Beetles are small, reddish-brown beetles that infest stored grain products")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Bed Bugs"),
            "is_group": 0,
            "name": _("Bed Bugs"),
            "parent_pest_type": "All Crawling Pests",
            "standard_rate": 0.0,
            "description": _("Bed Bugs are small, reddish-brown insects that feed on the blood of humans and animals while they sleep")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Mites"),
            "is_group": 0,
            "name": _("Mites"),
            "parent_pest_type": "All Crawling Pests",
            "standard_rate": 0.0,
            "description": _("Mites are small arthropods that belong to the class Arachnida and are closely related to ticks")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Fleas"),
            "is_group": 0,
            "name": _("Fleas"),
            "parent_pest_type": "All Crawling Pests",
            "standard_rate": 0.0,
            "description": _("Fleas are small, wingless insects that are external parasites of mammals and birds, known for their jumping ability and bloodsucking behavior")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Ticks"),
            "is_group": 0,
            "name": _("Ticks"),
            "parent_pest_type": "All Crawling Pests",
            "standard_rate": 0.0,
            "description": _("Ticks are small arachnids that are ectoparasites, feeding on the blood of mammals, birds, and sometimes reptiles and amphibians")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Ants"),
            "is_group": 0,
            "name": _("Ants"),
            "parent_pest_type": "All Crawling Pests",
            "standard_rate": 0.0,
            "description": _("Ants are social insects that live in colonies and are known for their ability to work together to find food and build nests")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Spiders"),
            "is_group": 0,
            "name": _("Spiders"),
            "parent_pest_type": "All Crawling Pests",
            "standard_rate": 0.0,
            "description": _("Spiders are arachnids that have eight legs and are known for their ability to spin webs to catch prey")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Cockroaches"),
            "is_group": 0,
            "name": _("Cockroaches"),
            "parent_pest_type": "All Crawling Pests",
            "standard_rate": 0.0,
            "description": _("Cockroaches are insects that are known for their resilience and ability to survive in various environments, often considered pests due to their association with unsanitary conditions")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Scorpions"),
            "is_group": 0,
            "name": _("Scorpions"),
            "parent_pest_type": "All Crawling Pests",
            "standard_rate": 0.0,
            "description": _("Scorpions are predatory arachnids that have a segmented tail with a venomous stinger, known for their nocturnal behavior and ability to survive in harsh environments")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Centipede"),
            "is_group": 0,
            "name": _("Centipede"),
            "parent_pest_type": "All Crawling Pests",
            "standard_rate": 0.0,
            "description": _("Centipedes are elongated arthropods with one pair of legs per body segment, known for their fast movement and venomous bite")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Cats"),
            "is_group": 0,
            "name": _("Cats"),
            "parent_pest_type": "All Pest Types",
            "standard_rate": 0.0,
            "description": _("Cats are small, carnivorous mammals that are often kept as pets but can also be considered pests when they stray into areas where they are not wanted")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Rats"),
            "is_group": 0,
            "name": _("Rats"),
            "parent_pest_type": "Rodents",
            "standard_rate": 0.0,
            "description": _("Rats are medium-sized rodents that are known for their adaptability and ability to thrive in various environments, often considered pests due to their association with unsanitary conditions and potential to spread diseases")
        },
        # Service Type
        {
            "doctype": "PC Service Type",
            "service_name": _("Public health pest control"),
            "description": _("Pest control services aimed at protecting public health by controlling pests that can transmit diseases or cause health hazards")
        },
        {
            "doctype": "PC Service Type",
            "service_name": _("Termite control"),
            "description": _("Pest control services focused on the prevention and elimination of termite infestations, which can cause significant damage to wooden structures")
        },
        {
            "doctype": "PC Service Type",
            "service_name": _("Sterilization and disinfection"),
            "description": _("Services that involve sterilization and disinfection to eliminate pests and prevent the spread of diseases, often used in healthcare settings, food processing facilities, and other environments where hygiene is critical")
        },
        # Severity Level
        {
            "doctype": "Severity Level",
            "severity_level": "Low",
            "description": "Low severity level for minor pest issues"
        },
        {
            "doctype": "Severity Level",
            "severity_level": "Medium",
            "description": "Medium severity level for moderate pest issues"
        },
        {
            "doctype": "Severity Level",
            "severity_level": "High",
            "description": "High severity level for severe pest issues"
        },
        {
            "doctype": "Severity Level",
            "severity_level": "Preventive",
            "description": "Preventive severity level for proactive pest control measures"
        },
        # Visit Type
        {
            "doctype": "Visit Type",
            "visit_type": "Preventive",
            "description": "Preventive visit for regular pest control"
        },
        {
            "doctype": "Visit Type",
            "visit_type": "Emergency",
            "description": "Emergency visit for urgent pest control"
        },
        {
            "doctype": "Visit Type",
            "visit_type": "Follow-up",
            "description": "Follow-up visit after initial pest control"
        },
        {
            "doctype": "Visit Type",
            "visit_type": "Inspection",
            "description": "Inspection visit to assess pest control needs"
        },
        {
            "doctype": "Visit Type",
            "visit_type": "Consultation",
            "description": "Consultation visit for pest control advice"
        },
        {
            "doctype": "Visit Type",
            "visit_type": "Treatment",
            "description": "Treatment visit for pest control application"
        },
        {
            "doctype": "Visit Type",
            "visit_type": "Monitoring",
            "description": "Monitoring visit to check pest control effectiveness"
        }
    ]
    make_records(records)
