import type { AstroGlobal } from 'astro';

type Token = {
	access_token: string;
	token_type: string;
};

type User = {
	email: string;
	role: 'admin' | 'manager' | 'user';
};

type Session = {
	user: User | null;
	token?: Token;
};

type Method = 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE';

export const useSession = (Astro: AstroGlobal) => {
	const session: Session = Astro.cookies.get('session')?.json();
	return session || { user: null };
};

type DataFormat = 'json' | 'text' | 'blob';

const getResponse = async (response: Response, dataFormat: DataFormat) => {
	if (dataFormat === 'json') return response.json();
	if (dataFormat === 'text') return response.json();
	if (dataFormat === 'blob') return response.blob();
};

export const f = async ({
	url,
	token,
	method = 'GET',
	contentType,
	body,
	dataFormat = 'json',
}: {
	url: string;
	token?: Token;
	method?: Method;
	contentType?: 'application/json' | 'multipart/form-data; boundary=---011000010111000001101001';
	body?: string | FromData;
	dataFormat?: DataFormat;
}) => {
	const headers: {
		Authorization?: string;
		'Content-Type'?: string;
	} = {};
	if (token !== undefined)
		headers['Authorization'] = `${token.token_type} ${token.access_token}`;
	if (contentType !== undefined) headers['Content-Type'] = contentType;

	const params: {
		method?: Method;
		headers?: typeof headers;
		body?: string;
	} = {};
	if (Object.keys(headers).length !== 0) params['headers'] = headers;
	if (body) params['body'] = body;
	if (method !== 'GET') params['method'] = method;

	const response = await fetch(url, params);

	const data = await getResponse(response, dataFormat);

	return { data, response };
};
