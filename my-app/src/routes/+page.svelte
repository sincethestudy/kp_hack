<script>
  let userPrompt = "";

  $: promptVariables = userPrompt
    .match(/\{(.*?)\}/g)
    ?.map((v) => v.slice(1, -1));
  $: console.log(promptVariables);
  $: dataVariables = [];

  async function sendPrompt() {
    console.log(userPrompt);
    for (let i = 0; i < promptVariables.length; i++) {
      console.log(promptVariables[i], dataVariables[i]);
    }
    await complete();
  }

  async function complete() {
    const response = await fetch("http://localhost:8000/complete", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        system_message: "You are an animal generator",
        user_message: userPrompt,
        inputs: dataVariables,
      }),
    });

    if (!response.ok) {
      throw new Error("HTTP error " + response.status);
    }

    let reader = response.body.getReader();
    let decoder = new TextDecoder();

    streamed_response = "";

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
  let arr = ["", "", "", ""];
</script>

<h1 class="text-2xl font-bold">PromptBreeder</h1>
<main class="flex items-start flex-col px-12 py-8 w-full">
  <section class="w-full">
    <h3>Input Prompt</h3>
    <input
      bind:value={userPrompt}
      placeholder="Insert the prompt here"
      class="input border border-red-500 rounded w-full"
    />
    {promptVariables}
    <h3>Variables</h3>
    <input class="input border border-red-500 rounded" />
    {#if promptVariables}
      {#each promptVariables as v, i}
        <div>Variable {v}</div>
        <input
          bind:value={dataVariables[i]}
          class="input border border-red-500 rounded w-full"
        />
      {/each}
    {/if}
    <button
      on:click={sendPrompt}
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    >
      Generate
    </button>
  </section>
  <section>
    {#each arr as item}
      <p>{item}</p>
    {/each}
  </section>
</main>

<style>
  .input {
    padding: 0.5rem;
    color: dimgrey;
  }
</style>
