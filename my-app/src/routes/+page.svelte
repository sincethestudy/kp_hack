<script>
  let userPrompt = "";
  let systemPrompt =
    "Summarize content you are provided with for a second-grade student.";

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

<h1 class="text-2xl font-bold">PromptBreeder</h1>
<main class="flex items-start flex-row px-12 py-8 w-full">
  <section class="w-1/4">
    <label for="userPrompt">Input Prompt</label>
    <textarea
      id="userPrompt"
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
    <div class="container m-auto grid grid-cols-2 gap-4">
    {#each arr as item}
      <!-- <div class="max-w-lg bg-slate-50">{item}</div> -->
        <div class="tile bg-teal-500 overflow-y-scroll">
          <h1 class="tile-marker overflow-y-scroll">{item}</h1>
        </div>
        <!-- <div class="tile bg-amber-500">
          <h1 class="tile-marker">TWO</h1>
        </div>
        <div class="tile bg-yellow-500">
          <h1 class="tile-marker">THREE</h1>
        </div>
        <div class="tile bg-lime-600">
          <h1 class="tile-marker">FOUR</h1>
        </div> -->
    {/each}
    </div>
  </section>

  
</main>

<style>
</style>
