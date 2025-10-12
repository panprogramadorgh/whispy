#! /bin/sh

BDIR=$CMAKE_BUILD_DIR

if [ "$BDIR" = "" ]; then
  BDIR=cmake-build
fi

cmake --build $BDIR -- -j $(nproc) &&
mkdir -p ./src/whispy/lib

cp $BDIR/libwhispy.so ./src/whispy/lib &&
cp $BDIR/lib/whisper.cpp/src/libwhisper.so ./src/whispy/lib &&
cp $BDIR/lib/whisper.cpp/src/libwhisper.so.1 ./src/whispy/lib &&
cp $BDIR/lib/whisper.cpp/src/libwhisper.so.1.7.4 ./src/whispy/lib &&
cp $BDIR/lib/whisper.cpp/ggml/src/libggml.so ./src/whispy/lib &&
cp $BDIR/lib/whisper.cpp/ggml/src/libggml-base.so ./src/whispy/lib &&
cp $BDIR/lib/whisper.cpp/ggml/src/libggml-cpu.so ./src/whispy/lib