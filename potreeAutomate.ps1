for ($i = 0; $i -le 26; $i++) {
    $number = $i.ToString()
    Write-Host "Runnig test $i"
    ./PotreeConverter.exe ".\testInputs\output_1"+ $number + ".las" -o C:/xampp/htdocs/potree --generate-page ("boundedCloud_1_" + $number) 
}
for ($i = 0; $i -le 26; $i++) {
    $number = $i.ToString()
    Write-Host "Runnig test $i"
    ./PotreeConverter.exe ".\testInputs\output_2" + $number + ".las" -o C:/xampp/htdocs/potree --generate-page ("boundedCloud_2_" + $number)
}
for ($i = 0; $i -le 26; $i++) {
    Write-Host "Runnig test $i"
    $number = $i.ToString()
    ./PotreeConverter.exe ".\testInputs\output_3" + $number + ".las" -o C:/xampp/htdocs/potree --generate-page ("boundedCloud_3_" + $number)
}



