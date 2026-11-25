
#!/bin/bash

BASE="http://127.0.0.1:5000"
COOKIE="cookies.txt"

read_credentials() {
    read -r -p "Kullanici adi: " USERNAME
    read -r -p "E-posta: " EMAIL
    read -r -s -p "Sifre: " PASSWORD
    echo
}

case "$1" in
  register)
    read_credentials

    PAYLOAD=$(python3 -c 'import json,sys; print(json.dumps({"username":sys.argv[1],"email":sys.argv[2],"password":sys.argv[3]}))' \
      "$USERNAME" "$EMAIL" "$PASSWORD")

    curl -i -X POST "$BASE/api/auth/register" \
      -H "Content-Type: application/json" \
      -d "$PAYLOAD"
    ;;

  login)
    read -r -p "Kullanici adi: " USERNAME
    read -r -s -p "Sifre: " PASSWORD
    echo

    PAYLOAD=$(python3 -c 'import json,sys; print(json.dumps({"username":sys.argv[1],"password":sys.argv[2]}))' \
      "$USERNAME" "$PASSWORD")

    curl -i -c "$COOKIE" -X POST "$BASE/api/auth/login" \
      -H "Content-Type: application/json" \
      -d "$PAYLOAD"
    ;;

  me)
    curl -i -b "$COOKIE" "$BASE/api/auth/me"
    ;;

  desks)
    curl -s "$BASE/api/desks/"
    echo
    ;;

  select)
    curl -i -b "$COOKIE" -X POST "$BASE/api/desks/$2/select"
    ;;

  release)
    curl -i -b "$COOKIE" -X POST "$BASE/api/desks/release"
    ;;

  break)
    curl -i -b "$COOKIE" -X POST "$BASE/api/desks/break"
    ;;

  resume)
    curl -i -b "$COOKIE" -X POST "$BASE/api/desks/break/resume"
    ;;

  logout)
    curl -i -b "$COOKIE" -c "$COOKIE" -X POST "$BASE/api/auth/logout"
    ;;

  *)
    echo "Kullanim:"
    echo "./test_lms.sh register"
    echo "./test_lms.sh login"
    echo "./test_lms.sh me"
    echo "./test_lms.sh desks"
    echo "./test_lms.sh select 1"
    echo "./test_lms.sh release"
    echo "./test_lms.sh break"
    echo "./test_lms.sh resume"
    echo "./test_lms.sh logout"
    ;;
esac
