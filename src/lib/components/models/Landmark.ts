// Base class for shared properties
export class Landmark {
	x: number;
	y: number;

	constructor(x: number, y: number) {
		this.x = x;
		this.y = y;
	}
}

// 2D landmark, no additional properties needed
export class Landmark2d extends Landmark {
	constructor(x: number, y: number) {
		super(x, y);
	}
}

// 3D landmark, adds the z property
export class Landmark3d extends Landmark {
	z: number;

	constructor(x: number, y: number, z: number) {
		super(x, y);
		this.z = z;
	}
}
