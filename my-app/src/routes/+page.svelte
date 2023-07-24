<script>
  import GridItem from "./GridItem.svelte";
  import { complete } from "./complete.js";
  import { userPrompt, grid, systemPrompt } from "../store.js";
  import { mutate } from "./mutate";
  let mutated = false;
  $: promptVariables = $userPrompt
    .match(/\{(.*?)\}/g)
    ?.map((v) => v.slice(1, -1));
  $: console.log(promptVariables);
  $: dataVariables = [];

  async function sendPrompt() {
    mutated = true;
    const mutatePrompts = await mutate($userPrompt, $systemPrompt);
    grid.set(mutatePrompts.map((p) => ({ prompt: p, completion: "" })));
    await complete(mutatePrompts, $systemPrompt, dataVariables);
  }
</script>

<div class="h-full p-4 space-y-8">
  <h1 class="text-4xl font-bold">pMux</h1>
  <div class="flex flex-row h-full space-x-4">
    <div class="h-full space-y-4 left-side {mutated ? 'collapsed' : ''} ">
      <div>
        <label for="userPrompt">Input Prompt</label>
        <textarea
          rows="10"
          id="userPrompt"
          type="text"
          bind:value={$userPrompt}
          placeholder="Insert the prompt here"
          class="block p-2.5 border bg-gray-100 rounded w-full text-sm text-gray-900 focus:ring-blue-300"
        />
        {#if promptVariables}
          <h3>Prompt Variables</h3>
          {#each promptVariables as v, i}
            <div
              class="flex flex-col p-2.5 items-start justify-start gap-1 bg-gray-100 rounded"
            >
              <label for={`input-${i}`} class="text-blue-400"
                >{"{ " + i + " }"}</label
              >
              <textarea
                rows="4"
                id={`input-${i}`}
                type="text"
                bind:value={dataVariables[i]}
                placeholder="Variable data"
                class="block w-full text-sm text-gray-900 border p-2.5 rounded bg-inherit focus:ring-blue-300"
              />
            </div>
          {/each}
        {/if}
      </div>

      <div>
        <label for="systemPrompt">Additional Instructions</label>
        <textarea
          type="text"
          rows="5"
          id="systemPrompt"
          placeholder="Add additional instructions to modify the prompt"
          bind:value={$systemPrompt}
          class="block p-2.5 border bg-gray-100 rounded w-full text-sm text-gray-900 focus:ring-blue-300"
        />
      </div>
      <button
        on:click={sendPrompt}
        class="px-4 py-2 my-4 font-bold text-white bg-blue-500 rounded-lg hover:bg-blue-700"
      >
        Mutate
      </button>
    </div>
    {#if mutated}
      <div class="flex flex-row w-full">
        <div class="flex flex-col w-full h-full">
          <GridItem {...$grid[0]} />
          <GridItem {...$grid[1]} />
        </div>
        <div class="flex flex-col w-full h-full">
          <GridItem {...$grid[2]} />
          <GridItem {...$grid[3]} />
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  .left-side {
    transition: width 0.3s ease-in;
    width: 100%;
  }
  .left-side.collapsed {
    width: 30%;
  }
</style>
