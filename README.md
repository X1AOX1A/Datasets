A code repository for datasets downloading.

- Download the target dataset with `download_datasets.sh`:

```shell
cd DATASET_NAME
chmod +x download_datasets.sh
nohup ./download_datasets.sh >nohup.out& 2>&1
```

- Download the target dataset with `download_datasets.py`:

```shell
cd DATASET_NAME
python ./download_datasets.py
```