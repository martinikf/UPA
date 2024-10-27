// 2D landmark
export class Landmark2d {
	x: number;
	y: number;

	constructor(x: number, y: number) {
		this.x = x;
		this.y = y;
	}
}

// 3D landmark, adds the z property
export class Landmark3d extends Landmark2d {
	z: number;

	constructor(x: number, y: number, z: number) {
		super(x, y);
		this.z = z;
	}
}
