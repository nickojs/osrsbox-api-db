# Author:  PH01L
# Email:   phoil@osrsbox.com
# Website: https://www.osrsbox.com
#
# Description:
# Dockerfile for data initialization
#
# Copyright (c) 2020, PH01L
###############################################################################
FROM python:3.7-alpine
LABEL MAINTAINER="PH01L <phoil@osrsbox.com>"

# Set PYTHONPATH environment variable
ENV PYTHONPATH "${PYTHONPATH}:/var/www/eve/"

# Set working directory
WORKDIR /var/www/eve/

# Install requirements
ADD ./requirements.txt /var/www/eve/requirements.txt
RUN pip install -r requirements.txt

# Default entrypoint for data insertion
ENTRYPOINT ["sh"]

