
export async function load({params}){
    let title = params.slug
    const response = await fetch("http://localhost:3000/api/StockDataFor/"+ title);
    let data = await response.json()

    let labels = [""];

    return{
        title:params.slug,
    }
}