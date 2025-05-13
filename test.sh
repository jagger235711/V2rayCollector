temp_response=$(mktemp)
current_url="http://0.0.0.0:25500/sub?target=mixed&url=https://raw.githubusercontent.com/ts-sf/fly/main/v2"
curl -fs -L -o "$temp_response" "$current_url"