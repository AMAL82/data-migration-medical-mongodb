Write-Host "==== Étape 1 : Nettoyage des données ===="
docker-compose run --rm migration python ./script/data_cleaning.py
if ($LASTEXITCODE -ne 0) { Write-Host "Erreur lors du nettoyage des données." -ForegroundColor Red; exit 1 }

Write-Host "==== Étape 2 : Migration vers MongoDB ===="
docker-compose run --rm migration python ./script/migration.py
if ($LASTEXITCODE -ne 0) { Write-Host "Erreur lors de la migration des données." -ForegroundColor Red; exit 1 }

Write-Host "==== Étape 3 : Test post-migration ===="
docker-compose run --rm migration python ./script/test_post_migration.py
if ($LASTEXITCODE -ne 0) { Write-Host "Erreur lors du test post-migration." -ForegroundColor Red; exit 1 }

Write-Host "Migration complétée avec succès !" -ForegroundColor Green