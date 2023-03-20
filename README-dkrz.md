# stac at dkrz

## infos andrey

https://docs.google.com/document/d/1DVonmNU8FzaS66GjYiEMftXF9qCDpg-YjXtve08lEn0/edit#heading=h.oxsfdxvp2n1c

### copy

Resources required to implement the CEDA STAC API implementation in DKRZ

STAC API
https://github.com/cedadev/stac-fastapi-elasticsearch/tree/atod

STAC Generator
https://github.com/cedadev/stac-generator-example

https://github.com/cedadev/stac-generator.git
git checkout issue/172/atod

Pystac
https://github.com/cedadev/pystac-client/tree/asset-search
https://github.com/cedadev/esgf-stac-client

Necessary config files (latest versions)
https://drive.google.com/drive/folders/1psdyQyPrlaaqLC-Rb3QWRtzxcaR9BWO8?usp=sharing

regex:  'https://swift.dkrz.de/v1/dkrz_0b2a0dcc-1430-4a8a-9f25-a6cb8924d92b/cmip6-zarr-2021\/(?P<mip_era>\w+)\.(?P<activity_id>\w+)\.(?P<institution_id>\w+(?:-\w+)*)\.(?P<source_id>\w+(?:-\w+)+)\.(?P<experiment_id>\w+)\.(?P<member_id>\w+)\.(?P<table_id>\w+)\.(?P<variable_id>\w+)\.(?P<grid_label>\w+)\.(?P<version>\w+)'


 intake catalog uri: https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/-/raw/master/esm-collections/cloud-access/dkrz_cmip6_cloud.json
The VM:
https://cloud.dkrz.de/dashboard/project/instances/96cc605f-5963-4085-9389-1c791b5bdadf/


## setup notes

stac-test1.cloud.dkrz.de


cd /usr/local/STAC/

https://github.com/cedadev/stac-fastapi-elasticsearch

branch atod

conda activate pystac

edit config:
/usr/local/STAC/stac-fastapi-elasticsearch/conf/defaults.py
```
dap_url = ''
posix_download_url = ''
```

make run-sample-elasticsearch

## client 

https://github.com/cedadev/stac-generator-example

pip install -r requirements.txt

https://github.com/cedadev/stac-generator.git
git checkout issue/172/atod

pip install -e .

Necessary config files (latest versions)
https://drive.google.com/drive/folders/1psdyQyPrlaaqLC-Rb3QWRtzxcaR9BWO8?usp=sharing



stac_generator conf/asset-generator.yaml 
stac_generator conf/item-generator.yaml
stac_generator conf/collection-generator.yaml

run search:

curl -X 'POST' 'http://0.0.0.0:8081/asset/search' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{
"q": "MPI-ESM*"
}'


## at dkrz

/usr/local/STAC/dkrz

git clone https://github.com/IS-ENES-Data/stac-fastapi-elasticsearch.git

git checkout dkrz


### clients

git clone https://github.com/IS-ENES-Data/stac-generator.git

git checkout dkrz

examples ...

git clone https://github.com/IS-ENES-Data/stac-generator-example.git

git checkout dkrz

## nore intake at dkrz

https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/-/raw/master/esm-collections/cloud-access/dkrz_cmip5_archive.json
https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/-/raw/master/esm-collections/cloud-access/dkrz_cmip5_disk.json
https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/-/raw/master/esm-collections/cloud-access/dkrz_cmip6_cloud.json
https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/-/raw/master/esm-collections/cloud-access/dkrz_cmip6_disk.json
https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/-/raw/master/esm-collections/cloud-access/dkrz_cordex_disk.json
https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/-/raw/master/esm-collections/cloud-access/dkrz_dyamond-winter_disk.json
https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/-/raw/master/esm-collections/cloud-access/dkrz_era5_disk.json
https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/-/raw/master/esm-collections/cloud-access/dkrz_monsoon_disk.yaml
https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/-/raw/master/esm-collections/cloud-access/dkrz_mpige_disk.json
https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/-/raw/master/esm-collections/cloud-access/dkrz_nextgems_disk.json
https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/-/raw/master/esm-collections/cloud-access/dkrz_palmod2_disk.json

