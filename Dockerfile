# syntax=docker/dockerfile:1

FROM ubuntu:latest

RUN apt-get update -y; apt-get install python3 python3-pip wget nano curl unzip fontconfig libfontconfig1 libicu-dev -y;

WORKDIR /tmp
RUN useradd -m john; chown -R john:john /app; chown -R john:john /home/john; chown -R john:john /usr/local

RUN chown -R john:john .

# Download latest TwitchDownloaderCLI
RUN curl -s https://api.github.com/repos/lay295/TwitchDownloader/releases/latest \
	| grep -E "browser_download_url\": (.*?)-Linux-x64.zip" \
	| cut -d : -f 2,3 | tr -d \"\
	| wget -qi -

RUN mkdir files

RUN unzip *.zip
RUN rm *.zip

# Install TwitchDownloaderCLI
RUN chmod +x TwitchDownloaderCLI
RUN cp TwitchDownloaderCLI /usr/bin/TwitchDownloaderCLI
RUN rm TwitchDownloaderCLI

WORKDIR /app
USER john
