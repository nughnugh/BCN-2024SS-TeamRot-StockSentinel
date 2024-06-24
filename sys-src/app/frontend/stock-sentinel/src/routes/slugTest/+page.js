//normally here we load database values
const values = [
    {name: 'Slug Test One', text: 'Welcome to Slug One'},
    {name: 'Slug Test Two', text: 'Welcome to Slug Two'},
    {name: 'Slug Test Three', text: 'Welcome to Slug Three'},
]

export function load(){
    return {
        items: values
    }
}