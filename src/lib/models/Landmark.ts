/**
 * Represents a 2-dimensional landmark point.
 * Typically used for coordinates in pixel space on the video frame.
 */
export class Landmark2d {
	x: number;
	y: number;

	/**
	 * Creates an instance of Landmark2d.
	 * @param x The x-coordinate.
	 * @param y The y-coordinate.
	 */
	constructor(x: number, y: number) {
		this.x = x;
		this.y = y;
	}
}

/**
 * Represents a 3-dimensional landmark point, inheriting from Landmark2d.
 */
export class Landmark3d extends Landmark2d {
	z: number;

	/**
	 * Creates an instance of Landmark3d.
	 * @param x The x-coordinate.
	 * @param y The y-coordinate.
	 * @param z The z-coordinate (depth).
	 */
	constructor(x: number, y: number, z: number) {
		super(x, y);
		this.z = z;
	}
}
