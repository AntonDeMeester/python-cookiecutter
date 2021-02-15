FROM python:3.9

ENV WORKDIR=/code

# set the working directory in the container
WORKDIR $WORKDIR

{%- if cookiecutter.fast_api == true -%}
EXPOSE 8000
{% endif %}

# copy the dependencies file to the working directory
COPY Pipfile* $WORKDIR

# install dependencies 
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# copy the content of the local src directory to the working directory
COPY {{cookiecutter.app_name}}/ config/ .

{%- if cookiecutter.fast_api == true -%}
CMD [ "uvicorn", "wealth.main:app", "--host", "0.0.0.0", "--port", "8000"]
{%- else -%}
CMD ["python" "main.py"]
{%- endif -%}
