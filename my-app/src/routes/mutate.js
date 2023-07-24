export async function mutate(prompt, systemPrompt) {
  const response = await fetch("http://localhost:8000/mutate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt: prompt,
      instructions: systemPrompt,
    }),
  });

  if (!response.ok) {
    throw new Error("HTTP error " + response.status);
  }
  const json = await response.json();
  return json;
}
