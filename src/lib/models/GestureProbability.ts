/**
 * Represents the probability of a recognized gesture (letter).
 * Contains the identified letter and the confidence score (probability) from the classifier.
 */
export class GestureProbability {
	letter: string;
	probability: number;

	/**
	 * Creates an instance of GestureProbability.
	 * @param letter The recognized letter/gesture label.
	 * @param probability The associated probability score.
	 */
	constructor(letter: string, probability: number) {
		this.letter = letter;
		this.probability = probability;
	}
}
