from frappe import _
from frappe.desk.page.setup_wizard.setup_wizard import make_records


def make_fixtures():
    records = [
        # Pest Type
        {
            "doctype": "Pest Type",
            "pest_name": _("Gecko"),
            "name": _("Gecko"),
            "description": _("Geckos are small to medium-sized lizards found in warm climates")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Snakes"),
            "name": _("Snakes"),
            "description": _("Snakes are elongated, legless, carnivorous reptiles of the suborder Serpentes")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Vipers"),
            "name": _("Vipers"),
            "description": _("Vipers are a family of venomous snakes found in most parts of the world")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Flies"),
            "name": _("Flies"),
            "description": _("Flies are insects of the order Diptera, characterized by a single pair of wings and compound eyes")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Drain Flies"),
            "name": _("Drain Flies"),
            "description": _("Drain Flies are small flies that breed in stagnant water and organic matter")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Mosquitoes"),
            "name": _("Mosquitoes"),
            "description": _("Mosquitoes are small, flying insects known for their biting and bloodsucking behavior")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Chironomus"),
            "name": _("Chironomus"),
            "description": _("Chironomus, also known as non-biting midges, are small flies that resemble mosquitoes but do not bite")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Beetles"),
            "name": _("Beetles"),
            "description": _("Beetles are a group of insects that form the order Coleoptera, characterized by their hard exoskeleton and forewings")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Flour Beetle"),
            "name": _("Flour Beetle"),
            "description": _("Flour Beetles are small, reddish-brown beetles that infest stored grain products")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Bed Bugs"),
            "name": _("Bed Bugs"),
            "description": _("Bed Bugs are small, reddish-brown insects that feed on the blood of humans and animals while they sleep")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Mites"),
            "name": _("Mites"),
            "description": _("Mites are small arthropods that belong to the class Arachnida and are closely related to ticks")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Fleas"),
            "name": _("Fleas"),
            "description": _("Fleas are small, wingless insects that are external parasites of mammals and birds, known for their jumping ability and bloodsucking behavior")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Ticks"),
            "name": _("Ticks"),
            "description": _("Ticks are small arachnids that are ectoparasites, feeding on the blood of mammals, birds, and sometimes reptiles and amphibians")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Ants"),
            "name": _("Ants"),
            "description": _("Ants are social insects that live in colonies and are known for their ability to work together to find food and build nests")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Spiders"),
            "name": _("Spiders"),
            "description": _("Spiders are arachnids that have eight legs and are known for their ability to spin webs to catch prey")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Cockroaches"),
            "name": _("Cockroaches"),
            "description": _("Cockroaches are insects that are known for their resilience and ability to survive in various environments, often considered pests due to their association with unsanitary conditions")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Scorpions"),
            "name": _("Scorpions"),
            "description": _("Scorpions are predatory arachnids that have a segmented tail with a venomous stinger, known for their nocturnal behavior and ability to survive in harsh environments")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Centipede"),
            "name": _("Centipede"),
            "description": _("Centipedes are elongated arthropods with one pair of legs per body segment, known for their fast movement and venomous bite")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Cats"),
            "name": _("Cats"),
            "description": _("Cats are small, carnivorous mammals that are often kept as pets but can also be considered pests when they stray into areas where they are not wanted")
        },
        {
            "doctype": "Pest Type",
            "pest_name": _("Rats"),
            "name": _("Rats"),
            "description": _("Rats are medium-sized rodents that are known for their adaptability and ability to thrive in various environments, often considered pests due to their association with unsanitary conditions and potential to spread diseases")
        },
        # Pest Category (replaces the old Pest Type tree grouping)
        {
            "doctype": "Pest Category",
            "category_name": _("Flying Pests"),
            "pests": [
                {"pest_type": _("Flies")},
                {"pest_type": _("Drain Flies")},
                {"pest_type": _("Mosquitoes")},
                {"pest_type": _("Chironomus")}
            ]
        },
        {
            "doctype": "Pest Category",
            "category_name": _("Crawling Pests"),
            "pests": [
                {"pest_type": _("Beetles")},
                {"pest_type": _("Flour Beetle")},
                {"pest_type": _("Bed Bugs")},
                {"pest_type": _("Mites")},
                {"pest_type": _("Fleas")},
                {"pest_type": _("Ticks")},
                {"pest_type": _("Ants")},
                {"pest_type": _("Spiders")},
                {"pest_type": _("Cockroaches")},
                {"pest_type": _("Scorpions")},
                {"pest_type": _("Centipede")}
            ]
        },
        {
            "doctype": "Pest Category",
            "category_name": _("Rodents"),
            "pests": [
                {"pest_type": _("Rats")}
            ]
        },
        {
            "doctype": "Pest Category",
            "category_name": _("Reptiles"),
            "pests": [
                {"pest_type": _("Gecko")},
                {"pest_type": _("Snakes")},
                {"pest_type": _("Vipers")}
            ]
        },
        # Service Type
        {
            "doctype": "Service Type",
            "service_name": _("Public health pest control"),
            "description": _("Pest control services aimed at protecting public health by controlling pests that can transmit diseases or cause health hazards")
        },
        {
            "doctype": "Service Type",
            "service_name": _("Termite control"),
            "description": _("Pest control services focused on the prevention and elimination of termite infestations, which can cause significant damage to wooden structures")
        },
        {
            "doctype": "Service Type",
            "service_name": _("Sterilization and disinfection"),
            "description": _("Services that involve sterilization and disinfection to eliminate pests and prevent the spread of diseases, often used in healthcare settings, food processing facilities, and other environments where hygiene is critical")
        },
        # Condition Level
        {
            "doctype": "Condition Level",
            "level_name": "Low",
            "description": "Low severity level for minor pest issues"
        },
        {
            "doctype": "Condition Level",
            "level_name": "Medium",
            "description": "Medium severity level for moderate pest issues"
        },
        {
            "doctype": "Condition Level",
            "level_name": "High",
            "description": "High severity level for severe pest issues"
        },
        {
            "doctype": "Condition Level",
            "level_name": "Preventive",
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
