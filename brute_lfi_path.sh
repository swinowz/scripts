#!/bin/bash

usage() {
  echo "Usage: $0 -u url -w wordlist -e 'error message'"
  echo "  -u    Base URL (ex: http://site.local/page=)"
  echo "  -w    Wordlist à tester"
  echo "  -e    Message d'erreur à ignorer (ex: 'Not found')"
  exit 1
}

[[ $# -eq 0 ]] && usage

while getopts "u:w:e:" opt; do
  case $opt in
    u) URL="$OPTARG" ;;
    w) WORDLIST="$OPTARG" ;;
    e) ERROR_MSG="$OPTARG" ;;
    *) usage ;;
  esac
done

[[ -z "$URL" || -z "$WORDLIST" || -z "$ERROR_MSG" ]] && usage

clear
LINES=$(tput lines)
toggle=0

# Arsenal-style colors
COLOR1='\033[38;5;45m'   # Cyan flashy
COLOR2='\033[38;5;201m'  # Magenta clair
NC='\033[0m'

while read -r path; do
    full_url="${URL}${path}"

    # TESTING info en bas
    tput cup $((LINES - 1)) 0
    echo -ne "\033[1m\033[38;5;250mTESTING : $path\033[K${NC}"

    response=$(curl -s "$full_url")

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

# Curseur propre à la fin
tput cup $LINES 0
echo ""
