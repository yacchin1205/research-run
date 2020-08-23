FROM yacchin1205/research-notebook:latest

USER root

RUN conda install supervisor jupyter_kernel_gateway

# Install production dependencies.
RUN pip install Flask gunicorn requests

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN mv ./notebooks/* ./ && mv ./scripts/* / && \
    chmod +x /*.sh && mkdir -p /opt/run/conf.d && \
    mv /supervisor.conf /opt/run/ && \
    mv /main.conf /opt/run/conf.d/

# Prepare files
RUN if [ -f "./prepare.ipynb" ]; then papermill ./prepare.ipynb -; fi
RUN cd /; curl -O http://compling.hss.ntu.edu.sg/wnja/data/1.1/wnjpn.db.gz && gunzip wnjpn.db.gz

CMD /start.sh
