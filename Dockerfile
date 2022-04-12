FROM continuumio/miniconda3

RUN /opt/conda/bin/conda config --add channels conda-forge && /opt/conda/bin/conda update -y conda \
    && /opt/conda/bin/conda install -y geopandas  dash  \
    dash-bootstrap-components  \
    dash-core-components  
    

WORKDIR /app

COPY . .

CMD ["python", "app.py"]