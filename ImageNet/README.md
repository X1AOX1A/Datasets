# ImageNet

## ImageNet Large Scale Visual Recognition Challenge 2012 (ILSVRC2012)

- [ILSVRC2012](https://image-net.org/challenges/LSVRC/2012/index)
- [Download Links](https://image-net.org/challenges/LSVRC/2012/2012-downloads.php)

```shell
## make directories
mkdir ILSVRC2012
mkdir ILSVRC2012/images
mkdir ILSVRC2012/bounding_boxes
mkdir ILSVRC2012/images/train
mkdir ILSVRC2012/images/valid
mkdir ILSVRC2012/images/test
mkdir ILSVRC2012/bounding_boxes/train
mkdir ILSVRC2012/bounding_boxes/valid
mkdir ILSVRC2012/bounding_boxes/test

## Download Images
# download train(task1&2) images to ILSVRC2012/images/train
# 138GB. MD5: 1d675b47d978889d74fa0da5fadfb00e
wget https://download_link_to_ILSVRC_2012/ILSVRC2012_img_train.tar -P ILSVRC2012/images/train

# download train(task3 only) images to ILSVRC2012/images/train
# 728MB. MD5: ccaf1013018ac1037801578038d370da
wget https://download_link_to_ILSVRC_2012/ILSVRC2012_img_train_t3.tar -P ILSVRC2012/images/train

# download valid(all tasks) images to ILSVRC2012/images/valid
# 6.3GB. MD5: 29b22e2961454d5413ddabcf34fc5622
wget https://download_link_to_ILSVRC_2012/ILSVRC2012_img_val.tar -P ILSVRC2012/images/valid

# download test(all tasks) images to ILSVRC2012/images/test
# 13GB. MD5: e1b8681fff3d63731c599df9b4b6fc02 
wget https://download_link_to_ILSVRC_2012/ILSVRC2012_img_test_v10102019.tar -P ILSVRC2012/images/test

## Download Bounding Boxes
# download train(task1&2) bounding boxes to ILSVRC2012/bounding_boxes/train
# 20MB. MD5: 9271167e2176350e65cfe4e546f14b17
wget https://download_link_to_ILSVRC_2012/ILSVRC2012_bbox_train_v2.tar.gz -P ILSVRC2012/bounding_boxes/train

# download train(task3 only) bounding boxes to ILSVRC2012/bounding_boxes/train
# 1MB. MD5: 61ebd3cc0e4793899a841b6b27f3d6d8
wget https://download_link_to_ILSVRC_2012/ILSVRC2012_bbox_train_dogs.tar.gz -P ILSVRC2012/bounding_boxes/train

# download valid(all tasks) bounding boxes to ILSVRC2012/bounding_boxes/valid
# 2.2MB. MD5: f4cd18b5ea29fe6bbea62ec9c20d80f0
wget https://download_link_to_ILSVRC_2012/ILSVRC2012_bbox_val_v3.tgz -P ILSVRC2012/bounding_boxes/valid

# download test(task3 only) bounding boxes to ILSVRC2012/bounding_boxes/test
# 33MB. MD5: 2dfdb2677fd9661585d17d5a5d027624
wget https://download_link_to_ILSVRC_2012/ILSVRC2012_bbox_test_dogs.zip -P ILSVRC2012/bounding_boxes/test
```