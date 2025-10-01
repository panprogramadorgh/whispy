ARG cmake_build_type="Release"
ARG build_directory="./build"

FROM debian:trixie-backports
WORKDIR /app
COPY . .

RUN apt update && apt install g++ make cmake
RUN cmake . -B "$build_directory" -DCMAKE_BUILD_TYPE="$cake_build_type" && cmake --build "$build_directory"

FROM python:latest

CMD ["python3", "./tests/basic-test.py"]