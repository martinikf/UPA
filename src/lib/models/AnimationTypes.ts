import type * as THREE from 'three';

export type ActionName =
	| 'ActionLetterA'
	| 'ActionLetterAA'
	| 'ActionLetterAd'
	| 'ActionLetterB'
	| 'ActionLetterBB'
	| 'ActionLetterC'
	| 'ActionLetterCC'
	| 'ActionLetterCc'
	| 'ActionLetterCh'
	| 'ActionLetterChCh'
	| 'ActionLetterD'
	| 'ActionLetterDc'
	| 'ActionLetterDD'
	| 'ActionLetterE'
	| 'ActionLetterEc'
	| 'ActionLetterEd'
	| 'ActionLetterEE'
	| 'ActionLetterF'
	| 'ActionLetterFF'
	| 'ActionLetterG'
	| 'ActionLetterGG'
	| 'ActionLetterH'
	| 'ActionLetterHH'
	| 'ActionLetterI'
	| 'ActionLetterId'
	| 'ActionLetterII'
	| 'ActionLetterJ'
	| 'ActionLetterJJ'
	| 'ActionLetterK'
	| 'ActionLetterKK'
	| 'ActionLetterL'
	| 'ActionLetterLL'
	| 'ActionLetterM'
	| 'ActionLetterMM'
	| 'ActionLetterN'
	| 'ActionLetterNc'
	| 'ActionLetterNN'
	| 'ActionLetterO'
	| 'ActionLetterOd'
	| 'ActionLetterOO'
	| 'ActionLetterP'
	| 'ActionLetterPP'
	| 'ActionLetterQ'
	| 'ActionLetterQQ'
	| 'ActionLetterR'
	| 'ActionLetterRc'
	| 'ActionLetterRR'
	| 'ActionLetterS'
	| 'ActionLetterSc'
	| 'ActionLetterSS'
	| 'ActionLetterT'
	| 'ActionLetterTc'
	| 'ActionLetterTT'
	| 'ActionLetterU'
	| 'ActionLetterUd'
	| 'ActionLetterUU'
	| 'ActionLetterV'
	| 'ActionLetterVV'
	| 'ActionLetterW'
	| 'ActionLetterWW'
	| 'ActionLetterX'
	| 'ActionLetterXX'
	| 'ActionLetterY'
	| 'ActionLetterYd'
	| 'ActionLetterYY'
	| 'ActionLetterZ'
	| 'ActionLetterZc'
	| 'ActionLetterZZ'
	| 'ActionRest'
	| 'ActionRestToTransition'
	| 'PoseFive'
	| 'PoseLetterA'
	| 'PoseLetterB'
	| 'PoseLetterC'
	| 'PoseLetterCH'
	| 'PoseLetterD'
	| 'PoseLetterE'
	| 'PoseLetterF'
	| 'PoseLetterG'
	| 'PoseLetterH'
	| 'PoseLetterI'
	| 'PoseLetterJ'
	| 'PoseLetterK'
	| 'PoseLetterL'
	| 'PoseLetterM'
	| 'PoseLetterN'
	| 'PoseLetterO'
	| 'PoseLetterP'
	| 'PoseLetterQ'
	| 'PoseLetterR'
	| 'PoseLetterS'
	| 'PoseLetterT'
	| 'PoseLetterU'
	| 'PoseLetterV'
	| 'PoseLetterW'
	| 'PoseLetterX'
	| 'PoseLetterY'
	| 'PoseLetterZ'
	| 'PoseNumber5'
	| 'PosePositionRest'
	| 'PosePositionTransition'
	| 'KeyAction';

export type GLTFResult = {
	nodes: {
		Ch22_Hair: THREE.SkinnedMesh;
		Ch22_Pants: THREE.SkinnedMesh;
		Ch22_Shirt: THREE.SkinnedMesh;
		Ch22_Sneakers: THREE.SkinnedMesh;
		Ch22_Body: THREE.SkinnedMesh;
		mixamorig2Hips: THREE.Bone;
	};
	materials: {
		Ch22_hair: THREE.MeshStandardMaterial;
		Ch22_body: THREE.MeshStandardMaterial;
	};
};
