FROM python:3
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y curl wget git ruby python3 python3-pip bc

RUN curl -Ls https://api.github.com/repos/ReFirmLabs/binwalk/releases/latest | \
  grep -wo "\"https.*tarball.*\"" | sed 's/"//g' | wget -qi - -O binwalk.tar.gz && \
  tar -xf binwalk.tar.gz && \
  cd ReFirmLabs-binwalk-*/ && \
  echo y | ./deps.sh | true

RUN apt-get install -y mtd-utils gzip bzip2 tar arj lhasa p7zip p7zip-full cabextract fusecram cramfsswap squashfs-tools sleuthkit default-jdk cpio lzop lzma srecord zlib1g-dev liblzma-dev liblzo2-dev unzip

RUN git clone https://github.com/devttys0/sasquatch && (cd sasquatch && ./build.sh && cd -)
RUN git clone https://github.com/devttys0/yaffshiv && (cd yaffshiv && python3 setup.py install && cd -)

RUN python3 -m pip install python-lzo cstruct ubi_reader
RUN apt-get install -y python3-magic openjdk-8-jdk unrar

# Release 2.3.1
RUN python3 -m pip install git+https://github.com/ReFirmLabs/binwalk@772f271

WORKDIR /binwalkparallel

ADD dlink.json .

ADD parallel_firmware_checker.py .

CMD ["python3", "parallel_firmware_checker.py", "-p", "/shared/firmware-images/tenda", "-c", "tenda", "-l", "/shared/firmware-images/binwalk-result/tenda-logs"]
