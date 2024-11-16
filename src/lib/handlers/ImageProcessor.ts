// https://github.com/kinivi/hand-gesture-recognition-mediapipe
import { Landmark2d, Landmark3d } from '$lib/models/Landmark';

/**
 * Processes the extracted landmarks from MediaPipe
 * @param landmarks Array of 3D landmarks
 * @param imageWidth Video frame width
 * @param imageHeight Video frame height
 * @returns number[] to be used for classification
 */
export function processLandmarks(
	landmarks: Landmark3d[],
	imageWidth: number,
	imageHeight: number
): number[] {
	return calcRelativeLandmarks(calcAbsolutePositions(landmarks, imageWidth, imageHeight));
}

/**
 * Converts landmark coordinates to absolute pixel positions
 * @param landmarks Array of 3D landmarks
 * @param imageWidth Video frame width
 * @param imageHeight Video frame height
 * @returns Array of 2D landmarks - pixel coordinates
 */
function calcAbsolutePositions(
	landmarks: Landmark3d[],
	imageWidth: number,
	imageHeight: number
): Landmark2d[] {
	const newLandmarks = [];

	for (const landmark of landmarks) {
		const x = Math.min(Math.floor(landmark.x * imageWidth), imageWidth - 1);
		const y = Math.min(Math.floor(landmark.y * imageHeight), imageHeight - 1);
		//let z = landmark.z;
		newLandmarks.push(new Landmark2d(x, y));
	}

	return newLandmarks;
}

/**
 * Normalizes landmarks relative to the base (wrist) position
 * Makes the model translation-invariant
 * @param landmarks Array of absolute position landmarks
 * @returns Flattened array of normalized coordinates
 */
function calcRelativeLandmarks(landmarks: Landmark2d[]): number[] {
	const tempLandmarkList = structuredClone(landmarks);

	let baseX: number = 0;
	let baseY: number = 0;

	// Normalize positions relative to wrist
	for (let index = 0; index < tempLandmarkList.length; index++) {
		const landmarkPoint = tempLandmarkList[index];

		if (index === 0) {
			baseX = landmarkPoint.x;
			baseY = landmarkPoint.y;
		}

		tempLandmarkList[index].x = tempLandmarkList[index].x - baseX;
		tempLandmarkList[index].y = tempLandmarkList[index].y - baseY;
	}

	// Flatten to 1D array for model input
	const flattenedLandmarkList = [];
	for (let index = 0; index < tempLandmarkList.length; index++) {
		flattenedLandmarkList.push(tempLandmarkList[index].x);
		flattenedLandmarkList.push(tempLandmarkList[index].y);
	}

	// Normalize
	const absValues = flattenedLandmarkList.map(Math.abs);
	const maxValue: number = Math.max(...absValues);

	return flattenedLandmarkList.map((val) => val / maxValue);
}
