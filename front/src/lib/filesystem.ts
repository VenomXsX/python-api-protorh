import * as fs from 'fs';
import * as path from 'path';
import { url } from './api';

// define paths
const PATH = path.resolve('./public');
const file_path = path.resolve(PATH, 'openapi.json');

const checkFile = async () => {
	// if exist then delete it
	if (fs.existsSync(file_path)) {
		fs.rmSync(file_path, { force: true });
	}
	// download openapi.json
	const response = await fetch(`${url}/openapi.json`);
	const json = await response.json();
	fs.writeFileSync(file_path, JSON.stringify(json, null, 2));
};

export { checkFile };
