import os
import math

# import argparse
import numpy as np
import laspy
import tqdm
from pathlib import Path
import cloudComPy as cc
from gendata import getSampleCloud, dataDir
from multiprocessing import cpu_count

from time import perf_counter, localtime, time
import datetime

# import logging

print("ComputeClouds_> Main : Libs loaded")

### TODO : Clear the code below
### TODO : Keep the cohesion of the code


def prRed(skk):
    print("\033[91m {}\033[00m".format(skk))


def prGreen(skk):
    print("\033[92m {}\033[00m".format(skk))


def prYellow(skk):
    print("\033[93m {}\033[00m".format(skk))


def prLightPurple(skk):
    print("\033[94m {}\033[00m".format(skk))


def prPurple(skk):
    print("\033[95m {}\033[00m".format(skk))


def prCyan(skk):
    print("\033[96m {}\033[00m".format(skk))


def prLightGray(skk):
    print("\033[97m {}\033[00m".format(skk))


def prBlack(skk):
    print("\033[98m {}\033[00m".format(skk))


def convertLasTxt(
    pathToFile: str, nameOfFileOutput: str = "myCloud.txt"
) -> list:
    """convertLasTxt Converts .las file to .txt file for reading with cloudComPy.
    Note: it uses tqdm to show the progress of the conversion.

    Parameters
    ----------
    pathToFile : str
        _description_
    """
    listCoord_XYZ = np.empty([1, 3])
    tmpList = []
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    # limit : int = 0
    #! remark - path 2 has a lot of points, so it takes a while to read it (76_568_359 to be exact).
    with tqdm.tqdm(total=Path(pathToFile).stat().st_size) as pbar:
        with laspy.open(source=pathToFile) as cloudFileHeader:
            if type(cloudFileHeader) != None:
                cloudFile = laspy.read(source=pathToFile)
                try:
                    print("Cloud loaded")
                    print(f"cloud name:{cloudFile.header}")
                except Exception as e:
                    print(e)
                    print(f"cloud name:<unknown>")

            # ? It seems that chunk_iterator helps to read data in batches. In every batch it reads the data and then it moves to the next batch.
            # ? Points.array is in fact a one point array. if we set chunk_iterator to (1)
            # ? What is the data inside of the point? It must be x,y,z and something else. It is possible to extract x,y,z from the point. Is it enough data?
            for points in cloudFileHeader.chunk_iterator(1):
                # print("points.array[0]['X'], points.array[0]['Y'], points.array[0]['Z']", points.x, points.y, points.array[0]['Z'])
                # print("Compare the values", points.x[0] == points.array[0]['X'])
                # print("Compare the values", points.x[0],  points.array[0]['X'])

                # x,y,z = points.array[0]['X'], points.array[0]['Y'], points.array[0]['Z']
                x, y, z = points.x[0], points.y[0], points.z[0]

                # valuesToAppend = np.array([[x,y,z]])
                valuesToAppend = [x, y, z]
                tmpList.append(valuesToAppend)
                # listCoord_XYZ = np.concatenate((listCoord_XYZ, valuesToAppend), axis=0)
                # np.append(arr = listCoord_XYZ, values= valuesToAppend , axis=0)
                pbar.update(n=1)
                # if limit == 20:
                #     break
                # limit +=1
            listCoord_XYZ = np.array(tmpList)
            pbar.close()
            print("Shape of the array:", listCoord_XYZ.shape)
            np.savetxt(
                nameOfFileOutput,
                listCoord_XYZ,
                delimiter=" ",
                newline="\n",
            )
            print(f"convertLasTxt _> File {nameOfFileOutput} saved")
    print("convertLasTxt _> Conversion finished")
    return listCoord_XYZ


def createShpereFull(
    number: int,
    center: list,
    radius: float,
    cutTheShape: bool = True,
) -> list:
    """createShpereFull It generates sphere point cloud (and points inside the volume) with a given center and radius.

    Parameters
    ----------
    number : int
        _description_
    center : list
        _description_
    radius : float
        _description_
    cutTheShape : bool, optional
        _description_, by default True

    Returns
    -------
    list
        _description_
    """
    # generate the random quantities
    phi = np.random.uniform(0, 2 * np.pi, size=(number,))
    theta_cos = np.random.uniform(-1, 1, size=(number,))
    u = np.random.uniform(0, 1, size=(number,))

    # calculate sin(theta) from cos(theta)
    theta_sin = np.sqrt(1 - theta_cos**2)
    r = radius * np.cbrt(u)

    # use list comprehension to generate the coordinate array without a loop
    # don't forget to offset by the atom's position (center)
    return np.array(
        [
            np.array(
                [
                    center[0] + r[i] * theta_sin[i] * np.cos(phi[i]),
                    center[1] + r[i] * theta_sin[i] * np.sin(phi[i]),
                    center[2] + r[i] * theta_cos[i],
                ]
            )
            for i in range(number)
        ]
    )


def createSpherePoints(
    radius: float = 5,
    number: int = 10,
    center: list = [0, 0, 0],
    cutTheShape: str = "None",
    leftTreshold: float = 1,
    rightTreshold: float = 1,
) -> list:
    """createSpherePoints It generates sphere point cloud with points only on its surface with a given center and radius.

    Parameters
    ----------
    radius : float, optional
        _description_, by default 5
    number : int, optional
        _description_, by default 10
    center : list, optional
        _description_, by default [0,0,0]
    cutTheShape : str, optional
        _description_, Cut the shape of the sphere according to GLOBAL coordinates. Values = "None", "Left", "Right" by default "None"
    leftTreshold : float, optional
        _description_, by default 1
    rightTreshold : float, optional
        _description_, by default 1

    Returns
    -------
    list
        _description_
    """
    pi = math.pi
    sin = math.sin
    cos = math.cos
    lst = []
    for phi in [(pi * i) / (number - 1) for i in range(number)]:
        M = int(sin(phi) * (number - 1)) + 1
        for theta in [(2 * pi * i) / M for i in range(M)]:
            x = center[0] + radius * sin(phi) * cos(theta)
            y = center[1] + radius * sin(phi) * sin(theta)
            z = center[2] + radius * cos(phi)
            if cutTheShape == "left" and z <= leftTreshold:
                continue

            elif cutTheShape == "right" and z >= rightTreshold:
                continue

            else:
                lst.append((x, y, z))

    return np.array(lst)


def createSampleCloud(
    frequency1: float = 1.0, frequency2: float = 2.0
) -> str:
    """createSampleCloud It generates a two sample point clouds. Looks like a teardrop hitting the water.

    Returns
    -------
    str
        two paths to point clouds, two strings in total
    """
    return getSampleCloud(frequency1), getSampleCloud(frequency2)


def writeParamsFile(
    parametersConfigFilePath: str = "m3c2_params_custom.txt",
    threadsNum: int = 10,
    scaleResolution: float = 1.0,
    verbose: bool = False,
) -> str:
    """writeParamsFile Create a file with parameters for the simulation and return the path to the file.

    Parameters
    ----------
    parametersConfigFilePath : str, optional
        _description_, by default "m3c2_params_custom.txt"
    threadsNum : int, optional
        Threads for multithreading by C++ (bypasses GIL of python), by default 10
    scaleResolution : float, optional
        Experimental, scaling up the parameters according to format of point clouds, by default 1.0

    Returns
    -------
    str
        path to the params file
    """
    if verbose:
        timeStart = perf_counter()
    assert threadsNum > 0, "threads must be greater than 0"
    assert (
        threadsNum <= cpu_count()
    ), "threads must be less than max number of threads on given pc"
    prYellow("writeParamsFile _> threadsNum: %d" % threadsNum)

    m3c2_params_dic = {}
    m3c2_params_dic["ExportDensityAtProjScale"] = "false"
    m3c2_params_dic["ExportStdDevInfo"] = "false"
    m3c2_params_dic["M3C2VER"] = 1
    m3c2_params_dic["MaxThreadCount"] = threadsNum
    m3c2_params_dic["MinPoints4Stat"] = 5
    m3c2_params_dic["NormalMaxScale"] = 41500 * scaleResolution
    m3c2_params_dic["NormalMinScale"] = 10300.25 * scaleResolution
    m3c2_params_dic["NormalMode"] = 0
    m3c2_params_dic["NormalPreferedOri"] = 4
    m3c2_params_dic["NormalScale"] = 20000 * scaleResolution
    m3c2_params_dic["NormalStep"] = 10397.25 * scaleResolution
    m3c2_params_dic["NormalUseCorePoints"] = "false"
    m3c2_params_dic["PM1Scale"] = 1
    m3c2_params_dic["PM2Scale"] = 1
    m3c2_params_dic["PositiveSearchOnly"] = "false"
    m3c2_params_dic["ProjDestIndex"] = 1
    m3c2_params_dic["RegistrationError"] = 0
    m3c2_params_dic["RegistrationErrorEnabled"] = "false"
    m3c2_params_dic["SearchDepth"] = 370000.125 * scaleResolution
    m3c2_params_dic["SearchScale"] = 10300.25 * scaleResolution
    m3c2_params_dic["SubsampleEnabled"] = "true"
    m3c2_params_dic["SubsampleRadius"] = 5000.625 * scaleResolution
    m3c2_params_dic["UseMedian"] = "false"
    m3c2_params_dic["UseMinPoints4Stat"] = "false"
    m3c2_params_dic["UseOriginalCloud"] = "false"
    m3c2_params_dic["UsePrecisionMaps"] = "false"
    m3c2_params_dic["UseSinglePass4Depth"] = "false"
    paramFilename = os.path.join(
        os.path.abspath("")
        + "\dataFolder\PythonParameters\%s"
        % parametersConfigFilePath
    )
    print(f"Writing parameters to {paramFilename}")
    with open(paramFilename, "w") as f:
        f.write("[General]\n")
        for k, v in m3c2_params_dic.items():
            f.write("%s=%s\n" % (k, v))
        assert os.path.isfile(paramFilename), "File does not exist"
        if verbose:
            timeEnd = perf_counter()
            prPurple(
                "writeParamsFile _> time: %.2f"
                % (timeEnd - timeStart)
            )
        return paramFilename


def overwrite_parameters(path_to_params_file, parameters_dic):
    with open(path_to_params_file, "w") as f:
        f.write("[General]\n")
        for key, value in parameters_dic.items():
            f.write("%s=%s\n" % (key, value))
    return path_to_params_file


def calcM3C2(
    firstCd: str,
    secondCd: str,
    includeTimestamp: bool = False,
    nameOfFileOutput: str = "M3C2.las",
    parametersConfigFilePath: str = "m3c2_params.txt",
    alignICP: bool = False,
    ICP_max_iterations: int = 40,
    debugTest: bool = False,
    verbose: bool = False,
) -> None:
    """calcM3C2 _summary_

    Parameters
    ----------
    firstCd : str
        _description_
    secondCd : str
        _description_
    includeTimestamp : bool, optional
    Includes timestamp in the name of the file. If true then also saves the file as .las format, by default False
        , by default False
    nameOfFileOutput : str, optional
        _description_, by default "M3C2.las"
    parametersConfigFilePath : str, optional
        _description_, by default "m3c2_params.txt"
    alignICP : bool, optional
        _description_, by default True
    ICP_max_iterations : int, optional
        _description_, by default 40
    debugTest : bool, optional
        _description_, by default False
    verbose : bool, optional
        Additional debug info. Prints out task time, by default False

    Raises
    ------
    RuntimeError
        _description_
    RuntimeError
        _description_
    RuntimeError
        _description_
    RuntimeError
        _description_
    """
    if verbose:
        timeStartTask = perf_counter()
    paramFilePath = parametersConfigFilePath
    path1 = firstCd
    path2 = secondCd

    """
    assert os.path.isfile(
        path1
    ), "First cloud file does not exist. Check the path."
    assert os.path.isfile(
        path2
    ), "Second cloud file does not exist. Check the path."
    """
    prYellow("parametersConfigFilePath _>")
    prYellow(os.path.abspath(parametersConfigFilePath))
    # print(os.path.abspath(parametersConfigFilePath) + parametersConfigFilePath )

    assert os.path.isfile(
        paramFilePath
    ), "Parameters file does not exist. Check the path."

    prGreen("Paths are correct")

    # gen.createSymbolicLinks() # required for tests on build, before cc.initCC.init
    cc.initCC()
    prCyan("Loading clouds into CloudComPy...")
    # * uncomment for generic point clouds test.
    #! Remember that depending on cloud there has to be a good params file for it!
    cloud1 = cc.loadPointCloud(path1)
    cloud2 = cc.loadPointCloud(path2)

    prGreen("Loading finished")
    # cloud1.setName("cloud1")
    # cloud2.setName("cloud2")
    if verbose:
        timeStartICP = perf_counter()
    if alignICP:
        prCyan("Aligning clouds using ICP...")
        res = cc.ICP(
            data=cloud2,
            model=cloud1,
            minRMSDecrease=1.0e-5,
            randomSamplingLimit=50000,
            maxIterationCount=ICP_max_iterations,
            removeFarthestPoints=False,
            method=cc.CONVERGENCE_TYPE.MAX_ERROR_CONVERGENCE,
            adjustScale=False,
            finalOverlapRatio=0.90,
            maxThreadCount=0,
        )
        tr2 = res.transMat
        cloud2ICP = res.aligned
        cloud2ICP.applyRigidTransformation(tr2)
        cloud2ICP.setName("cloud2_transformed_afterICP")
        prGreen("Alignment finished")
        cloud2 = cloud2ICP
        if verbose:
            timeEndICP = perf_counter()
            prPurple(
                "ICP time: %.2f" % (timeEndICP - timeStartICP)
            )  # timeEndICP - timeStartICP

    #! Reading parameters form ready file for now

    prYellow("Reading params from %s" % paramFilePath)
    if verbose:
        timeStartM3C2 = perf_counter()
    prCyan("Searching for M3C2 plugin in enviroment...")
    if cc.isPluginM3C2():
        ###* this is actually necesary for the plugin to work
        import cloudComPy.M3C2

        if debugTest is False:
            prGreen("M3C2 plugin is loaded, attempting to run M3C2")
            CloudAfterM3C2 = cc.M3C2.computeM3C2(
                [cloud1, cloud2], paramFilePath
            )
            prGreen("M3C2 plugin work finished")
            if CloudAfterM3C2 is None:
                raise RuntimeError
            if CloudAfterM3C2.getNumberOfScalarFields() < 3:
                raise RuntimeError
            dic = CloudAfterM3C2.getScalarFieldDic()
            sf = CloudAfterM3C2.getScalarField(dic["M3C2 distance"])
            if sf is None:
                raise RuntimeError
            if verbose:
                timeEndM3C2 = perf_counter()
                prPurple(
                    "M3C2 time: %.2f" % (timeEndM3C2 - timeStartM3C2)
                )  # timeEndICP - timeStartICP

        # if not math.isclose(sf.getMax(), 0.71, rel_tol=0.01):
        #     raise RuntimeError
        # if not math.isclose(sf.getMin(), -0.70, rel_tol=0.01):
        #     raise RuntimeError

        if includeTimestamp:
            current_time = time()
            # print("The current time is : ", current_time)
            date_time_format = datetime.date.fromtimestamp(
                current_time
            )
            prCyan("The data is : %s" % (str(date_time_format)))
            nameOfFileOutput = (
                nameOfFileOutput.split(".")[0]
                + "_"
                + str(date_time_format)
                + ".las"
            )
            pathToSaveOutput = os.path.abspath(nameOfFileOutput)
        else:
            pathToSaveOutput = os.path.abspath(nameOfFileOutput)
        print(f"Saving results to {pathToSaveOutput}")
        try:
            cc.SavePointCloud(CloudAfterM3C2, pathToSaveOutput)  # OK
            assert os.path.isfile(
                pathToSaveOutput
            ), "Error, File not saved. Ignore if debugTest is True"
        except UnboundLocalError:
            prRed(
                "No cloud is being returned from M3C2 and no cloud is being saved!"
            )
        prGreen("Job finished")
    else:
        prRed(
            "M3C2 plugin is not loaded, please check the installation"
        )
        raise RuntimeError
    if verbose:
        timeEndTask = perf_counter()
        prPurple(
            "Total time: %.2f" % (timeEndTask - timeStartTask)
        )  # timeEndICP - timeStartICP


def boundingBox(cloud):
    """
    Calculates the bounding box of a cloud. TODO test

    Parameters
    ----------
    cloud : CloudComPy.Cloud
        Cloud to calculate the bounding box of.

    Returns
    -------
    CloudComPy.Cloud
        Bounding box of the cloud. This is a CloudComPy object and not a filtered cloud.
    """
    minX = cloud.getMinX()
    minY = cloud.getMinY()
    minZ = cloud.getMinZ()
    maxX = cloud.getMaxX()
    maxY = cloud.getMaxY()
    maxZ = cloud.getMaxZ()
    boundingBox = cc.Cloud(
        name="boundingBox",
        pointCount=8,
        pointAttributes=cc.PointAttributes(
            attributes=[
                cc.PointAttribute(
                    name="x",
                    type=cc.PointAttributeType.FLOAT,
                    count=1,
                    offset=0,
                ),
                cc.PointAttribute(
                    name="y",
                    type=cc.PointAttributeType.FLOAT,
                    count=1,
                    offset=4,
                ),
                cc.PointAttribute(
                    name="z",
                    type=cc.PointAttributeType.FLOAT,
                    count=1,
                    offset=8,
                ),
            ]
        ),
    )
    boundingBox.setPoint(0, minX, minY, minZ)
    boundingBox.setPoint(1, minX, minY, maxZ)
    boundingBox.setPoint(2, minX, maxY, minZ)
    boundingBox.setPoint(3, minX, maxY, maxZ)
    boundingBox.setPoint(4, maxX, minY, minZ)
    boundingBox.setPoint(5, maxX, minY, maxZ)
    boundingBox.setPoint(6, maxX, maxY, minZ)
    boundingBox.setPoint(7, maxX, maxY, maxZ)
    return boundingBox


def constrainCloud(
    path_to_cloud: str,
    path_to_output_cloud: str = "\constrained_cloud.txt",
    bounding_box_list: list = [-10, 10, -10, 10, -10, 10, -10, 10],
) -> str:
    """
    Constrains the bounding box of a cloud.

    Parameters
    ----------
    path_to_cloud : CloudComPy.Cloud
        Path to a cloud to constrain the bounding box of.
    path_to_output_cloud : str
        Path to the output cloud.


    bounding_box_list : list
        List of bounding coords to constrain the cloud to. E.g. bounding_box_list = [Xmin, Xmax, Ymin, Ymax, Zmin, Zmax]
    Returns
    -------
    CloudComPy.Cloud
        Constrained bounding box of the cloud. Filtered original cloud.
    """
    assert os.path.isfile(path_to_cloud), "Error, file not found"
    if path_to_output_cloud == "\constrained_cloud.txt":
        path_to_output_cloud = (
            os.path.abspath("") + "/constrained_cloud.txt"
        )

    print(f"Constraining cloud {path_to_cloud}")
    print(f"Output cloud {path_to_output_cloud}")
    # Xmin, Xmax, Ymin, Ymax, Zmin, Zmax = -0, 3, -0, 3, -10, 10
    [Xmin, Xmax, Ymin, Ymax, Zmin, Zmax] = bounding_box_list
    time_now: float = perf_counter()
    with open(path_to_cloud, "r") as f:
        # TODO check if this is the correct way to read the file, maybe it is better to use the different methods.
        data1 = f.readlines()
        print("Data loaded")
        print("Data1: ", len(data1))
        # data1 = [list(map(float, line.split())) for line in data1]
        # data2 = [list(map(float, line.split())) for line in data2]

        data1_list = []
        for i in range(len(data1)):
            data1_list.append(data1[i].split(" "))
            data1_list[i] = [float(x) for x in data1_list[i]]

        print("data1_list length: ", len(data1_list))

        print("data1_list[:10]: ", data1_list[:10])
    print("File read and converted in:", perf_counter() - time_now)

    # np.savetxt(
    #     r"C:\Users\szinp\Desktop\GIS_PROJECT\CloudComPy39_20220513\CloudCompPy_Computing-CloudPoint\dataFolder\pythonScripts_testInputs\1_E_subsample_ORIGINAL.txt",
    #     data1_list,
    #     delimiter=" ",
    #     newline="\n",
    # )
    # ********************************************************************************************************************
    # ? Filtering CHAD version
    # ********************************************************************************************************************
    time_now: float = perf_counter()

    print("Filtering")

    filtered_data1_list = []
    with tqdm.tqdm(total=len(data1_list)) as pbar:
        pbar.colour = "MAGENTA"
        for cell_in_data1_list in data1_list:
            if (
                cell_in_data1_list[0] >= Xmax
                or cell_in_data1_list[0] <= Xmin
                or cell_in_data1_list[1] >= Ymax
                or cell_in_data1_list[1] <= Ymin
                or cell_in_data1_list[2] >= Zmax
                or cell_in_data1_list[2] <= Zmin
            ):
                continue
            else:
                filtered_data1_list.append(cell_in_data1_list)
                # TODO fix the update of the bar
            pbar.update(1)
        pbar.close()

    print("Filtering done")
    print("Filtered_data1_list len: ", len(filtered_data1_list))
    print("Filtering done in: ", perf_counter() - time_now)
    assert (
        len(filtered_data1_list) > 1
    ), "Filtering failed, check the bounding box"

    print(f"Saving filtered data to {path_to_output_cloud}...")

    np.savetxt(
        fname=path_to_output_cloud,
        X=filtered_data1_list,
        delimiter=" ",
        newline="\n",
    )
    print("Done saving filtered data")
    return path_to_output_cloud
