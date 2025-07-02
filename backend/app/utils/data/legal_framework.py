"""Base de connaissances juridique statique des baux commerciaux"""

LEGAL_FRAMEWORK = {
    "indexation_rules": {
        "valid_indices": {
            "ILAT": {
                "name": "Indice des Loyers des Activités Tertiaires",
                "mandatory_since": "2022-01-01",
                "legal_ref": "Décret n°2022-1267 du 30 septembre 2022"
            },
            "ILC": {
                "name": "Indice des Loyers Commerciaux", 
                "sectors": ["commerce", "artisanat"],
                "legal_ref": "Art. L145-38 Code de commerce"
            }
        },
        "deprecated_indices": {
            "ICC": {
                "name": "Indice du Coût de la Construction",
                "deprecated_since": "2022-01-01",
                "replacement": "ILAT",
                "legal_ref": "Décret n°2022-1267"
            },
            "ICT": {
                "name": "Indice du Coût des Travaux",
                "deprecated_since": "2022-01-01", 
                "replacement": "ILAT"
            }
        }
    },
    
    "revision_rules": {
        "triennal_revision": {
            "frequency": "3 ans",
            "notice_period_days": 90,
            "legal_ref": "Art. L145-38 Code de commerce",
            "prescription_years": 3
        },
        "renouvellement": {
            "notice_period_months": 6,
            "legal_ref": "Art. L145-9 Code de commerce"
        }
    },
    
    "critical_clauses": [
        {
            "clause_type": "indexation_icc", 
            "risk_level": "HIGH",
            "description": "Clause d'indexation ICC obsolète",
            "legal_issue": "ICC supprimé depuis 2022",
            "action": "Notification changement vers ILAT",
            "legal_ref": "Décret n°2022-1267"
        },
        {
            "clause_type": "revision_triennale",
            "risk_level": "MEDIUM", 
            "description": "Échéance révision triennale approche",
            "action": "Notifier révision 90 jours avant échéance",
            "legal_ref": "Art. L145-38 Code de commerce"
        }
    ],
    
    "mandatory_clauses": [
        {
            "type": "destination",
            "description": "Clause de destination obligatoire",
            "legal_ref": "Art. L145-47 Code de commerce"
        },
        {
            "type": "duree_minimale",
            "description": "Durée minimale 9 ans sauf dérogation",
            "legal_ref": "Art. L145-4 Code de commerce"
        }
    ]
}

MARKET_BENCHMARKS = {
    "ile_de_france": {
        "paris_center": {"min": 800, "max": 1500, "median": 1200},
        "paris_periphery": {"min": 400, "max": 800, "median": 600},
        "banlieue_proche": {"min": 250, "max": 450, "median": 350},
        "banlieue_eloignee": {"min": 150, "max": 300, "median": 220}
    },
    "major_cities": {
        "lyon": {"min": 200, "max": 400, "median": 300},
        "marseille": {"min": 150, "max": 350, "median": 250},
        "bordeaux": {"min": 180, "max": 380, "median": 280},
        "toulouse": {"min": 160, "max": 320, "median": 240}
    }
}