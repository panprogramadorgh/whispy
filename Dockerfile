FROM gcc:15.2.0 as builder

ENV CMAKE_BUILD_TYPE=Release
ENV CMAKE_BUILD_DIR=cmake-build

RUN apt update && apt install -y cmake make

WORKDIR /app
COPY . .

CMD ["sh", "-c", "cmake . -B ${CMAKE_BUILD_DIR} -DCMAKE_TOOLCHAIN_FILE=./cmake/toolchains/amd64-linux-gnu.cmake && make -j 4"]
