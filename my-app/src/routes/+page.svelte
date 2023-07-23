<script>
  let userPrompt = "";
  let systemPrompt = "Mutate the user prompt into four new prompts.";

  $: promptVariables = userPrompt
    .match(/\{(.*?)\}/g)
    ?.map((v) => v.slice(1, -1));
  $: console.log(promptVariables);
  $: dataVariables = [];

  let arr = ["", "", "", ""];

  async function sendPrompt() {
    await complete();
  }

  async function complete() {
    const response = await fetch("http://localhost:8000/complete", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        system_message: systemPrompt,
        user_message: userPrompt,
        inputs: dataVariables,
      }),
    });

    if (!response.ok) {
      throw new Error("HTTP error " + response.status);
    }

    let reader = response.body.getReader();
    let decoder = new TextDecoder();

    // streamed_response = "";

    while (true) {
      let { value, done } = await reader.read();
      if (done) {
        break;
      }
      let decoded_value = decoder.decode(value, { stream: true });
      let lines = decoded_value.split("\n").filter(Boolean);

      lines.forEach((line) => {
        let { text, box_idx } = JSON.parse(line);
        arr[box_idx] += text;
        arr = [...arr];
      });
    }
  }
</script>

<main class="h-full">
  <h1 class="text-2xl font-bold">PromptBreeder</h1>
  <div class="flex items-start flex-row px-8 py-8 w-full">
    <section class="w-1/4 mr-4">
      <label for="userPrompt">Input Prompt</label>
      <textarea
        rows="10"
        id="userPrompt"
        type="text"
        bind:value={userPrompt}
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
              class="input border border-gray-500 rounded"
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
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Mutate
      </button>
    </section>
    <div class="container m-auto grid grid-cols-2 gap-4">
      {#each arr as item}
        <div class="sticky top-15 z-0 flex h-24 flex-shrink-0 bg-neutral-600 bg-opacity-25 backdrop-blur-3xl">
          <h1 class="tile-marker overflow-y-scroll">{item}</h1>
        </div>
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
