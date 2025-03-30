import type { Classificator } from '$lib/handlers/Classificator';
import * as tf from '@tensorflow/tfjs-core';
import { GestureProbability } from '$lib/models/GestureProbability';

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import * as tfdf from '@tensorflow/tfjs-tfdf';

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

export class ClassificatorDF implements Classificator {
	model: tfdf.TFDFModel | undefined = undefined;

	constructor() {}

	/**
	 * Method to check if classificator is loaded
	 * @returns bool which is true if classification is ready to be used
	 */
	ready() {
		return this.model != undefined;
	}

	/**
	 * Loads
	 */
	async load() {
		const baseURL = `${window.location.protocol}//${window.location.host}`;
		tfdf.setLocateFile(() => {
			return `${baseURL}/inference.wasm`;
		});

		if (this.model == undefined)
			this.model = await tfdf.loadTFDFModel(`${baseURL}/models/tfjsDF/model.json`);
	}

	/**
	 * Classifies hand gestures using
	 * @param landmarks Flattened, normalized landmark coordinates
	 * @returns Array of probabilities for each supported gesture
	 */
	async predict(landmarks: number[]): Promise<GestureProbability[]> {
		if (this.model === undefined) {
			await this.load();
			if (this.model === undefined) {
				throw new Error('Model not loaded');
			}
		}

		// Build input
		const inputDict: { [key: string]: tf.Tensor } = {};
		for (let i = 0; i < 42; i++) {
			inputDict[`f${i + 1}`] = tf.tensor([landmarks[i]]);
		}

		// TODO: Throws console warning that it should use only execute, yet execute throws error
		const output = (await this.model.executeAsync(inputDict)) as tf.Tensor;

		// TODO: Figure out why the output is shifted by 28 places (num of categories)
		const probabilitiesOff = (await output.data()) as Float32Array;
		const probabilities = probabilitiesOff.slice(28, 28 + 28);

		const gestureProbabilities: GestureProbability[] = [];
		for (let i = 0; i < probabilities.length; i++) {
			gestureProbabilities.push(new GestureProbability(letters[i], probabilities[i]));
		}
		return gestureProbabilities;
	}
}
