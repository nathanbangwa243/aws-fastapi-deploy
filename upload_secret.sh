# while IFS='=' read -r line; do
#   line=$(echo "$line" | tr -d '[:space:]') # Supprimer les espaces et tabulations
#   if [[ ! "$line" =~ ^# ]] && [[ ! -z "$line" ]]; then # Ignorer les lignes vides et commençant par #
#     key="${line%%=*}"
#     value="${line#*=}"
#     gh secret set "$key" <<< "$value"
#   fi
# done < .env

#!/bin/bash

# Nom de l'environnement
ENVIRONMENT_NAME="production"

# Créer l'environnement s'il n'existe pas déjà
if ! gh environment list | grep -q "$ENVIRONMENT_NAME"; then
  gh environment create "$ENVIRONMENT_NAME" --description "Environnement de production"
fi

# Charger les clés depuis le fichier .env
while IFS='=' read -r line; do
  line=$(echo "$line" | tr -d '[:space:]') # Supprimer les espaces et tabulations
  if [[ ! "$line" =~ ^# ]] && [[ ! -z "$line" ]]; then # Ignorer les lignes vides et commençant par #
    key="${line%%=*}"
    value="${line#*=}"
    gh secret set "$key" --env "$ENVIRONMENT_NAME" <<< "$value"
  fi
done < .env