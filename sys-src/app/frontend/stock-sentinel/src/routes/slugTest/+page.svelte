<script lang="ts">
    export let data;


</script>

<h1>Welcome to /slugTest! Here we Test the slugs</h1>

{#each data.items as choice}
    <div>
        <p>{choice.text}</p>
        <a href='/slugTest/{choice.name}'>{choice.name}</a>
    </div>
{/each}

{#each stocks as stock}
    <div>
        <p>{stock.name}</p>
    </div>
{/each}

<style>
    h1, p{
        color: blue;
    }
    a{
        color: red;
    }
</style>