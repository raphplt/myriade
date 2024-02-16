<div class="flex flex-col gap-5 items-center mx-auto w-full h-[100vh] mt-16">
  <img src={logo} alt="logo" class="inline-block" />
  <form class="flex items-center justify-center gap-5" on:submit|preventDefault={handleSubmit}>
    <input bind:value={searchQuery} type="text" placeholder="Rechercher..." class="w-96 h-12 px-4 border-2 border-gray-300 rounded-md" />
    <button type="submit" class="w-12 h-12 bg-[#104817] text-white rounded-2xl">
      <Icon icon="akar-icons:search" class="w-6 h-6 inline-block" />
    </button>
  </form>
    {#if searchResults && searchResults.length > 0}
      <div class="mt-5 w-1/3">
        <h2 class="text-lg font-bold">Résultats de la recherche :</h2>
        <ul>
          {#each searchResults as result}
          <div>
            <p class="text-sm text-gray-500 mb-5"> {result.documents.length} {result.documents.length > 1 ? "résultats trouvés.": "résultat trouvé."}</p>
            {#each result.documents as doc}
              <div class="bg-slate-200 p-4 rounded-lg mb-3">
                <a href={doc.url} target="_blank" >
                  <span class="text-blue-800">{truncate(doc.url, 50)}</span>
                  
                  <h3 class="text-green-800">{doc.details.title}</h3>
                </a>
                <p>{doc.details.content}</p>
              </div>
            {/each}
          </div>
        {/each}
        </ul>
      </div>
    {:else if searchResults && searchResults.length === 0}
      <p>Aucun résultat trouvé.</p>
    {/if}
  
</div>

<script>
  import logo from "../assets/logo.png";
  import Icon from '@iconify/svelte';
	import { fetchData } from "./page";

  let searchQuery = ""; 
  /**
		* @type {string | any[] | null}
		*/
  let searchResults = null;


  async function handleSubmit() {
    try {
      const data = await fetchData(searchQuery);
      searchResults = data.results;
       console.log("caca", searchResults)
    } catch (error) {
      console.error(error);
    }
  }

  /**
		* @param {string} str
		* @param {number} n
		*/
  function truncate(str, n) {
    return str.length > n ? str.substr(0, n - 1) + "..." : str;
  }

</script>
