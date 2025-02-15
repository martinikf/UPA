// Configuration constants
export const MIN_GROUP_LENGTH = 6;
const SPACE_INSERT_THRESHOLD = 20;
const MULTI_CHAR_TOKENS = ['Ch'];
const ERROR_CONTEXT_SIZE = 1; // Characters to check around mismatches

export function convertToFrequencyFormat(input: string): string {
	// Tokenize input with multi-character support
	const tokens: string[] = [];
	let i = 0;
	while (i < input.length) {
		let matched = false;
		for (const token of MULTI_CHAR_TOKENS) {
			if (input.substring(i, token.length) === token) {
				tokens.push(token);
				i += token.length;
				matched = true;
				break;
			}
		}
		if (!matched) {
			tokens.push(input[i]);
			i++;
		}
	}

	let result = '';
	let currentToken = tokens[0];
	let count = 1;

	for (let i = 1; i <= tokens.length; i++) {
		const isValidExtension =
			i < tokens.length &&
			(tokens[i] === currentToken ||
				(i > ERROR_CONTEXT_SIZE &&
					i < tokens.length - ERROR_CONTEXT_SIZE &&
					tokens[i - ERROR_CONTEXT_SIZE] === currentToken &&
					tokens[i + ERROR_CONTEXT_SIZE] === currentToken));

		if (isValidExtension) {
			count++;
		} else {
			if (
				count >= MIN_GROUP_LENGTH ||
				((currentToken.toLowerCase() === 'g' || currentToken.toLowerCase() === 'f') &&
					count >= MIN_GROUP_LENGTH / 2)
			) {
				result += currentToken;
				if (count >= SPACE_INSERT_THRESHOLD) {
					result += ' ';
				}
			}

			if (i < tokens.length) {
				currentToken = tokens[i];
				count = 1;
			}
		}
	}

	return result;
}
