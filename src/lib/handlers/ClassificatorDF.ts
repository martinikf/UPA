import type { Classificator } from '$lib/handlers/Classificator';
import * as tf from '@tensorflow/tfjs-core';
import * as tfdf from '@tensorflow/tfjs-tfdf';
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

//TODO: on reload, throws error: "Cannot use import statement outside a module:
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
		tfdf.setLocateFile((path, base) => {
			return 'https://localhost:5173/inference.wasm';
		});

		if (this.model == undefined)
			this.model = await tfdf.loadTFDFModel('https://localhost:5173/models/tfjsDF/model.json');
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

		const inputDict = {
			f1: tf.tensor([landmarks[0]]),
			f2: tf.tensor([landmarks[1]]),
			f3: tf.tensor([landmarks[2]]),
			f4: tf.tensor([landmarks[3]]),
			f5: tf.tensor([landmarks[4]]),
			f6: tf.tensor([landmarks[5]]),
			f7: tf.tensor([landmarks[6]]),
			f8: tf.tensor([landmarks[7]]),
			f9: tf.tensor([landmarks[8]]),
			f10: tf.tensor([landmarks[9]]),
			f11: tf.tensor([landmarks[10]]),
			f12: tf.tensor([landmarks[11]]),
			f13: tf.tensor([landmarks[12]]),
			f14: tf.tensor([landmarks[13]]),
			f15: tf.tensor([landmarks[14]]),
			f16: tf.tensor([landmarks[15]]),
			f17: tf.tensor([landmarks[16]]),
			f18: tf.tensor([landmarks[17]]),
			f19: tf.tensor([landmarks[18]]),
			f20: tf.tensor([landmarks[19]]),
			f21: tf.tensor([landmarks[20]]),
			f22: tf.tensor([landmarks[21]]),
			f23: tf.tensor([landmarks[22]]),
			f24: tf.tensor([landmarks[23]]),
			f25: tf.tensor([landmarks[24]]),
			f26: tf.tensor([landmarks[25]]),
			f27: tf.tensor([landmarks[26]]),
			f28: tf.tensor([landmarks[27]]),
			f29: tf.tensor([landmarks[28]]),
			f30: tf.tensor([landmarks[29]]),
			f31: tf.tensor([landmarks[30]]),
			f32: tf.tensor([landmarks[31]]),
			f33: tf.tensor([landmarks[32]]),
			f34: tf.tensor([landmarks[33]]),
			f35: tf.tensor([landmarks[34]]),
			f36: tf.tensor([landmarks[35]]),
			f37: tf.tensor([landmarks[36]]),
			f38: tf.tensor([landmarks[37]]),
			f39: tf.tensor([landmarks[38]]),
			f40: tf.tensor([landmarks[39]]),
			f41: tf.tensor([landmarks[40]]),
			f42: tf.tensor([landmarks[41]])
		};

		const output = (await this.model.executeAsync(inputDict)) as tf.Tensor;

		const probabilitiesOff = output.dataSync() as Float32Array;

		// TODO: Figure out why the output is shifted by 28 places (num of categories)
		const probabilities = probabilitiesOff.slice(28, 28 + 28);

		const gestureProbabilities: GestureProbability[] = [];
		for (let i = 0; i < probabilities.length; i++) {
			gestureProbabilities.push(new GestureProbability(letters[i], probabilities[i]));
		}
		return gestureProbabilities;
	}
}
