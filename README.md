# API-Driven — Pilotage EC2 via API Gateway + Lambda (LocalStack)

## Architecture
HTTP Request → API Gateway → Lambda → EC2 (LocalStack)

Une requête HTTP déclenche via API Gateway une fonction Lambda qui démarre, stoppe ou consulte l'état d'une instance EC2 simulée dans LocalStack.

---

## Prérequis

- GitHub Codespaces
- Compte LocalStack : https://app.localstack.cloud/
- Python 3.11+

---

## Installation

### 1. Lancer LocalStack

```bash
localstack auth set-token <YOUR_TOKEN>
localstack start -d
localstack status services
```

> 📸 **Capture 1 — LocalStack services disponibles** (`localstack status services` avec tous les ✔)

### 2. Installer les dépendances

```bash
pip install boto3 awscli-local awscli
```

### 3. Déployer l'infrastructure

```bash
python deploy.py
```

> 📸 **Capture 2 — Résultat de `python deploy.py`** (Instance ID + API URL affichés)

Ce script crée automatiquement :
- Une instance EC2 (simulée)
- Une fonction Lambda `ec2-controller`
- Une API Gateway avec la route `/ec2`

---

## Utilisation

```bash
python3 -c "
import boto3, json
lmb = boto3.client('lambda', region_name='us-east-1',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test', aws_secret_access_key='test')

# Status
r = lmb.invoke(FunctionName='ec2-controller',
    Payload=json.dumps({'action': 'status', 'instance_id': '<INSTANCE_ID>'}))
print(r['Payload'].read().decode())
"
```

> 📸 **Capture 3 — Résultat des 3 actions : STOP / STATUS / START**

---

## Structure du projet
├── deploy.py          # Script de déploiement complet
├── lambda/
│   └── handler.py     # Fonction Lambda (start/stop/status EC2)
├── requirements.txt
└── README.md

---

## Résultats attendus

| Action | Réponse |
|--------|---------|
| status | `{"statusCode": 200, "body": "i-xxx : running"}` |
| stop   | `{"statusCode": 200, "body": "stopped i-xxx"}` |
| start  | `{"statusCode": 200, "body": "started i-xxx"}` |

> 📸 **Capture 4 — Port 4566 public dans l'onglet PORTS de Codespace**

---

## Auteur

Andy Piquionne — EFREI Paris — MSc Cybersécurité & Management
