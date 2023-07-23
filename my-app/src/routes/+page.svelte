<script>
  let prompt = "";

  $: promptVariables = prompt.match(/\{(.*?)\}/g)?.map((v) => v.slice(1, -1));
  $: console.log(promptVariables);
  $: dataVariables = [];

  function sendPrompt() {
    console.log(prompt);
    for (let i = 0; i < promptVariables.length; i++) {
      console.log(promptVariables[i], dataVariables[i]);
    }
  }
</script>

<h1 class="text-2xl font-bold">PromptBreeder</h1>
<main class="flex items-start flex-col px-12 py-8 w-full">
  <section>
    <h3>Input Prompt</h3>
    <input
      bind:value={prompt}
      placeholder="Insert the prompt here"
      class="input border border-red-500 rounded"
    />
    {promptVariables}
    <h3>Variables</h3>
    <input class="input border border-red-500 rounded" />
    {#if promptVariables}
      {#each promptVariables as v, i}
        <div>Variable {v}</div>
        <input
          bind:value={dataVariables[i]}
          class="input border border-red-500 rounded"
        />
      {/each}
    {/if}
    <button
      on:click={sendPrompt}
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    >
      Generate
    </button>
  </section>
  <!-- <section>
    <div>
      <input class="input border border-red-500 rounded w-3/4" />
    </div>
  </section> -->
</main>

<style>
  .input {
    padding: 0.5rem;
    color: dimgrey;
  }
</style>
