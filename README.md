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

## Contents
Suggested winpython env


## Connection

|aoPin|Cable #|Coil|Comp. mT/V|
|:---:|:---:|:---:|:---:|
|2|1|Z - Mid top|5.003|
|5|2|Z - Mid bot|4.433|
|4|3|Y - Inn right|5.143|
|1|4|Y - Inn left|5.024|
|3|5|X - Out right|4.879|
|0|6|X - Out left|5.003|
|6|7|Not Used|Not Used|
|7|8|Not Used|Not Used|

![Click here for the image](Images/coil_connection.png)
