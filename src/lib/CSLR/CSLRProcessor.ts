export class CSLRProcessor {
	rawString: string;

	similarLetterSets = [
		['a', 'e', 's'],
		['h', 'u', 'v'],
		['k', 'l'],
		['t', 'f', 'b'],
		['c', 'o', 'g']
	];

	constructor(_rawString: string) {
		this.rawString = _rawString;
	}

	getLLMInput() {}

	/// Slices the text into blocks of similar letters with their frequency
	sliceText() {
		let block: { key: string; frequency: number };
		for (let i = 0; i < this.rawString.length; i++) {}
	}
}
