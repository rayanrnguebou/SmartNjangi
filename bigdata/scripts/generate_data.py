#!/usr/bin/env python3
"""
SmartNjangi - Generateur de donnees simulees realistes
=======================================================

Genere :
- 5000 utilisateurs avec prenoms/noms/villes camerounais
- 200 tontines avec parametres realistes
- Memberships (adhesions des utilisateurs aux tontines)
- ~50 000 paiements avec patterns comportementaux realistes

Sortie : 4 fichiers JSON dans data/simulated/
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# ===========================================================================
# DONNEES DE REFERENCE CAMEROUNAISES
# ===========================================================================

PRENOMS_MASCULINS = [
    "Aboubakar", "Achille", "Alphonse", "Armand", "Boris", "Calvin", "Christian",
    "Dieudonne", "Emmanuel", "Fabrice", "Felix", "Franck", "Gilbert", "Gilles",
    "Hassan", "Ibrahim", "Ismael", "Jean", "Joel", "Junior", "Kevin", "Landry",
    "Lucien", "Marcel", "Martin", "Mathieu", "Mbarga", "Moise", "Narcisse",
    "Nicolas", "Ousmane", "Patrice", "Paul", "Pierre", "Raoul", "Raymond",
    "Richard", "Robert", "Rodrigue", "Roger", "Roland", "Romaric", "Samuel",
    "Serge", "Simon", "Stephane", "Sylvain", "Theophile", "Thierry", "Vincent",
    "Wilfried", "Yannick", "Yves", "Zacharie", "Eric", "Bertrand", "Cyrille",
    "Donald", "Herve", "Olivier", "Pascal", "Steve", "Ulrich"
]

PRENOMS_FEMININS = [
    "Adele", "Agathe", "Aicha", "Alice", "Aline", "Annette", "Aminatou",
    "Beatrice", "Brigitte", "Carine", "Caroline", "Cecile", "Celestine",
    "Chantal", "Christelle", "Christine", "Claire", "Clarisse", "Constance",
    "Delphine", "Dorothee", "Edith", "Elise", "Emilie", "Estelle", "Esther",
    "Fatima", "Florence", "Francine", "Genevieve", "Germaine", "Gisele",
    "Henriette", "Isabelle", "Jacqueline", "Jeanne", "Judith", "Julienne",
    "Justine", "Khadija", "Laetitia", "Laure", "Lucie", "Madeleine",
    "Marguerite", "Marie", "Marlene", "Martine", "Mireille", "Monique",
    "Nadege", "Ngono", "Nicole", "Pascaline", "Pauline", "Perpetue", "Rachel",
    "Rebecca", "Reine", "Rita", "Rosalie", "Solange", "Sophie", "Stella",
    "Sylvie", "Therese", "Veronique", "Viviane", "Yolande", "Audrey", "Diane",
    "Inelda", "Joelle", "Larissa", "Murielle", "Nadine", "Rebecca", "Ruth"
]

NOMS_FAMILLE = [
    "Abanda", "Abega", "Atangana", "Awono", "Ayissi", "Bakari", "Bana", "Belibi",
    "Bell", "Bessala", "Bidias", "Biya", "Bouba", "Diop", "Djoumessi", "Dongmo",
    "Eboa", "Ebode", "Edzimbi", "Eko", "Eloundou", "Ema", "Engo", "Enow",
    "Eteki", "Etoga", "Eyenga", "Fai", "Feudjio", "Fokou", "Fokoua", "Foncha",
    "Fonkou", "Fotso", "Foumane", "Hamadou", "Issa", "Kameni", "Kamga", "Kana",
    "Kandem", "Kemajou", "Kemtchouang", "Kenfack", "Kenmogne", "Kingue", "Kom",
    "Komen", "Kouam", "Lekane", "Mabou", "Manga", "Manguele", "Mbappe", "Mbarga",
    "Mbock", "Mboumegne", "Mendomo", "Menye", "Meta", "Mevoua", "Meyong",
    "Mokom", "Mongo", "Mouafo", "Moudio", "Mpacko", "Muna", "Ndedi", "Ndjock",
    "Ndongo", "Nga", "Ngalle", "Ngassam", "Ngoumou", "Ngwa", "Nguelle", "Njoya",
    "Nkah", "Nkomo", "Nkoulou", "Noumbissi", "Nyemeck", "Onana", "Ondoa",
    "Ondoua", "Onguene", "Otele", "Ouandji", "Owona", "Sambo", "Sani", "Sock",
    "Song", "Soppo", "Tagne", "Talla", "Tamo", "Tchakounte", "Tchoumi",
    "Tedongmo", "Teguia", "Tene", "Tiomela", "Toko", "Tonye", "Tsala", "Tsanga",
    "Wandji", "Yebga", "Yene", "Yong", "Zambo", "Zang", "Zogo"
]

REGIONS_VILLES = {
    "Centre": ["Yaounde", "Mbalmayo", "Obala", "Bafia", "Mfou", "Mbankomo"],
    "Littoral": ["Douala", "Edea", "Nkongsamba", "Loum", "Yabassi", "Mbanga"],
    "Ouest": ["Bafoussam", "Dschang", "Mbouda", "Bandjoun", "Foumban", "Bangangte"],
    "Sud-Ouest": ["Buea", "Limbe", "Tiko", "Kumba", "Mamfe", "Mundemba"],
    "Nord-Ouest": ["Bamenda", "Kumbo", "Wum", "Ndop", "Mbengwi", "Nkambe"],
    "Nord": ["Garoua", "Guider", "Pitoa", "Figuil", "Lagdo", "Poli"],
    "Extreme-Nord": ["Maroua", "Mokolo", "Kousseri", "Yagoua", "Mora", "Kaele"],
    "Adamaoua": ["Ngaoundere", "Tibati", "Meiganga", "Banyo", "Tignere"],
    "Sud": ["Ebolowa", "Kribi", "Sangmelima", "Ambam", "Djoum"],
    "Est": ["Bertoua", "Batouri", "Yokadouma", "Abong-Mbang", "Belabo"]
}

PROFESSIONS = [
    "Commercant", "Commercante", "Agriculteur", "Agricultrice", "Couturier",
    "Couturiere", "Mecanicien", "Taxi-man", "Mototaxi", "Vendeur", "Vendeuse",
    "Enseignant", "Enseignante", "Infirmier", "Infirmiere", "Fonctionnaire",
    "Etudiant", "Etudiante", "Coiffeur", "Coiffeuse", "Restauratrice",
    "Buyam-sellam", "Macon", "Menuisier", "Electricien", "Plombier", "Chauffeur",
    "Cultivateur", "Eleveur", "Pecheur", "Tailleur", "Cordonnier", "Bijoutier",
    "Photographe", "Journaliste", "Secretaire", "Comptable", "Commercial",
    "Technicien", "Boulanger", "Boucher", "Pharmacien", "Banquier"
]

# Prefixes telephoniques MTN et Orange Cameroun
PREFIXES_MTN = ["65", "67", "68"]
PREFIXES_ORANGE = ["69", "65", "66"]
TOUS_PREFIXES = PREFIXES_MTN + PREFIXES_ORANGE

THEMES_TONTINES = [
    "Solidarite", "Amitie", "Avenir", "Espoir", "Reussite", "Union", "Famille",
    "Fraternite", "Confiance", "Prosperite", "Esperance", "Progres", "Force",
    "Lumiere", "Harmonie", "Honneur", "Dignite", "Excellence", "Vision",
    "Patience", "Persiverance", "Foi", "Unite", "Paix", "Reconnaissance"
]


# ===========================================================================
# FONCTIONS DE GENERATION
# ===========================================================================

def generate_phone():
    """Genere un numero camerounais au format +237XXXXXXXXX"""
    prefix = random.choice(TOUS_PREFIXES)
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f"+237{prefix}{suffix}"


def generate_user(user_index):
    """Genere un utilisateur fictif avec un profil de fiabilite cache"""
    sex = random.choice(["M", "F"])
    prenom = random.choice(PRENOMS_MASCULINS if sex == "M" else PRENOMS_FEMININS)
    nom = random.choice(NOMS_FAMILLE)
    region = random.choice(list(REGIONS_VILLES.keys()))
    ville = random.choice(REGIONS_VILLES[region])
    profession = random.choice(PROFESSIONS)

    # Distribution des profils de fiabilite (utilise pour generer payments coherents)
    r = random.random()
    if r < 0.60:
        reliability = "high"          # 60% : tres fiables
    elif r < 0.85:
        reliability = "medium"        # 25% : moyens
    elif r < 0.95:
        reliability = "low"           # 10% : peu fiables
    else:
        reliability = "very_low"      # 5% : problematiques

    # Date de creation (entre 1 et 24 mois)
    days_ago = random.randint(30, 730)
    created_at = datetime.now() - timedelta(days=days_ago)

    return {
        "_id": f"user_{user_index:05d}",
        "phone": generate_phone(),
        "name": f"{prenom} {nom}",
        "sex": sex,
        "city": ville,
        "region": region,
        "profession": profession,
        "createdAt": created_at.isoformat(),
        "_reliability_profile": reliability,  # Champ interne (a retirer en production)
        "isActive": random.random() < 0.95
    }


def generate_tontine(tontine_index, admin_id, region):
    """Genere une tontine avec parametres realistes"""
    # Taille du groupe (elargi pour generer plus de memberships)
    r = random.random()
    if r < 0.15:
        max_members = random.randint(8, 12)      # Petites tontines familiales
    elif r < 0.55:
        max_members = random.randint(13, 25)     # Moyennes (quartier, eglise)
    elif r < 0.90:
        max_members = random.randint(26, 40)     # Grandes (association)
    else:
        max_members = random.randint(41, 60)     # Tres grandes (corporations, marche)

    # Montant par tour (en FCFA)
    r = random.random()
    if r < 0.50:
        amount = random.choice([5000, 10000, 15000, 20000])           # Faibles
    elif r < 0.85:
        amount = random.choice([25000, 50000, 75000, 100000])         # Moyens
    else:
        amount = random.choice([150000, 200000, 300000, 500000])      # Eleves

    # Frequence
    r = random.random()
    if r < 0.30:
        frequency = "weekly"
    elif r < 0.50:
        frequency = "biweekly"
    else:
        frequency = "monthly"

    # Date de demarrage (entre 1 et 12 mois en arriere)
    days_ago = random.randint(30, 365)
    start_date = datetime.now() - timedelta(days=days_ago)

    name = f"Tontine {random.choice(THEMES_TONTINES)} {random.randint(1, 99)}"

    return {
        "_id": f"tontine_{tontine_index:04d}",
        "name": name,
        "adminId": admin_id,
        "amountPerTurn": amount,
        "frequency": frequency,
        "maxMembers": max_members,
        "currentMembers": 0,  # sera mis a jour apres memberships
        "startDate": start_date.isoformat(),
        "status": "active",
        "rules": {
            "selectionMode": random.choice(["fixed_order", "random", "auction"]),
            "latePenalty": random.choice([0, 500, 1000, 2000]),
        },
        "region": random.choice(list(REGIONS_VILLES.keys())),
        "createdAt": start_date.isoformat()
    }


def generate_memberships(users, tontines):
    """Cree les adhesions utilisateurs-tontines de maniere coherente."""
    memberships = []
    membership_id = 0

    for tontine in tontines:
        # Tirer N membres aleatoires (parmi les utilisateurs)
        nb_members = tontine["maxMembers"]
        selected_users = random.sample(users, min(nb_members, len(users)))

        for order, user in enumerate(selected_users, start=1):
            membership_id += 1
            # Date d'adhesion proche du demarrage de la tontine
            tontine_start = datetime.fromisoformat(tontine["startDate"])
            joined_offset = random.randint(0, 14)  # adhesion dans les 2 semaines apres demarrage
            joined_at = tontine_start + timedelta(days=joined_offset)

            memberships.append({
                "_id": f"membership_{membership_id:06d}",
                "tontineId": tontine["_id"],
                "userId": user["_id"],
                "joinedAt": joined_at.isoformat(),
                "orderInRotation": order,
                "hasReceivedTurn": False,  # mis a jour si applicable
                "status": "active"
            })

        # Mettre a jour le nombre de membres de la tontine
        tontine["currentMembers"] = len(selected_users)

    return memberships


def generate_payments(users, tontines, memberships):
    """Genere les paiements avec patterns realistes selon le profil de fiabilite"""
    payments = []
    payment_id = 0

    # Indexer les utilisateurs par ID pour acces rapide
    users_by_id = {u["_id"]: u for u in users}

    # Indexer les memberships par tontine pour iterer
    memberships_by_tontine = {}
    for m in memberships:
        memberships_by_tontine.setdefault(m["tontineId"], []).append(m)

    for tontine in tontines:
        tontine_id = tontine["_id"]
        amount = tontine["amountPerTurn"]
        frequency = tontine["frequency"]
        start_date = datetime.fromisoformat(tontine["startDate"])
        tontine_memberships = memberships_by_tontine.get(tontine_id, [])

        # Determine l'intervalle entre paiements
        if frequency == "weekly":
            interval_days = 7
        elif frequency == "biweekly":
            interval_days = 14
        else:
            interval_days = 30

        # Nombre de cycles ecoules depuis le debut
        days_elapsed = (datetime.now() - start_date).days
        nb_cycles = max(1, days_elapsed // interval_days)

        # Pour chaque cycle, chaque membre doit verser
        for cycle in range(nb_cycles):
            due_date = start_date + timedelta(days=interval_days * (cycle + 1))

            for membership in tontine_memberships:
                user = users_by_id[membership["userId"]]
                reliability = user["_reliability_profile"]
                payment_id += 1

                # Determine le comportement de paiement selon le profil
                r = random.random()
                if reliability == "high":
                    # 95% paye a temps, 4% en retard, 1% manque
                    if r < 0.95:
                        status, delay_days = "paid", random.randint(0, 1)
                    elif r < 0.99:
                        status, delay_days = "late", random.randint(2, 5)
                    else:
                        status, delay_days = "missed", -1

                elif reliability == "medium":
                    # 75% a temps, 20% retard, 5% manque
                    if r < 0.75:
                        status, delay_days = "paid", random.randint(0, 2)
                    elif r < 0.95:
                        status, delay_days = "late", random.randint(3, 10)
                    else:
                        status, delay_days = "missed", -1

                elif reliability == "low":
                    # 50% a temps, 35% retard, 15% manque
                    if r < 0.50:
                        status, delay_days = "paid", random.randint(0, 3)
                    elif r < 0.85:
                        status, delay_days = "late", random.randint(5, 20)
                    else:
                        status, delay_days = "missed", -1

                else:  # very_low
                    # 20% a temps, 30% retard, 50% manque
                    if r < 0.20:
                        status, delay_days = "paid", random.randint(0, 5)
                    elif r < 0.50:
                        status, delay_days = "late", random.randint(7, 30)
                    else:
                        status, delay_days = "missed", -1

                # Construire l'enregistrement de paiement
                if status == "missed":
                    paid_at = None
                else:
                    paid_at = (due_date + timedelta(days=delay_days)).isoformat()

                payment_method = random.choice(["mtn_momo", "orange_money", "mtn_momo", "mtn_momo"])

                payments.append({
                    "_id": f"payment_{payment_id:07d}",
                    "tontineId": tontine_id,
                    "userId": user["_id"],
                    "amount": amount,
                    "dueDate": due_date.isoformat(),
                    "paidAt": paid_at,
                    "status": status,
                    "paymentMethod": payment_method,
                    "transactionRef": f"TXN{payment_id:09d}" if status != "missed" else None,
                    "delayDays": delay_days if status != "missed" else None
                })

    return payments


# ===========================================================================
# EXECUTION PRINCIPALE
# ===========================================================================

def main():
    # Determiner le chemin du projet (script dans bigdata/scripts/)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent
    output_dir = project_root / "data" / "simulated"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("SmartNjangi - Generation de donnees simulees")
    print("=" * 60)
    print(f"Repertoire de sortie : {output_dir}\n")

    # Definir la seed pour reproductibilite
    random.seed(42)

    # --- 1. Generer les utilisateurs ---
    NB_USERS = 60000
    print(f"[1/4] Generation de {NB_USERS} utilisateurs...")
    users = [generate_user(i) for i in range(1, NB_USERS + 1)]
    print(f"      OK - {len(users)} utilisateurs generes")

    # --- 2. Generer les tontines ---
    NB_TONTINES = 1000
    print(f"\n[2/4] Generation de {NB_TONTINES} tontines...")
    tontines = []
    for i in range(1, NB_TONTINES + 1):
        admin = random.choice(users)
        tontines.append(generate_tontine(i, admin["_id"], admin["region"]))
    print(f"      OK - {len(tontines)} tontines generees")

    # --- 3. Generer les memberships ---
    print(f"\n[3/4] Generation des memberships...")
    memberships = generate_memberships(users, tontines)
    print(f"      OK - {len(memberships)} memberships generees")

    # --- 4. Generer les paiements ---
    print(f"\n[4/4] Generation des paiements (peut prendre 30s a 1min)...")
    payments = generate_payments(users, tontines, memberships)
    print(f"      OK - {len(payments)} paiements generes")

    # --- Sauvegarde JSON ---
    print(f"\nSauvegarde dans {output_dir}...")

    with open(output_dir / "users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    with open(output_dir / "tontines.json", "w", encoding="utf-8") as f:
        json.dump(tontines, f, ensure_ascii=False, indent=2)

    with open(output_dir / "memberships.json", "w", encoding="utf-8") as f:
        json.dump(memberships, f, ensure_ascii=False, indent=2)

    with open(output_dir / "payments.json", "w", encoding="utf-8") as f:
        json.dump(payments, f, ensure_ascii=False, indent=2)

    # --- Statistiques finales ---
    print("\n" + "=" * 60)
    print("STATISTIQUES")
    print("=" * 60)

    # Distribution des profils de fiabilite
    profiles = {}
    for u in users:
        p = u["_reliability_profile"]
        profiles[p] = profiles.get(p, 0) + 1
    print(f"\nProfils de fiabilite :")
    for p, n in sorted(profiles.items()):
        print(f"  {p:12s} : {n:5d} ({n/len(users)*100:.1f}%)")

    # Distribution des statuts de paiement
    statuses = {}
    for p in payments:
        s = p["status"]
        statuses[s] = statuses.get(s, 0) + 1
    print(f"\nStatuts de paiement :")
    for s, n in sorted(statuses.items()):
        print(f"  {s:12s} : {n:6d} ({n/len(payments)*100:.1f}%)")

    # Volume financier total
    total_amount = sum(p["amount"] for p in payments if p["status"] != "missed")
    print(f"\nVolume financier brasse (paiements effectues) : {total_amount:,.0f} FCFA")
    print(f"Volume financier moyen par tontine            : {total_amount/len(tontines):,.0f} FCFA")

    print("\n" + "=" * 60)
    print("GENERATION TERMINEE")
    print("=" * 60)
    print(f"\nFichiers crees :")
    for filename in ["users.json", "tontines.json", "memberships.json", "payments.json"]:
        filepath = output_dir / filename
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"  {filename:25s} : {size_mb:.2f} MB")


if __name__ == "__main__":
    main()
