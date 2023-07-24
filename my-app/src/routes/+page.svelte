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
  <div class="flex flex-row h-full">
    <div class="left-side w-[45%] h-full space-y-4">
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
            <div class="flex flex-row items-center justify-start">
              <label for={`input-${i}`} class="">{i}</label>
              <input
                id={`input-${i}`}
                bind:value={dataVariables[i]}
                class="border border-gray-500 rounded input"
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
  .left-side * {
    transition: flex 1s ease-in-out;
    transform-origin: top left;
  }
</style>
