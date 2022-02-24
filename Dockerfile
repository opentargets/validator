FROM python:3.7-slim
LABEL maintainer="data@opentargets.org"

#need make gcc etc for requirements later
RUN apt-get update && apt-get install -y \
    build-essential

#put the application in the right place
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pip install --no-cache-dir -e .

# point to the entrypoint script
ENTRYPOINT [ "opentargets_validator" ]
