FROM yacchin1205/research-notebook:20200512

USER root

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN mv ./notebooks/* ./

# Install production dependencies.
RUN pip install Flask gunicorn

# Prepare files
RUN if [ -f "./prepare.ipynb" ]; then papermill ./prepare.ipynb -; fi

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
