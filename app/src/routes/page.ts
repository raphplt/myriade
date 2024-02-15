import { fetchFromAPIWithQuery } from "$lib/api";

export async function fetchData(query: string) {
	try {
		const data = await fetchFromAPIWithQuery("search", query);
		console.log("result", data);

		return data;
	} catch (error) {
		console.error(error);
	}
}
