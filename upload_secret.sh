while IFS='=' read -r line; do
  line=$(echo "$line" | tr -d '[:space:]') # Supprimer les espaces et tabulations
  if [[ ! "$line" =~ ^# ]] && [[ ! -z "$line" ]]; then # Ignorer les lignes vides et commençant par #
    key="${line%%=*}"
    value="${line#*=}"
    gh secret set "$key" <<< "$value"
  fi
done < .env