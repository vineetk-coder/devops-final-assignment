#!/usr/bin/env bash
# Exercise-10 Step 10: curl tests. Pass the two URLs printed by `minikube service`.
# Usage: bash scripts/curl_tests.sh http://127.0.0.1:35855 http://127.0.0.1:38975
set -euo pipefail
PRODUCT_URL="${1:?product-catalog URL required}"
CART_URL="${2:?shopping-cart URL required}"

echo "GET /products";  curl -s "$PRODUCT_URL/products"; echo
echo "GET /cart";      curl -s "$CART_URL/cart"; echo
echo "POST /cart"
curl -s -X POST "$CART_URL/cart" -H "Content-Type: application/json" \
     -d '{"id": 1, "name": "Laptop", "quantity": 1}'; echo
