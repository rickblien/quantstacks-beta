# 'https://www.youtube.com/watch?v=bi0cKgmRuiA'
# Dockerfile, Image, Container

# Base Image
FROM python:3-onbuild

# Creaete a working directory for a starting point inside docker container
WORKDIR /usr/src/app

# Copy dependencies requirement
COPY ./requirement.txt ./requirement

# Install dependencies requrement
RUN pip3 install -r requirements.txt 

# Copy app directory and create app directory in Docker Container
COPY ./quantstacks-beta ./usr/src/app/

# Debugging - Verify copied file to Docker
RUN ls -l

# Set port
EXPOSE 8080

# Run "streamlit run" command
ENTRYPOINT [ "streamlit",'run' ]

# Run 'Dashboard.py' command
CMD [ "./Dashboard.py" ]



