for ($i = 0; $i -le 15; $i++) {
    Write-Host "Runnig test $i"
    ./PotreeConverter.exe .\testInputs\output_1.las -o C:/xampp/htdocs/potree --generate-page boundedCloud_1
}



​```​​
from computeclouds import ComputeClouds
​X_glob =  503455.626160 ​
​Y_glob =  4918094.496948
Z_glob =  720.263306
X_delta = 100
Y_delta = 100
Z_delta = 100
bounding_box_list=[X_glob - X_delta, X_glob + X_delta, Y_glob - Y_delta, Y_glob + Y_delta, Z_glob - Z_delta, Z_glob + Z_delta]
​​path_to_constrained_1 = ComputeClouds.constrainCloud(path_to_cloud=path_to_file_original_1, bounding_box_list=bounding_box_list, path_to_output_cloud=path_to_output_cloud_1)
path_to_constrained_2 = ComputeClouds.constrainCloud(path_to_cloud=path_to_file_original_2, bounding_box_list=bounding_box_list, path_to_output_cloud=path_to_output_cloud_2)​
​ComputeClouds.calcM3C2(
    firstCd=path_to_constrained_1,
    secondCd=path_to_constrained_2,
    parametersConfigFilePath=path_to_params_file,
    nameOfFileOutput=nameOfFileOutput, verbose=False
)
​```