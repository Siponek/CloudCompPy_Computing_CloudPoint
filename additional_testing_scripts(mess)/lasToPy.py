import os
# import sys
import math
# import psutil
import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
# from matplotlib import colors
import laspy
import tqdm
# from time import sleep
from pathlib import Path
import argparse


def convertLasTxt(pathToFile : str, nameOfFileOutput : str = "myCloud.txt") -> list:
    """convertLasTxt Converts .las file to .txt file for reading with cloudComPy.
    Note: it uses tqdm to show the progress of the conversion.

    Parameters
    ----------
    pathToFile : str
        _description_
    """
    listCoord_XYZ = np.empty([1,3])
    tmpList = []
    x:float = 0.0
    y:float = 0.0
    z:float = 0.0
    # limit : int = 0
    #! remark - path 2 has a lot of points, so it takes a while to read it (76_568_359 to be exact).
    with tqdm.tqdm(total=Path(pathToFile).stat().st_size) as pbar:
        with laspy.open(source = pathToFile) as cloudFileHeader:
            if type(cloudFileHeader) != None:
                cloudFile = laspy.read(source=pathToFile)
                try:
                    print("Cloud loaded")
                    print(f"cloud name:{cloudFile.header}")
                except:
                    print(f"cloud name:<unknown>")
            for points in cloudFileHeader.chunk_iterator(1):
                x,y,z = points.array[0]['X'], points.array[0]['Y'], points.array[0]['Z']
                # valuesToAppend = np.array([[x,y,z]])
                valuesToAppend = [x,y,z]
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
            np.savetxt(nameOfFileOutput, listCoord_XYZ, delimiter=" ", newline="\n")
            print(f"convertLasTxt _> File {nameOfFileOutput} saved")
    print("convertLasTxt _> Conversion finished")
    return listCoord_XYZ
# pass radius as an argument
def create_points_around_atom(number:int, center:list, radius:float):

    # generate the random quantities
    phi         = np.random.uniform( 0, 2*np.pi, size=(number,))
    theta_cos   = np.random.uniform(-1,       1, size=(number,))
    u           = np.random.uniform( 0,       1, size=(number,))

    # calculate sin(theta) from cos(theta)
    theta_sin   = np.sqrt(1 - theta_cos**2)
    r           = radius * np.cbrt(u)

    # use list comprehension to generate the coordinate array without a loop
    # don't forget to offset by the atom's position (center)
    return np.array([
        np.array([
            center[0] + r[i] * theta_sin[i] * np.cos(phi[i]),
            center[1] + r[i] * theta_sin[i] * np.sin(phi[i]),
            center[2] + r[i] * theta_cos[i]
        ]) for i in range(number)
    ])

def createSphere(radius:float = 5, number:int=10,  center:list = [0,0,0]):
    pi = math.pi
    sin = math.sin
    cos = math.cos
    lst = []
    for phi in [(pi*i)/(number-1) for i in range(number)]:
        M = int(sin(phi)*(number-1))+1
        for theta in [(2*pi*i)/M for i in range(M)]:
            x = center[0] + radius * sin(phi) * cos(theta)
            y = center[1] + radius * sin(phi) * sin(theta)
            z = center[2] + radius * cos(phi)
            lst.append((x, y, z))
    return np.array(lst)


def main():
    print("Main : Libs loaded")
    parser = argparse.ArgumentParser(description='Convert .las files into .txt files for cloudComPy. example: python3 lasToPy.py -i "C:\Users\User\Desktop\myCloud.las" -o "C:\Users\User\Desktop\myCloud.txt"')
    parser.add_argument('datapath', type=Path)
    parser.add_argument('--output', type=str, default="myCloud.txt")
    args = parser.parse_args()
    print(f"Main : {args.datapath}")
    print(f"Main : {args.output}")
    print("Main : Checking if file exists...")
    assert os.path.isfile(args.datapath)

    print("Main : Starting conversion")
    listOfCloudPointsFirst = convertLasTxt(pathToFile=args.datapath
                                        , nameOfFileOutput=args.output)
    print(f"File from {args.datapath} \n Done")

                                    

if __name__ == "__main__":
    main()