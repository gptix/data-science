#!/usr/bin/env python

import numpy

from tensorflow_core.keras.preprocessing import image
from tensorflow_core.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow_core.keras.applications.resnet50 import ResNet50


def instantiate_model():
	return (ResNet50(weights='imagenet'))


def load(img_path):
	return (image.load_img(img_path, target_size=(224, 224)))


def preprocess(img):
	arr = image.img_to_array(img)
	expanded = numpy.expand_dims(arr, axis=0)
	preprocessed = preprocess_input(expanded)
	return (preprocessed)


def predict(img_path: str, persistent: 'Persistent', classification_threshold: float = 0.3) -> dict:
	x = preprocess(load(img_path))
	model = persistent.models['resnet']
	feats = model.predict(x)
	results = decode_predictions(feats)[0]
	output = [
		{
			'object': str(pred[1]),
			'confidence': str(pred[2]),
		} for pred in results if pred[2] >= classification_threshold
	]

	return (output)


