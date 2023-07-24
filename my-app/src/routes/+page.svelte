<script>
  import GridItem from "./GridItem.svelte";
  import { complete } from "./complete.js";
  import { userPrompt, grid, systemPrompt } from "../store.js";
  import { mutate } from "./mutate";

  $: promptVariables = $userPrompt
    .match(/\{(.*?)\}/g)
    ?.map((v) => v.slice(1, -1));
  $: console.log(promptVariables);
  $: dataVariables = [];

  async function sendPrompt() {
    const mutatePrompts = await mutate($userPrompt, $systemPrompt);
    grid.set(mutatePrompts.map((p) => ({ prompt: p, completion: "" })));
    await complete(mutatePrompts, $systemPrompt, dataVariables);
  }
</script>

<h1 class="text-2xl font-bold">PromptBreeder</h1>
<div class="flex flex-row h-full p-8">
  <div class="w-[45%] h-full">
    <label for="userPrompt">Input Prompt</label>
    <textarea
      rows="10"
      id="userPrompt"
      type="text"
      bind:value={$userPrompt}
      placeholder="Insert the prompt here"
      class="block p-2.5 border border-slate-500 rounded w-full text-sm text-gray-900 focus:ring-blue-300"
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
    <label for="systemPrompt">Additional Instructions</label>
    <textarea
      type="text"
      rows="5"
      id="systemPrompt"
      bind:value={$systemPrompt}
      placeholder={$systemPrompt}
      class="block p-2.5 border border-slate-500 rounded w-full text-sm text-gray-900 focus:ring-blue-300"
    />
    <button
      on:click={sendPrompt}
      class="px-4 py-2 my-4 font-bold text-white bg-blue-500 rounded-lg hover:bg-blue-700"
    >
      Mutate
    </button>
  </div>
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
</div>
