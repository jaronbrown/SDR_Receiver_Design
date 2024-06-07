FROM python:3.11.8-slim-bookworm

# Setup Quisk Configs
ENV conf="/config/quisk_config1.py"
ENV conf2="/config/quisk_config2.py"
ENV PYTHONPATH="/usr/lib/python3/dist-packages/"
ENV HOME="/config/"

# Setup timezone
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update \
	&& apt-get install -y \
	build-essential \
	cmake \
	g++ \
	libfftw3-dev \
	libasound2-dev \
	portaudio19-dev \
	libpulse-dev \
	python3-dev \
	libpython3-dev \
	python3-wxgtk4.0 \
	python3-usb \
	python3-serial \
	python3-setuptools \
	libpython3-dev \
	python3-numpy \
	swig \
	git \
	pulseaudio \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Install SoapySDR
RUN git clone --depth 1 --branch soapy-sdr-0.8.1 https://github.com/pothosware/SoapySDR.git /SoapySDR \
	&& mkdir /SoapySDR/build \
	&& cd /SoapySDR/build \
	&& cmake .. \
	&& make -j`nproc` \
	&& ldconfig

# Build Quisk
RUN git clone --depth 1 --branch v4.2.29 https://github.com/jimahlstrom/quisk /quisk \
	&& cd /quisk \
	&& make

# Fix Permissions - match local
RUN chown -R 1000:1001 /quisk

# Setup User
WORKDIR /config/

# Note run xhost +local: on host before docker run
CMD ["/bin/bash", "-c", "python3 /quisk/quisk.py -a --config=${conf} --config2=${conf2}"]
