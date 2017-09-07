# libftdi1.4 with Python3.6 (32bit) for Windows

## Introduction

This repository attempts to control a Adafruit FT232H chip via USB interface on Windows. Adafruit has a step-by-step tutorial on its website (https://learn.adafruit.com/adafruit-ft232h-breakout/windows-setup).

However, you will have trouble if you are using Python3.6 because:
  - the information is for libftdi1.0 with Python2.7
  - python binding (.pyd) file is highly version-dependent
  - destructive changes have been made to the API of libftdi1.2
  - Python3 handles "bytes", "bytearray", and "string" type differently from Python2

In this page, I will write about how to prepare a development environment on a Windows machine. Also, you can directly grab the binary files from release if you are not interested in the topic.

## How to use the files in "release"

Follow the Adafruit tutorial except that:
  - at step2 "libftdi Install", use the files in my release instead of theirs
  - at step3 "Adafruit Python GPIO Library Install", overwrite FT232H.py file in "Python diretory/Lib/site-packages/Adafruit_GPIO"

Then you should be able to run the codes in Example folder.

========================================================

Read below only if you are interested in how to compile the libftdi1.4 source code

========================================================

## How to compile the libftdi1.4 Python binding on Windows

The goal of this is to get ftdi1.py and _ftdi1.pyd for the target platform. (Python3.6 32bit on Windows)

You need to prepare:
  - libftdi1.4 source code (https://www.intra2net.com/en/developer/libftdi/)
  - cmake Windows binary distribution (https://cmake.org/download/)
  - C, C++ compilors. I used Qt creator. (https://www.qt.io/ide/)
  - SWIG, a c++ to Python "interpreter". (http://www.swig.org/)

Note: You can also cross-compile it for Windows on a Linux machine. Refer to "README" under libbftdi1.4 sourcode root directory.

## Compilor config

After installation of cmake-gui, run Qt creator and go to "Option/Build&Run/Kits". Change the following fields:
  - C compilor
  - C++ compilor
  - CMake Tool
 This will help cmake-gui auto fill the compilor paths.

## CMake the source code

Run Cmake and set "source code directory" to ".../libftdi1-1.4" and "binary directory" to ".../libftdi1-1.4/build".

Go to menu "Tools -> Config" and select MinGW Makefiles as the generator. Specify your Python directory and SWIG directory if errors pop out.

Note: 

Some errors might pop out if you are using the latest cmake-gui. You can fix that by editing "libftdi1-1.4/Python/CMakelist.txt". 

Before:

SWIG_ADD_MODULE(ftdi1 python ftdi1.i)

After:

if (${CMAKE_VERSION} VERSION_LESS "3.8.0")

    SWIG_ADD_MODULE(ftdi1 python ftdi1.i)
    
else()

    SWIG_ADD_LIBRARY(ftdi1
    
    LANGUAGE python
    
    SOURCES ftdi1.i)
    
endif()

Note2:

Some errors might pop out telling you some files are missing. (such as xxx.h and usblib.dll) You can probably find these files here. (http://libusb.info/)

## Create Python binding

Open command prompt and cd to "...\libftdi1-1.4\build\Python".Run command "mingw32-make". Some errors might pop out indicating missing files. Fix that manually. The "ftdi1.py" and "_ftdiq1.pyd" files will then be generated under the same directory. Copy and paste the files to ".../Python diretory/Lib/site-packages" and test the codes in "Example" folder of this Github repository.

## Update FT232h.py

The FT232h.py in "Python diretory/Lib/site-packages/Adafruit_GPIO" is written for Python 2.7. To make it work for Python3 or above, some workarounds are necessary. The major changes are the way Python3 handles bytes and bytearrays. Google "Python3 bytes bytearray unicode" for more details. A new FT232h.py for Python 3.6 can also be found in this Github repository. However, I only tested GPIO and I2C functions.
