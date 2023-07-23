<script>
  import GridItem from "./GridItem.svelte";
  import { complete } from "./complete.js";
  import { userPrompt, grid } from "../store.js";
  let systemPrompt = "Mutate the user prompt into four new prompts.";

  $: promptVariables = $userPrompt
    .match(/\{(.*?)\}/g)
    ?.map((v) => v.slice(1, -1));
  $: console.log(promptVariables);
  $: dataVariables = [];

  async function sendPrompt() {
    await complete($userPrompt, systemPrompt, dataVariables);
  }

  // async function complete() {
  //   const response = await fetch("http://localhost:8000/complete", {
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json",
  //     },
  //     body: JSON.stringify({
  //       system_message: systemPrompt,
  //       user_message: $userPrompt,
  //       inputs: dataVariables,
  //     }),
  //   });

  //   if (!response.ok) {
  //     throw new Error("HTTP error " + response.status);
  //   }

  //   let reader = response.body.getReader();
  //   let decoder = new TextDecoder();

  //   // streamed_response = "";

  //   while (true) {
  //     let { value, done } = await reader.read();
  //     if (done) {
  //       break;
  //     }
  //     let decoded_value = decoder.decode(value, { stream: true });
  //     let lines = decoded_value.split("\n").filter(Boolean);

  //     lines.forEach((line) => {
  //       let { text, box_idx } = JSON.parse(line);
  //       arr[box_idx] += text;
  //       arr = [...arr];
  //     });
  //   }
  // }
</script>

<main class="h-full">
  <h1 class="text-2xl font-bold">PromptBreeder</h1>
  <div class="flex flex-row items-start w-full px-8 py-8">
    <section class="w-1/4 mr-4">
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
      <label for="systemPrompt">Mutate Prompt</label>
      <textarea
        type="text"
        rows="10"
        id="systemPrompt"
        bind:value={systemPrompt}
        placeholder={systemPrompt}
        class="block p-2.5 border border-slate-500 rounded w-full text-sm text-gray-900 focus:ring-blue-300"
      />
      <button
        on:click={sendPrompt}
        class="px-4 py-2 font-bold text-white bg-blue-500 rounded hover:bg-blue-700"
      >
        Mutate
      </button>
    </section>
    <div class="container grid grid-cols-2 gap-4 m-auto">
      {#each $grid as item}
        <GridItem {...item} />
      {/each}
    </div>
  </div>
</main>

<style>
  main {
    height: 100%;
  }
  label {
    color: slategray;
  }
</style>
