#! /bin/sh

# Read env vars
BTYPE=$CMAKE_BUILD_TYPE
BDIR=$CMAKE_BUILD_DIR
COMPILER=$CMAKE_CXX_COMPILER

if [ "$BTYPE" = "" ]; then
  BTYPE=Release
fi

if [ "$BDIR" = "" ]; then
  BDIR=cmake-build
fi

if [ "$COMPILER" = "" ]; then
  COMPILER=/usr/bin/g++
fi

cmake . -B $BDIR -DCMAKE_BUILD_TYPE=$BTYPE -DCMAKE_CXX_COMPILER=$COMPILER