#!/bin/bash

usage() {
  echo "Usage: $0 -u url -w wordlist -e 'error message'"
  echo "  -u    Base URL (ex: http://site.local/page=)"
  echo "  -w    Wordlist à tester"
  echo "  -e    Message d'erreur à ignorer (ex: 'Not found')"
  echo "  -H    Header à prendre en compte (ex: 'Authorization: Bearer test')"
  exit 1
}

[[ $# -eq 0 ]] && usage

while getopts "u:w:H:e:" opt; do
  case $opt in
    u) URL="$OPTARG" ;;
    w) WORDLIST="$OPTARG" ;;
    e) ERROR_MSG="$OPTARG" ;;
    H) HEADER="$OPTARG" ;;
    *) usage ;;
  esac
done

[[ -z "$URL" || -z "$WORDLIST" || -z "$ERROR_MSG" ]] && usage

clear
LINES=$(tput lines)
toggle=0

COLOR1='\033[38;5;45m'
COLOR2='\033[38;5;201m'
NC='\033[0m'

while read -r path; do
    full_url="${URL}${path}"

    tput cup $((LINES - 1)) 0
    echo -ne "\033[1m\033[38;5;250mTESTING : $path\033[K${NC}"

    if [[ -n "$HEADER" ]]; then
        response=$(curl -s -H "$HEADER" "$full_url")
    else
        response=$(curl -s "$full_url")
    fi

    if [[ ! "$response" =~ $ERROR_MSG && -n "$response" ]]; then
        if [[ $toggle -eq 0 ]]; then
            COLOR="$COLOR1"
            toggle=1
        else
            COLOR="$COLOR2"
            toggle=0
        fi

        echo -e "\n\n${COLOR}┌────────────────────────────────────────────"
        echo "│ [+] Found: $path"
        echo "│ Content:"
        echo "$response" | sed 's/^/│ /'
        echo -e "└────────────────────────────────────────────${NC}"
    fi
done < "$WORDLIST"

tput cup $LINES 0
echo ""
