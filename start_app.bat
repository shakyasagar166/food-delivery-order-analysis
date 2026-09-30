@echo off
title QuickBite Food Delivery Analytics - Connected Full Stack
echo ======================================================================
echo    🍔 QUICKBITE FOOD DELIVERY ANALYTICS - FULL STACK APPLICATION
echo ======================================================================
echo 1. Connecting Database (SQLite data/food_delivery.db)...
echo 2. Linking Excel Model (excel/Food_Delivery_Analysis.xlsx)...
echo 3. Starting Python REST API Backend on Port 8000...
echo 4. Launching Frontend at http://localhost:8000 ...
echo ======================================================================

start http://localhost:8000
python server.py

pause
