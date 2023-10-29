import type { AstroGlobal } from 'astro';

type Token = {
	access_token: string;
	token_type: string;
};

type Method = 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE';

export const getToken = (Astro: AstroGlobal) => {
	return Astro.cookies.get('token')?.json() as Token;
};

export const f = async ({
	url,
	token,
	method = 'GET',
	contentType,
	body,
	json = true,
}: {
	url: string;
	token?: Token;
	method?: Method;
	contentType?: 'application/json';
	body?: string;
	json?: boolean;
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

	console.log(params);

	const response = await fetch(url, params);

	const data = json ? await response.json() : await response.text();

	return { data, response };
};
