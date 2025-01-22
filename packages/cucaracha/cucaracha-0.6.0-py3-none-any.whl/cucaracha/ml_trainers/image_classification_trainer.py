import datetime
import os
import random

import keras
import numpy as np
import tensorflow as tf

from cucaracha.ml_models.image_classification import SmallXception
from cucaracha.ml_models.model_architect import ModelArchitect
from cucaracha.ml_trainers.ml_pattern import (
    MLPattern,
    check_architecture_pattern,
)
from cucaracha.utils import load_cucaracha_dataset


class ImageClassificationTrainer(MLPattern):
    def __init__(self, dataset_path: str, num_classes: int, **kwargs):
        """
        This is the main constructor for a general Image Classification ML method.

        Note:
            The `dataset_path` should follow the `cucaracha` dataset folder
            organization. More details about how to organize the dataset can be
            found at the `cucaracha` documentation.

        Info:
            There are many ways to find and build datasets to use for your
            machine learning models. A simpler way is using the public datasets
            given at the `cucaracha` Kaggle repository. You can find more
            details at: [https://www.kaggle.com/organizations/cucaracha-project](https://www.kaggle.com/organizations/cucaracha-project)

        Args:
            dataset_path (str): The path to the dataset. This should follow the
             `cucaracha` dataset folder organization.
            num_classes (int): The number of classes in the dataset. This must
            be defined based on the classes presented in the dataset.
            **kwargs: Additional keyword arguments for configuring the model.
            Possible keys include:
            - 'img_shape' (tuple): The shape of the input images. Default
            is (128, 128).
            - 'architecture' (object): The model architecture to use. If
            not provided, a default SmallXception architecture will be used.
            - 'batch_size' (int): The batch size to use during training. If
            not provided, a default value from MLPattern class  will be used.
            - 'epochs' (int): The number of epochs to train the model. If
            not provided, a default value from MLPattern class will be used.
            - 'model_name' (str): The name to use when saving the trained
            model. If not provided, a default name will be generated.
        Raises:
            ValueError: If the provided architecture is not for image
            classification tasks.
        """

        super().__init__(dataset_path)
        check_architecture_pattern(kwargs, 'image_classification')

        self.img_shape = kwargs.get('img_shape', (128, 128))
        self.batch_size = kwargs.get('batch_size', 64)
        self.epochs = kwargs.get('epochs', 500)
        self.num_classes = num_classes

        self.architecture = None
        self.model = None
        # If no architecture is provided, use the default one
        self._initialize_model(kwargs.get('architecture'), kwargs)

        # if binary classification, use binary metrics
        self._initialize_metrics(kwargs)

        self.data_generator = self._create_data_generator(
            kwargs.get('data_generator')
        )
        self.class_names = {}
        self.class_weights = {}
        self.dataset = self.load_dataset(
            kwargs.get('use_data_augmentation', True)
        )

        # Define the default model name to save
        self._define_model_name(kwargs)

        self.history = None

    def load_dataset(self, use_data_augmentation: bool = True):
        """
        Loads and prepares the image classification dataset for training and
        validation.

        The root path of the dataset should follow the `cucaracha` dataset.
        Therefore, the user must have a permission to read and write in the
        dataset path folder in order to create the organized data.

        Note:
            This method is automatically called when the class is instantiated.
            However, the user can call it again to reload the dataset and make
            an internal evaluation.



        This method performs the following steps:

        1. Calls the superclass method to load the dataset.
        2. Loads the cucaracha dataset from the specified path.
        3. Prepares the dataset environment by creating subfolders for each label.
        4. Loads the organized data using `keras.utils.image_dataset_from_directory`.
        5. Maps the training and validation datasets to one-hot encoded labels.

        Returns:
            dict: A dictionary containing the training and validation datasets
            with keys 'train' and 'val'.
        """
        super().load_dataset()

        # Prepare all the dataset environment
        # Create subfolders for each label
        train_dataset, _ = load_cucaracha_dataset(
            self.dataset_path, 'image_classification'
        )

        # Load the organized data using keras.utils.image_dataset_from_directory
        train_ds, val_ds = keras.utils.image_dataset_from_directory(
            train_dataset,
            image_size=self.img_shape,
            batch_size=self.batch_size,
            validation_split=0.2,
            subset='both',
            seed=random.randint(0, 10000),
        )

        self.class_names = {
            i: name for i, name in enumerate(train_ds.class_names)
        }

        if use_data_augmentation:
            train_ds = train_ds.map(
                lambda x, y: (
                    self.data_generator(x),
                    tf.one_hot(y, depth=self.num_classes),
                )
            )
            val_ds = val_ds.map(
                lambda x, y: (
                    self.data_generator(x),
                    tf.one_hot(y, depth=self.num_classes),
                )
            )
        else:
            train_ds = train_ds.map(
                lambda x, y: (
                    x,
                    tf.one_hot(y, depth=self.num_classes),
                )
            )
            val_ds = val_ds.map(
                lambda x, y: (
                    x,
                    tf.one_hot(y, depth=self.num_classes),
                )
            )

        # Calculate class weights based on the proportions of data in the dataset
        dataset = {'train': train_ds, 'val': val_ds}
        self._collect_dataset_class_weigth(dataset)

        return dataset

    def train_model(self, **kwargs):
        """
        Trains the model using the provided dataset and configuration.

        The information of `epochs`, `batch_size`, `loss`, `optimizer`, and
        `metrics` are already defined in the class constructor and it is used
        here to adjust the model training.

        When the training is finished, the model is updated to be saved or
        checked by the user. The model is provided by the object itself using
        the `obj.model` attribute.

        Examples:
            >>> from tests import sample_paths as sp
            >>> obj = ImageClassificationTrainer(sp.DOC_ML_DATASET_CLASSIFICATION, 3) # doctest: +SKIP
            >>> obj.epochs = 10 # doctest: +SKIP
            >>> obj.batch_size = 32 # doctest: +SKIP
            >>> obj.train_model() # doctest: +SKIP

            After the training, the model can be saved using the `obj.model`
            >>> import tempfile # doctest: +SKIP
            >>> with tempfile.TemporaryDirectory() as tmpdirname: # doctest: +SKIP
            >>>     obj.model.save(os.path.join(tmpdirname, 'saved_model.keras')) # doctest: +SKIP

        As an optional parameter, one can uses the following:
        - `callbacks` (list): A list of callback instances to apply during
        training. This can be any of the callback methods provided by Keras,
        such as `EarlyStopping`, `ReduceLROnPlateau`, etc. If not provided,
        a default `ModelCheckpoint` callback is used to save the model at the
        end of each epoch.
        - `data_augmentation` (ImageDataGenerator): A data generator for data
        augmentation using the Keras ImageDataGenerator class. If not provided,
        the default data augmentation is used as defined in the
        `_create_data_generator` method in the constructor class.

        Args:
            callbacks (list, optional): A list of callback instances to apply during training.
                        These can be any of the callback methods provided by Keras,
                        such as `EarlyStopping`, `ReduceLROnPlateau`, etc.
                        If not provided, a default `ModelCheckpoint` callback is used
                        to save the model at the end of each epoch.
        """
        callbacks = kwargs.get('callbacks', [])
        if not callbacks:
            callbacks = [
                keras.callbacks.ModelCheckpoint(
                    os.path.join(self.dataset_path, self.model_name),
                    monitor='val_acc',
                    save_best_only=True,
                )
            ]

        self.model.compile(
            optimizer=self.optimizer,
            loss=self.loss,
            metrics=self.metrics,
        )

        self.history = self.model.fit(
            self.dataset['train'],
            epochs=self.epochs,
            callbacks=callbacks,
            batch_size=self.batch_size,
            validation_data=self.dataset['val'],
            class_weight=self.class_weights,
        )

    def _create_data_generator(self, layers_list: list = None):
        """
        Create a data generator for data augmentation.

        This is a data augmentation based on the Keras augmentation layers.
        If none is providaded, then a default data augmentation is set, which
        assumes the following layers: RandomFlip, RandomRotation, RandomZoom,
        RandomShear, and RandomTranslation.

        The user can provide a list of layers to be used in the data
        augmentation process, however, it must be a list of Keras layers.

        Returns:
            augmenter: A data augmentation generator.
        """
        if layers_list is not None:
            if not isinstance(layers_list, list) or not all(
                [
                    isinstance(layer, keras.layers.Layer)
                    for layer in layers_list
                ]
            ):
                raise ValueError(
                    'Data generator must be a list of Keras layers.'
                )

        data_aug = layers_list
        if data_aug is None:
            data_aug = [
                keras.layers.RandomFlip(),
                keras.layers.RandomRotation(
                    0.3,
                    fill_mode='constant',
                    fill_value=random.randint(0, 255),
                ),
                keras.layers.RandomZoom(
                    (-0.2, 0.4),
                    fill_mode='constant',
                    fill_value=random.randint(0, 255),
                ),
                keras.layers.RandomShear(
                    0.3,
                    fill_mode='constant',
                    fill_value=random.randint(0, 255),
                ),
                keras.layers.RandomTranslation(
                    (-0.3, 0.3),
                    0.1,
                    fill_mode='constant',
                    fill_value=random.randint(0, 255),
                ),
                keras.layers.RandomBrightness(0.3),
                keras.layers.GaussianNoise(0.6),
            ]

        def augmenter(images):
            for op in data_aug:
                images = op(images)

            return images

        return augmenter

    def collect_training_samples(self, num_samples: int = 30):
        """
        Collects a batch of training samples for visualization purposes.

        Args:
            num_samples (int, optional): The number of samples to collect.
            Defaults to 30.

        Returns:
            np.ndarray: A batch of training samples.
        """
        sample = []

        for i in range(num_samples):
            sample.append(next(iter(self.dataset['train']))[0].numpy())
            if len(np.concatenate(sample, axis=0)) >= num_samples:
                break
        # next(iter(self.dataset['train']))[0].numpy()[0:num_samples]
        return np.concatenate(sample, axis=0)[:num_samples]

    def _initialize_model(self, architecture: ModelArchitect, kwargs):
        """
        Initialize the model using the provided architecture.

        Args:
            architecture (ModelArchitect): The model architecture to use.
        """
        if kwargs.get('architecture') is None:
            default = SmallXception(
                img_shape=self.img_shape, num_classes=self.num_classes
            )
            self.architecture = default
            self.model = default.get_model()
        else:
            self.architecture = kwargs['architecture']
            self.model = self.architecture.get_model()

    def _initialize_metrics(self, kwargs):
        """
        Initialize the metrics based on the number of classes.
        """
        self.loss = kwargs.get('loss', keras.losses.CategoricalCrossentropy())
        self.metrics = kwargs.get(
            'metrics', [keras.metrics.CategoricalAccuracy(name='acc')]
        )
        self.optimizer = kwargs.get(
            'optimizer',
            keras.optimizers.Adam(
                keras.optimizers.schedules.ExponentialDecay(
                    initial_learning_rate=0.001,
                    decay_steps=10,
                    decay_rate=0.5,
                )
            ),
        )

    def _define_model_name(self, kwargs):
        time = datetime.datetime.now().strftime('%d%m%Y-%H%M%S')
        ds_name = os.path.basename(os.path.normpath(self.dataset_path))
        modality = self.architecture.modality
        self.model_name = (
            f'mod-{modality}-dataset-{ds_name}-timestamp-{time}.keras'
        )
        if 'model_name' in kwargs:
            self.model_name = kwargs['model_name']

    def _collect_dataset_class_weigth(self, dataset):
        """
        Collects the class weights based on the dataset proportions.
        This helps to balance the training process when the dataset is
        unbalanced.
        """
        class_counts = np.zeros(self.num_classes)
        for _, labels in dataset['train']:
            class_counts += np.sum(labels.numpy(), axis=0)

        total_samples = np.sum(class_counts)
        self.class_weights = {
            i: total_samples / (self.num_classes * count)
            for i, count in enumerate(class_counts)
        }
