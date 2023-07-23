<script>
  import { complete } from "./complete.js";
  let userPrompt = "";
  let systemPrompt = "THIS IS THE SYSTEM PROMPT";

  $: promptVariables = userPrompt
    .match(/\{(.*?)\}/g)
    ?.map((v) => v.slice(1, -1));
  $: console.log(promptVariables);
  $: dataVariables = [];

  let gridArray = ["", "", "", ""];

  async function sendPrompt() {
    await complete(gridArray, userPrompt, systemPrompt, promptVariables);
  }
</script>

<h1 class="text-2xl font-bold">PromptBreeder</h1>
<main class="flex items-start flex-row px-12 py-8 w-full">
  <section class="w-1/4">
    <h3>Input Prompt</h3>
    <textarea
      type="text"
      bind:value={userPrompt}
      placeholder="Insert the prompt here"
      class="input border border-slate-500 rounded w-full"
    />
    {#if promptVariables}
      {#each promptVariables as v, i}
        <div class="flex flex-row items-center justify-start">
          <span class="">{i} :</span>
          <input
            bind:value={dataVariables[i]}
            class="input border border-gray-500 rounded"
          />
        </div>
      {/each}
    {/if}
    <h3>Meta Prompt</h3>
    <textarea
      type="text"
      bind:value={systemPrompt}
      placeholder={systemPrompt}
      class="input border border-slate-500 rounded w-full"
    />
    <button
      on:click={sendPrompt}
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    >
      Generate
    </button>
  </section>
  <section class="flex w-3/4 flex-wrap">
    {#each gridArray as item}
      <div class="max-w-lg bg-slate-50">{item}</div>
    {/each}
  </section>
</main>

<style>
</style>
