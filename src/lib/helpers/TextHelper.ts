export function replaceCzechDiacriticsAndNormalize(input: string): string {
	const diacriticsMap: { [key: string]: string } = {
		á: 'a',
		č: 'c',
		ď: 'd',
		é: 'e',
		ě: 'e',
		í: 'i',
		ň: 'n',
		ó: 'o',
		ř: 'r',
		š: 's',
		ť: 't',
		ú: 'u',
		ů: 'u',
		ý: 'y',
		ž: 'z'
	};

	return removeFormating(input)
		.split('')
		.map((char) => diacriticsMap[char] || char)
		.join('');
}

export function removeFormating(str: string) {
	return str.trim().toLowerCase();
}

export function keepOnlyLetters(input: string): string {
	return input.replace(/[^\p{L}]/gu, '');
}
