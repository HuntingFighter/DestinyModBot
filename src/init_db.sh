if ! test -e ./data/data; then
    echo "Sleeping 30 seconds"
    sleep 30
    echo "Starting DB Init"
    mysql -u root -h mariadb -pPassword < /app/init_db.sql;
    echo "DB Init completed, starting bot";
else
    echo "Sleeping 30 seconds"
    sleep 30
fi

python3 -u ./bot.py
