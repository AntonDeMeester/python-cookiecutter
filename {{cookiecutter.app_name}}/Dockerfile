FROM python:3.9

ENV WORKDIR=/code

# set the working directory in the container
WORKDIR $WORKDIR

EXPOSE 8000

# copy the dependencies file to the working directory
COPY Pipfile* $WORKDIR

# install dependencies 
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# copy the content of the local src directory to the working directory
COPY {{cookiecutter.app_name}}/ config/ .

CMD [ "uvicorn", "wealth.main:app", "--host", "0.0.0.0", "--port", "8000"]
