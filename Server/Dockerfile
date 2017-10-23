# Use an official Python runtime as a parent image
FROM centos:7

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages needed, in this case pip for python installation modules
RUN yum -y update; yum clean all
RUN yum -y install epel-release; yum clean all
RUN yum -y install python-pip; yum clean all

#Install some pythons needs
RUN pip install -r requirements.txt
#RUN pip install opencv-python

# Make port 6666 available to the world outside this container
EXPOSE 6666

# Define environment variable
#ENV NAME World

# Run python server.py when the container launches
CMD ["python", "../vol/server.py"]
