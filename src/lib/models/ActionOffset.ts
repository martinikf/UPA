/**
 * Enum defining prefixes for animation action names within the 3D model.
 * Used to differentiate between different animation sets (e.g., one-handed vs. two-handed alphabet).
 * The specific values depend entirely on the naming convention used when creating the animations in the 3D model file.
 */
export enum ActionOffset {
	/** Prefix for standard one-handed finger alphabet letter animations. */
	ActionLetter = 'ActionLetter',
	/** Prefix for Czech two-handed finger alphabet letter animations. */
	CZ2ActionLetter = 'CZ2ActionLetter'
}
