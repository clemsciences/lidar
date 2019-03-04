#!/bin/bash

#-e git+https://github.com/Club-INTech/rplidar_a2.git@07cb93eff2fca2d45526760134577bad376c3897#egg=rplidar
git clone https://github.com/Club-INTech/rplidar_a2.git
git reset 07cb93eff2fca2d45526760134577bad376c3897
cd rplidar_a2
cmake CMakeLists.txt
make

