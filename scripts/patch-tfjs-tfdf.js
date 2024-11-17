import fs from 'fs';
import path from 'path';

const packagePath = path.join(
	process.cwd(), // Current working directory
	'node_modules',
	'@tensorflow',
	'tfjs-tfdf',
	'package.json'
);

try {
	const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf-8'));
	packageJson.type = 'module'; // Add "type": "module"
	fs.writeFileSync(packagePath, JSON.stringify(packageJson, null, 2));
	console.log('Patched @tensorflow/tfjs-tfdf/package.json successfully.');
} catch (error) {
	console.error('Failed to patch @tensorflow/tfjs-tfdf/package.json:', error);
}
