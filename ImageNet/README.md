# ImageNet

## ImageNet Large Scale Visual Recognition Challenge 2012 (ILSVRC2012)

## Data Features

## Data Example

```
NA
```

## Download Links

- [Download Links](https://image-net.org/challenges/LSVRC/2012/2012-downloads.php)

## Download Script

```shell
cd DATASET_NAME
chmod +x download_datasets.sh
nohup ./download_datasets.sh >nohup.out& 2>&1
watch -n 1 tail nohup.out
```

- The downloaded files are structured as follows:

```
ImageNet/
    ILSVRC2012/
        bounding_boxes/
            train/
                ILSVRC2012_bbox_train_dogs.tar.gz
                ILSVRC2012_bbox_train_v2.tar.gz
            valid/
                ILSVRC2012_bbox_val_v3.tgz
            test/
                ILSVRC2012_bbox_test_dogs.zip

        images/
            train/
                ILSVRC2012_img_train.tar
                ILSVRC2012_img_train_t3.tar
            valid/
                ILSVRC2012_img_val.tar
            test/
                ILSVRC2012_img_test_v10102019.tar
```

## Statistics

NA

## Reference

- [ILSVRC2012](https://image-net.org/challenges/LSVRC/2012/index)