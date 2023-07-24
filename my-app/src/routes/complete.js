import { grid } from "../store.js";
export async function complete(mutatedPrompts, systemPrompt, dataVariables) {
  const response = await fetch("http://localhost:8000/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      system_message: systemPrompt,
      prompts: mutatedPrompts,
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
      grid.update((grid) => {
        console.log(grid);
        grid[box_idx].completion += text;
        grid = [...grid];
        console.log(grid);
        return grid;
      });
    });
  }
}
