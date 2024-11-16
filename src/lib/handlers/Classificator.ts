import type { GestureProbability } from '$lib/models/GestureProbability';

/**
 * Interface for classificator implementation
 */
export interface Classificator {
	/**
	 * Method to check if classificator is loaded
	 * @returns bool which is true if classification is ready to be used
	 */
	ready(): boolean;

	/**
	 * Loads the Classificator model for gesture classification
	 */
	load(): Promise<void>;

	/**
	 * Classifies hand gestures using implemented model
	 * @param landmarks Flattened, normalized landmark coordinates
	 * @returns Array of probabilities for each supported gesture
	 */
	predict(landmarks: number[]): Promise<GestureProbability[]>;
}
