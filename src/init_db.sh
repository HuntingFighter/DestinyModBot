echo "Sleeping 5 seconds"
sleep 5
echo "Starting DB Init"
mysql -u root -h mariadb -pD2Banshee4Ever < /app/init_db.sql;
echo "DB Init completed, starting bot";

python3 -u ./bot.py