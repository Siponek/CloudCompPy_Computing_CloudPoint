for ($i = 0; $i -le 30; $i++) {
    $number = $i.ToString()
    Write-Host "        Runnig test 1 $i"
    Write-Host ("       \testInputs\output_1_" + $number + ".las")
    Write-Host ("       boundedCloud_1_" + $number)
    $path_to_las = "testInputs\output_1_" + $number + ".las"
    $name_boundedcloud = "boundedCloud_1_" + $number
    Start-Process -FilePath ./PotreeConverter.exe -ArgumentList "$path_to_las -o C:/xampp/htdocs/potree --generate-page $name_boundedcloud"
    

    # ./PotreeConverter.exe ("\testInputs\output_1_" + $number + ".las") -o C:/xampp/htdocs/potree --generate-page ("boundedCloud_1_" + $number)
}
for ($i = 0; $i -le 30; $i++) {
    $number = $i.ToString()
    Write-Host "        Runnig test 2 $i"
    Write-Host ("       \testInputs\output_2_" + $number + ".las")
    Write-Host ("       boundedCloud_2_" + $number)
    $path_to_las = "testInputs\output_2_" + $number + ".las"
    $name_boundedcloud = "boundedCloud_2_" + $number
    Start-Process -FilePath ./PotreeConverter.exe -ArgumentList "$path_to_las -o C:/xampp/htdocs/potree --generate-page $name_boundedcloud"

    # ./PotreeConverter.exe ("\testInputs\output_2_" + $number + ".las") -o C:/xampp/htdocs/potree --generate-page ("boundedCloud_2_" + $number)
}
for ($i = 0; $i -le 30; $i++) {
    $number = $i.ToString()
    Write-Host "        Runnig test 3 $i"
    Write-Host ("       \testInputs\output_3_" + $number + ".las")
    Write-Host ("       boundedCloud_3_" + $number)
    $path_to_las = "testInputs\output_3_" + $number + ".las"
    $name_boundedcloud = "boundedCloud_3_" + $number
    Start-Process -FilePath ./PotreeConverter.exe -ArgumentList "$path_to_las -o C:/xampp/htdocs/potree --generate-page $name_boundedcloud"

    # ./PotreeConverter.exe ("\testInputs\output_3_" + $number + ".las") -o C:/xampp/htdocs/potree --generate-page ("boundedCloud_3_" + $number)
}

# .\PotreeConverter.exe \testInputs\output_1_ -o C:/xampp/htdocs/potree --generate-page "boundedCloud_1_1"

