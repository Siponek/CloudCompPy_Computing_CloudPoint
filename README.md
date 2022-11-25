<!-- [![Total Downloads](https://poser.pugx.org/aimeos/aimeos-typo3/d/total.svg)](https://packagist.org/packages/aimeos/aimeos-typo3) -->
<!-- [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/aimeos/aimeos-typo3/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/aimeos/aimeos-typo3/?branch=master) -->
<!-- [![License](https://poser.pugx.org/aimeos/aimeos-typo3/license.svg)](https://packagist.org/packages/aimeos/aimeos-typo3) -->

# CloudCompPy_Computing-CloudPoint
Main API that is needed is inside __computeclouds/ComputeClouds.py__, rest of the files are to testing other funtionalities of CloudComPy.

Mini project for computing distances/differences between two point clouds using CloudComapre API.

## Usage
Import the ComputeClouds.py into your project [You might want to use sys.append({your_path}) if having problems with proejct structure] 

You can view the results through Potree using apache webserver from XAMPP or using CloudCompare.

As for today CloudComPy has implemented __guessParams__ option for its API, but if you want to make multiple passes for M3C2 plugin (of CloudCompare, present in CloudComPy API) to see which (M3C2)parameters are best for your configuration you can use Potree to visualise these changes. For Potree you can use __PotreeAutomate.ps1__ inside of __additional_testing_scripts(mess)__ if you are dealing with multiple passes of M3C2 plugin of CloudCompare. Place it inside potree folder and check the file paths to automate generating the pages for you.

### Requirements

- Anaconda environment prepared for Win10 option from project of CloudCompy39
<a href="https://github.com/CloudCompare/CloudComPy/blob/master/doc/UseWindowsCondaBinary.md">(CloudCompare for python)</a>

- Laspy
