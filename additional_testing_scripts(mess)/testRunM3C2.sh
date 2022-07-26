#!/bin/bash -e

# Run script.py
# python M3C2_CloudComparison.py -firstCloudPath .\\CloudCompPy_Computing-CloudPoint\\dataFolder\\pythonScri 
python -u ./M3C2_CloudComparison -firstCloudPath ./CloudCompPy_Computing-CloudPoint/dataFolder/pythonScripts_testInputs/testSphere_1 -secondCloudPath ./CloudCompPy_Computing-CloudPoint/dataFolder/pythonScripts_testInputs/testSphere_2


python ./M3C2_CloudComparison.py -firstCd /dataFolder/pythonScripts_testInputs/myCloud_1.txt -secondCd /dataFolder/pythonScripts_testInputs/myCloud_2.txt --nameOfFileOutput myCloud_local_test.las --parametersConfigFilePath /dataFolder/PythonParameters/m3c2_params.txt