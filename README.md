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

<img width="1438" height="1350" alt="image" src="https://github.com/user-attachments/assets/bdfcbdc0-68c6-4aa9-ab24-0fd1e9291e36" />

### 2. Installer les dépendances

```bash
pip install boto3 awscli-local awscli
```

### 3. Déployer l'infrastructure

```bash
python deploy.py
```

Ce script crée automatiquement :
- Une instance EC2 (simulée)
- Une fonction Lambda `ec2-controller`
- Une API Gateway avec la route `/ec2`


Vérification Instance EC2 : 

<img width="1610" height="276" alt="image" src="https://github.com/user-attachments/assets/93171dd2-408b-47ad-82c7-0809ca4b2b0d" />

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

<img width="1726" height="362" alt="image" src="https://github.com/user-attachments/assets/582d76e3-590d-4b91-b033-46752946df77" />

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

<img width="2122" height="68" alt="image" src="https://github.com/user-attachments/assets/17e39b96-b690-46c3-a37f-55c5caf3cfaa" />

---

## Auteur

Andy Piquionne — EFREI Paris — MSc Cybersécurité & Management
