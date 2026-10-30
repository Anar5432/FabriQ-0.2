@echo off
title FabriQ Spring Boot ERP Engine (Port 8080)
cd /d "%~dp0"
echo ===================================================
echo Starting FabriQ Spring Boot ERP Engine on Port 8080...
echo ===================================================
"C:\Program Files\Java\jdk-25.0.2\bin\java.exe" -Xms128m -Xmx512m -jar target\erp-0.0.1-SNAPSHOT.jar
pause
