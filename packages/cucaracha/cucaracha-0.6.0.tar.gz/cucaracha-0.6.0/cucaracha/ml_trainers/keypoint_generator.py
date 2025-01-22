# import keras
# import numpy as np

# # from cucaracha.ml_training.utils import get_keypoint_train_data


# class KeyPointsDataset(keras.utils.PyDataset):
#     def __init__(
#         self,
#         image_keys,
#         aug,
#         batch_size: int,
#         img_size: int,
#         num_keypoints: int,
#         train: bool = True,
#         **kwargs
#     ):
#         super().__init__(**kwargs)
#         self.image_keys = image_keys
#         self.aug = aug
#         self.batch_size = batch_size
#         self.train = train
#         self.img_size = img_size
#         self.num_keypoints = num_keypoints
#         self.on_epoch_end()

#     def __len__(self):
#         return len(self.image_keys) // self.batch_size

#     def on_epoch_end(self):
#         self.indexes = np.arange(len(self.image_keys))
#         if self.train:
#             np.random.shuffle(self.indexes)

#     def __getitem__(self, index):
#         indexes = self.indexes[
#             index * self.batch_size : (index + 1) * self.batch_size
#         ]
#         image_keys_temp = [self.image_keys[k] for k in indexes]
#         (images, keypoints) = self.__data_generation(image_keys_temp)

#         return (images, keypoints)

#     def __data_generation(self, image_keys_temp):
#         batch_images = np.empty(
#             (self.batch_size, self.img_size, self.img_size, 3), dtype='int'
#         )
#         batch_keypoints = np.empty(
#             (self.batch_size, 1, 1, self.num_keypoints), dtype='float32'
#         )

#         for i, key in enumerate(image_keys_temp):
#             data = get_keypoint_train_data(key)
#             current_keypoint = np.array(data['joints'])[:, :2]
#             kps = []

#             # To apply our data augmentation pipeline, we first need to
#             # form Keypoint objects with the original coordinates.
#             for j in range(0, len(current_keypoint)):
#                 kps.append(
#                     Keypoint(
#                         x=current_keypoint[j][0], y=current_keypoint[j][1]
#                     )
#                 )

#             # We then project the original image and its keypoint coordinates.
#             current_image = data['img_data']
#             kps_obj = KeypointsOnImage(kps, shape=current_image.shape)

#             # Apply the augmentation pipeline.
#             (new_image, new_kps_obj) = self.aug(
#                 image=current_image, keypoints=kps_obj
#             )
#             batch_images[
#                 i,
#             ] = new_image

#             # Parse the coordinates from the new keypoint object.
#             kp_temp = []
#             for keypoint in new_kps_obj:
#                 kp_temp.append(np.nan_to_num(keypoint.x))
#                 kp_temp.append(np.nan_to_num(keypoint.y))

#             # More on why this reshaping later.
#             batch_keypoints[i,] = np.array(
#                 kp_temp
#             ).reshape(1, 1, 24 * 2)

#         # Scale the coordinates to [0, 1] range.
#         batch_keypoints = batch_keypoints / IMG_SIZE

#         return (batch_images, batch_keypoints)
