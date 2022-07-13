for ($i = 0; $i -le 15; $i++) {
    Write-Host "Runnig test $i"
    ./PotreeConverter.exe .\testInputs\output_1.las -o C:/xampp/htdocs/potree --generate-page boundedCloud_1
}



