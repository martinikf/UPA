export enum Language {
	CzechFingerOneHand,
	CzechFingerTwoHand,
	Czech
}

export class Word {
	constructor(
		public str: string,
		public language: Language,
		public learned: boolean
	) {}
}
