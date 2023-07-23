<script>

    async function test(){
        const response = await fetch('http://localhost:8000/complete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({prompt: 'test'}),
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
            // Decode the value into a string
            let decoded_value = decoder.decode(value, {stream: true});
            streamed_response += decoded_value
        }
    }

    let streamed_response = ""

</script>

<button on:click={test} class="border bg-purple-300 hover:bg-purple-400">
    TEST complete
</button>

<p>{streamed_response}</p>