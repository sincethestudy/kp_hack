<script>
  import { userPrompt } from "../store.js";
  export let completion;
  export let prompt;

  let promptSide = false;

  function flip() {
    promptSide = !promptSide;
  }
  function onClick() {
    userPrompt.set(prompt);
  }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
  class="h-full m-1 p-2.5 rounded text-sm bg-opacity-25 bg-gray-300 cursor-pointer"
>
  <div class="flex flex-col justify-between h-full">
    <span class="overflow-y-scroll tile-marker">
      {promptSide ? prompt : completion}
    </span>

    {#if prompt}
      <div
        class="flex flex-row self-end justify-start w-full gap-2 justify-self-end"
      >
        <button on:click={flip} class="p-2 bg-blue-300 rounded"
          >See {promptSide ? "Completion" : "Prompt"}</button
        >
        <button on:click={onClick} class="p-2 bg-green-300 rounded">Use</button>
      </div>
    {/if}
  </div>
</div>
