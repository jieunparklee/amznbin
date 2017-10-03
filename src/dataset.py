import collections
import json
import random

import tensorflow as tf

import jsondic
from constants import TOTAL_DATA_SIZE, VALIDATION_SIZE, TEST_SIZE, RANDOM_SPLIT_FILE


class DataSet(object):
    def __init__(self,
                 input_list):
        self._input_list = input_list
        self._num_examples = len(input_list)
        self._epochs_completed = 0
        self._index_in_epoch = 0

    @property
    def images(self):
        # TODO : Check memory limit
        return self._get_images(0, self._num_examples)

    @property
    def labels(self):
        # TODO : Check memory limit
        return self._get_labels(0, self._num_examples)

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_completed(self):
        return self._epochs_completed

    def next_batch(self, batch_size):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Shuffle the data
            random.shuffle(self._input_list)
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch

        return self._get_images(start, end), self._get_labels(start, end)

    def _get_images(self, start, end):
        images = []
        # TODO
        return images

    def _get_labels(self, start, end):
        return jsondic.json2tv(self._input_list[start:end])


def load_dataset():
    num_training = TOTAL_DATA_SIZE - (VALIDATION_SIZE + TEST_SIZE)
    num_validation = VALIDATION_SIZE
    num_test = TEST_SIZE

    print('train:{0}, validation:{1}, test:{2}'.format(num_training, num_validation, num_test))

    if not tf.gfile.Exists(RANDOM_SPLIT_FILE):
        make_random_split(num_training, num_validation, num_test)
    with open(RANDOM_SPLIT_FILE, 'r') as random_split_file:
        random_split_json = json.load(random_split_file)

    train = DataSet(random_split_json.get('train'))
    validation = DataSet(random_split_json.get('validation'))
    test = DataSet(random_split_json.get('test'))

    ds = collections.namedtuple('Datasets', ['train', 'validation', 'test'])
    return ds(train=train, validation=validation, test=test)


# Randomly split the whole list into train, validation, and test set.
def make_random_split(train_size, validation_size, test_size):
    print('make new random_split.json for train:{0}, validation:{1}, test:{2}'.format(train_size, validation_size, test_size))
    random_list = list(range(1, TOTAL_DATA_SIZE + 1))
    random.shuffle(random_list)
    result = {
        'train': random_list[:train_size],
        'validation': random_list[train_size:train_size + validation_size],
        'test': random_list[train_size + validation_size:],
    }
    with open(RANDOM_SPLIT_FILE, 'w') as random_split_file:
        json.dump(result, random_split_file)
