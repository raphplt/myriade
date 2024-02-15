export async function fetchFromAPI(endpoint: any) {
	const API_URL = import.meta.env.API_URL;

	const response = await fetch(`${API_URL}/${endpoint}`);
	if (!response.ok) {
		throw new Error(`Erreur HTTP! Statut: ${response.status}`);
	}
	return await response.json();
}

export async function fetchFromAPIWithQuery(endpoint: any, query: any) {
	const API_URL = import.meta.env.API_URL;

	const response = await fetch(
		`http://127.0.0.1:8000/${endpoint}?query=${query}`
	);
	if (!response.ok) {
		throw new Error(`Erreur HTTP! Statut: ${response.status}`);
	}
	return await response.json();
}
