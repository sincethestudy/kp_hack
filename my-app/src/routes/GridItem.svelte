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

    flip();
  }
</script>

<div
  class="sticky z-0 flex flex-shrink-0 h-full p-2.5 rounded text-sm bg-opacity-25 top-15 bg-neutral-600 backdrop-blur-3xl"
  on:click={onClick}
>
  <h1 class="overflow-y-scroll tile-marker">
    {promptSide ? prompt : completion}
  </h1>
</div>
