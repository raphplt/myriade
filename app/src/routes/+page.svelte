<main class="flex flex-col gap-5 items-center mx-auto w-full h-[100vh] mt-16">
  <img src={Myriade} alt="logo" class="inline-block" />
  <form class="w-1/2 flex items-center justify-center gap-5" on:submit|preventDefault={handleSubmit}>
    <input bind:value={searchQuery} type="text" required placeholder="Rechercher..." class="drop-shadow-sm focus:outline-none w-1/2 h-12 px-4 border-2 border-gray-300 rounded-md focus:border-[#34813f]" />
    <button type="submit" class="w-12 h-12 bg-[#34813f] text-white rounded-xl">
      <Icon icon="akar-icons:search" class="w-6 h-6 inline-block" />
    </button>
  </form>
    {#if searchResults && searchResults.length > 0}
      <div class="mt-5 w-1/3">
        <h2 class="text-lg font-bold">Résultats de la recherche :</h2> 
        <p class="text-sm text-gray-500 mb-5"> {searchResults.length} {searchResults.length > 1 ? "résultats trouvés." : "résultat trouvé."} Temps de calcul : {(time).toFixed(2)} secondes</p>
        <ul>
          {#each searchResults as result}
            <div>
                  <div class="bg-gray-100 p-4 rounded-lg mb-3 drop-shadow-sm">
                    <a href={result.url} target="_blank" >
                      <h3 class="text-green-800">{result.details.title}</h3>
                      <span class="text-blue-800">{truncate(result.url, 50)}</span>
                     
                    </a>
                    <p>{truncate(result.details.content, 95)}</p>
                    <p class="italic text-gray-400 text-sm">Score : {(result.tfidf_score).toFixed(4)}</p>
                  </div>

            </div>
          {/each}

        </ul>
      </div>
    {:else if searchResults && searchResults.length === 0}
      <p>Aucun résultat trouvé.</p>
    {/if}
  
</main>

<script>
  import Icon from '@iconify/svelte';
  import Myriade from "../assets/Myriade.svg"
  import { fetchData } from "./page";

  let searchQuery = ""; 
  /**
   * @type {string | any[] | null}
   */
  let searchResults = null;
  let time = 0;


  async function handleSubmit() {
    try {
      const data = await fetchData(searchQuery);
      searchResults = data.results;
      time = data.time;
    } catch (error) {
      console.error("ERROR", error);
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