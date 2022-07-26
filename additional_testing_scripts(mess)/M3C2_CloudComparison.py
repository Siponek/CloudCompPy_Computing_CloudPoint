import os
import math
import argparse
import numpy as np
import laspy
from tqdm import tqdm
from pathlib import Path
import cloudComPy as cc
from gendata import getSampleCloud, dataDir

print("Main : Libs loaded")
import logging

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
    #! remark - path 2 has a lot of points, so it takes a while to read it (76_568_359 to be exact).
    with tqdm(total=Path(pathToFile).stat().st_size) as pbar:
        with laspy.open(source=pathToFile) as cloudFileHeader:
            if type(cloudFileHeader) != None:
                cloudFile = laspy.read(source=path2)
                try:
                    print("Cloud loaded")
                    print(f"cloud name:{cloudFile.header}")
                except:
                    print(f"cloud name:<unknown>")

            # ? It seems that chunk_iterator helps to read data in batches. In every batch it reads the data and then it moves to the next batch.
            # ? Points.array is in fact a one point array. if we set chunk_iterator to (1)
            # ? What is the data inside of the point? It must be x,y,z and something else. It is possible to extract x,y,z from the point. Is it enough data?
            for points in cloudFileHeader.chunk_iterator(1):
                x, y, z = (
                    points.array[0]["X"],
                    points.array[0]["Y"],
                    points.array[0]["Z"],
                )
                valuesToAppend = np.array([[x, y, z]])
                tmpList.append(valuesToAppend)
                # listCoord_XYZ = np.concatenate((listCoord_XYZ, valuesToAppend), axis=0)
                # np.append(arr = listCoord_XYZ, values= valuesToAppend , axis=0)
                pbar.update(n=1)
            listCoord_XYZ = np.array(tmpList)
            pbar.close()
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
    """createSpherePoints It generates sphere point cloud without any points in the volume with a given center and radius.

    Parameters
    ----------
    radius : float, optional
        _description_, by default 5
    number : int, optional
        _description_, by default 10
    center : list, optional
        _description_, by default [0,0,0]
    cutTheShape : str, optional
        _description_, Cut the shape of the sphere according to GLOBAL coordinates.
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


def main():
    """main Main funtion of the program."""

    # # create logger with 'spam_application'
    # logger = logging.getLogger("My_app")
    # logger.setLevel(logging.DEBUG)

    # # create console handler with a higher log level
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)

    # ch.setFormatter(CustomFormatter())

    # logger.addHandler(ch)

    argparser = argparse.ArgumentParser(
        description="Generate point cloud with M3C2 plugin"
    )  #! This is the main argument parser.
    argparser.add_argument(
        "-firstCd",
        type=str,
        help="path to the file of first cloud",
        required=True,
    )
    argparser.add_argument(
        "-secondCd",
        type=str,
        help="path to the file of second cloud",
        required=True,
    )
    argparser.add_argument(
        "--nameOfFileOutput",
        type=str,
        help="name of the output file",
        default="M3C2_output.las",
    )
    argparser.add_argument(
        "--parametersConfigFilePath",
        help="path to the file of parameters (e.g. m3c2_params.txt)",
        default="m3c2_params.txt",
    )
    argparser.add_argument(
        "-tVerbose",
        action="store_true",
        default=False,
        dest="boolean_Verbose",
        help="Set a verbose mode to true",
    )
    argparser.add_argument(
        "-fVerbose",
        action="store_false",
        default=True,
        dest="boolean_Verbose",
        help="Set a verbose mode to false",
    )
    argparser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0 (2020) by Szymon :>",
        help="show version",
    )
    args = argparser.parse_args()

    path1 = os.path.abspath("") + args.firstCd
    path2 = os.path.abspath("") + args.secondCd
    paramFilePath = (
        os.path.abspath("") + args.parametersConfigFilePath
    )
    assert os.path.isfile(
        path1
    ), "First cloud file does not exist. Check the path."
    assert os.path.isfile(
        path2
    ), "Second cloud file does not exist. Check the path."
    print(os.path.abspath("") + args.parametersConfigFilePath)
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
    # cloud1 = cc.loadPointCloud(getSampleCloud(1.0))
    # cloud2 = cc.loadPointCloud(getSampleCloud(2.0))
    prGreen("Loading finished")
    cloud1.setName("cloud1")
    cloud2.setName("cloud2")

    res = cc.ICP(
        data=cloud2,
        model=cloud1,
        minRMSDecrease=1.0e-5,
        randomSamplingLimit=50000,
        maxIterationCount=40,
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

    #! Reading parameters form ready file for now
    # Windows
    # paramFilename = (
    #     os.path.abspath("")
    #     + "\dataFolder\PythonParameters\\bigData_1_m3c2_params.txt"
    # )
    # Linux

    print(f"Reading params from {paramFilePath} ...")
    # with open(paramFilename, 'w') as f:
    #     f.write("[General]\n")
    #     for k,v in m3c2_params_dic.items():
    #         f.write("%s=%s\n"%(k,v))
    print("Searching for M3C2 plugin in enviroment...")
    if cc.isPluginM3C2():
        ###* this is actually necesary for the plugin to work
        import cloudComPy.M3C2

        prGreen("M3C2 plugin is loaded, attempting to run M3C2")
        CloudAfterM3C2 = cc.M3C2.computeM3C2(
            [cloud1, cloud2ICP], paramFilePath
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
        # if not math.isclose(sf.getMax(), 0.71, rel_tol=0.01):
        #     raise RuntimeError
        # if not math.isclose(sf.getMin(), -0.70, rel_tol=0.01):
        #     raise RuntimeError

        # Windows:

        pathToSaveOutput = (
            os.path.abspath("") + "/%s" % args.nameOfFileOutput
        )
        print(f"Saving results to {pathToSaveOutput}")
        cc.SavePointCloud(CloudAfterM3C2, pathToSaveOutput)  # OK
        # cc.SaveEntities([cloud1,cloud2, cloud2ICP, CloudAfterM3C2],pathToSaveOutput)


if __name__ == "__main__":
    main()
    prGreen("Job finished")
