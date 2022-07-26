FROM python:3
# Create scripts folder
RUN mkdir /scripts
# Setting work dir
WORKDIR /scripts
# Copy all py files and requirements.txt into scripts folder
COPY *.py  ./
ADD requirements.txt ./
# Install Python dependencies
RUN pip install -r ./requirements.txt
# Execute command to run python scripts
CMD [ "python", "/scripts/main.py" ]