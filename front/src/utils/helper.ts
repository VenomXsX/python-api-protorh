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

	const response = await fetch(url, params);

	const data = json ? await response.json() : await response.text();

	return { data, response };
};
