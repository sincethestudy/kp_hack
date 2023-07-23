<script>

    async function test(){
        const response = await fetch('http://localhost:8000/complete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({system_message: 'You are an animal generator', user_message: 'generate an animal that matches this country {0}', inputs: ['canada']}),
        });
        
        if (!response.ok) {
            throw new Error("HTTP error " + response.status);
        }
        
        let reader = response.body.getReader();
        let decoder = new TextDecoder();

        streamed_response = ""

        while(true) {
            let { value, done } = await reader.read();
            if (done) {
                break;
            }
            let decoded_value = decoder.decode(value, {stream: true});
            let lines = decoded_value.split('\n').filter(Boolean);

            lines.forEach(line => {
                let { text, box_idx } = JSON.parse(line);
                arr[box_idx] += text;
                arr = [...arr];
            });
        }
    }

    let streamed_response = ""

    let arr = ["", "", "", ""]

</script>

<button on:click={test} class="border bg-purple-300 hover:bg-purple-400">
    TEST complete
</button>

{#each arr as item}
    <p>{item}</p>
{/each}


