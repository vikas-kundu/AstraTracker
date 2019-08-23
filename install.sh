clear
echo "******* AstraTracker install in Progress ********"
echo ""
echo "=====> Installing BS4 "
sudo apt install python-bs4 
echo "=====> Installing Mechanize "
sudo apt install python-mechanize 
echo "=====> Installing Astra Tracker "
sudo cp AstraTracker /usr/bin/AstraTracker
sudo chmod +x /usr/bin/AstraTracker
echo "=====> Done "
