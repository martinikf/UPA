// src/models/word.ts
export enum Language {
	CzechFingerOneHand,
	CzechFingerTwoHand,
	Czech,
	ASL
}

export class Word {
	constructor(public str: string, public language: Language, public learned: boolean) {
	}
}