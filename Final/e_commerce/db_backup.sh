#!/bin/bashs
# Database backup script

BACKUP_DIR="/Users/aisultankhalelov/Desktop/KBTU/KBTU-Backend-Highload/Final/e_commerce/backups/db"
mkdir -p $BACKUP_DIR

pg_dump -U aissultan -F c -b -v -f "$BACKUP_DIR/db_backup_$(date +%F).backup" kbtu_highload_final
