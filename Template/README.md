# Dataset Name

## Data Features

## Data Example

```
NA
```

## Download Links

## Download Script

```shell
cd DATASET_NAME
chmod +x download_datasets.sh
nohup ./download_datasets.sh >nohup.out& 2>&1   # download in the background
disown %1                                       # optional, detach from the job
watch -n 1 tail nohup.out                       # watch the progress
```

- The downloaded files are structured as follows:

    ```
    DATASET_NAME/
        train.file xxG
        valid.file xxM
        test.file xxM
    ```

## Statistics

NA

## Reference

- [Ref](link)