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
  class="sticky top-15 z-0 flex h-24 flex-shrink-0 bg-neutral-600 bg-opacity-25 backdrop-blur-3xl"
  on:click={onClick}
>
  <h1 class="tile-marker overflow-y-scroll">
    {promptSide ? prompt : completion}
  </h1>
</div>
