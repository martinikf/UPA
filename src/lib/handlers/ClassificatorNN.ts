// Tensorflow imports
import * as tf from '@tensorflow/tfjs';
import type { LayersModel } from '@tensorflow/tfjs';

import type { Classificator } from '$lib/handlers/Classificator';
import { GestureProbability } from '$lib/models/GestureProbability';

/** Supported letters for gesture recognition */
const letters = [
	'A',
	'B',
	'C',
	'D',
	'E',
	'F',
	'G',
	'H',
	'Ch',
	'I',
	'J',
	'K',
	'L',
	'M',
	'N',
	'O',
	'P',
	'Q',
	'R',
	'S',
	'T',
	'U',
	'V',
	'W',
	'X',
	'Y',
	'Z',
	'None'
];

/**
 * Classificator based on tensor flow neural network.
 */
export class ClassificatorNN implements Classificator {
	/** TensorFlow.js gesture classification model */
	tfModel: LayersModel | undefined;

	constructor() {}

	/**
	 * Method to check if classificator is loaded
	 * @returns bool which is true if classification is ready to be used
	 */
	ready() {
		return this.tfModel != undefined;
	}

	/**
	 * Loads the TensorFlow.js model for gesture classification
	 */
	async load() {
		if (this.tfModel === undefined) {
			this.tfModel = await tf.loadLayersModel('models/tfjsmodel/model.json');
			// https://github.com/tensorflow/tfjs/tree/master/tfjs-backend-webgpu
		}
	}

	/**
	 * Classifies hand gestures using TensorFlow model
	 * @param landmarks Flattened, normalized landmark coordinates
	 * @returns Array of probabilities for each supported gesture
	 */
	async predict(landmarks: number[]): Promise<GestureProbability[]> {
		if (this.tfModel === undefined) {
			await this.load();
			if (this.tfModel === undefined) {
				throw new Error('Model not loaded');
			}
		}

		const input = tf.tensor(landmarks, [1, 42]);
		const output = this.tfModel.predict(input) as tf.Tensor;

		const probabilities = output.dataSync() as Float32Array;

		//Convert probabilities to GestureProbability[]
		const gestureProbabilities: GestureProbability[] = [];
		for (let i = 0; i < probabilities.length; i++) {
			gestureProbabilities.push(new GestureProbability(letters[i], probabilities[i]));
		}
		return gestureProbabilities;
	}
}
