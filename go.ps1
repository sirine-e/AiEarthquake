docker stop ia 2>$null; docker rm ia 2>$null
docker stop app 2>$null; docker rm app 2>$null

Push-Location -Path "ia"
docker build --rm -t ia .
Pop-Location

Push-Location -Path "app"
mvn clean package -DskipTests
docker build --rm -t app .
Pop-Location

Write-Host "Done! Press Enter to exit..." -ForegroundColor Green
Read-Host