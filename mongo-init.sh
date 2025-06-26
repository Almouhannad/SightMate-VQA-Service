#!/usr/bin/env bash
set -e

# wait-for-mongo (optional, but useful if network startup is slow)
until mongosh --username "$MONGO_INITDB_ROOT_USERNAME" \
              --password "$MONGO_INITDB_ROOT_PASSWORD" \
              --authenticationDatabase admin \
              --eval "db.adminCommand('ping')" &>/dev/null; do
  echo "Waiting for mongosh…"
  sleep 1
done

# create your app user in $MONGO_INITDB_DATABASE
mongosh --username "$MONGO_INITDB_ROOT_USERNAME" \
        --password "$MONGO_INITDB_ROOT_PASSWORD" \
        --authenticationDatabase admin <<EOF
use $MONGO_INITDB_DATABASE;
db.createUser({
  user:   "$MONGO_APP_USERNAME",
  pwd:    "$MONGO_APP_PASSWORD",
  roles: [ { role: "readWrite", db: "$MONGO_INITDB_DATABASE" } ]
});
EOF
