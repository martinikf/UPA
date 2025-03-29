/**
 * Enum defining the supported sign language systems or alphabets within the application.
 */
export enum Language {
	CzechFingerOneHand,
	CzechFingerTwoHand,
	Czech
}

/**
 * Represents a word or sign unit within the application.
 * Contains the text representation, the language system it belongs to,
 * and a flag indicating if the user has marked it as learned.
 */
export class Word {
	/**
	 * Creates an instance of Word.
	 * @param str The string representation of the word or sign.
	 * @param language The language system (e.g., finger alphabet type, sign language).
	 * @param learned A boolean indicating if the user considers this word/sign learned.
	 */
	constructor(
		public str: string,
		public language: Language,
		public learned: boolean
	) {}
}
