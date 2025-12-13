#!/usr/bin/env bash

BASE_URL="http://localhost:8000"
API_URL="$BASE_URL/api"
AGENT_TOKEN="agent123"
ADMIN_TOKEN="admin123"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'


print_pass() { echo -e "${GREEN}PASS${NC} - $1"; }
print_fail() { echo -e "${RED}FAIL${NC} - $1"; }


echo "======================================"
echo "   EnterpriseLink Backend Smoke Test   "
echo "======================================"


# 1) HEALTH CHECK
resp=$(curl -s "$BASE_URL/health")
if [[ "$resp" == *"status"* ]]; then
    print_pass "Health endpoint"
else
    print_fail "Health endpoint"
fi


# 2) UNAUTHORIZED CUSTOMER ACCESS
resp=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/customers/1")
if [[ "$resp" == "403" ]]; then
    print_pass "Unauthorized access correctly blocked"
else
    print_fail "Unauthorized access not blocked"
fi


## 3) VERIFY SEED DATA EXISTS
echo "Checking seeded customers..."

cust1=$(curl -s -H "Authorization: Bearer $AGENT_TOKEN" "$API_URL/customers/1")
cust2=$(curl -s -H "Authorization: Bearer $AGENT_TOKEN" "$API_URL/customers/2")

if [[ "$cust1" == *"id"* && "$cust2" == *"id"* ]]; then
    print_pass "Seed customers exist (IDs 1 and 2)"
else
    print_fail "Seed customers missing — expected customers (1, 2)"
    exit 1
fi


# 4) AUTHORIZED CUSTOMER ACCESS
resp=$(curl -s -H "Authorization: Bearer $AGENT_TOKEN" "$API_URL/customers/1")
if [[ "$resp" == *"Jane Doe"* ]]; then
    print_pass "Fetch customer #1"
else
    print_fail "Fetch customer #1"
fi


# 5) CREATE TICKET
ticket_resp=$(curl -s -X POST "$API_URL/tickets/" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"subject":"Laptop not booting","description":"System does not start."}')

if [[ "$ticket_resp" == *"Laptop not booting"* ]]; then
    print_pass "Create ticket"
else
    print_fail "Create ticket"
fi


# Extract new ticket ID
ticket_id=$(echo "$ticket_resp" | grep -o '"id":[0-9]*' | cut -d':' -f2)

if [[ -z "$ticket_id" ]]; then
    print_fail "Could not extract ticket ID"
else
    echo "   → Ticket ID: $ticket_id"
    print_pass "Extracted ticket ID"
fi


# 6) LIST TICKETS
resp=$(curl -s "$API_URL/tickets/")
if [[ "$resp" == *"Laptop not booting"* ]]; then
    print_pass "List tickets"
else
    print_fail "List tickets"
fi


# 7) UPDATE TICKET STATUS
resp=$(curl -s -X PATCH "$API_URL/tickets/$ticket_id" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"in_progress"}')

if [[ "$resp" == *"in_progress"* ]]; then
    print_pass "Update ticket status"
else
    print_fail "Update ticket status"
fi


# 8) ADD NOTE
resp=$(curl -s -X POST "$API_URL/notes/$ticket_id" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"Customer provided additional info."}')

if [[ "$resp" == *"additional info"* ]]; then
    print_pass "Add note to ticket"
else
    print_fail "Add note to ticket"
fi


# 9) ADD NOTE WITHOUT AUTH → expected 403
resp=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "$API_URL/notes/$ticket_id" \
  -H "Content-Type: application/json" \
  -d '{"text":"Unauthorized attempt"}')

if [[ "$resp" == "403" ]]; then
    print_pass "Unauthorized note blocked"
else
    print_fail "Unauthorized note allowed"
fi

echo ""
echo "======================================"
echo "      Smoke Test Completed"
echo "======================================"
