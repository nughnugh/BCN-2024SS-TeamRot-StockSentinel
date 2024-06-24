//normally here we load database values

export function load({params}){
    return {
        title: params.slug
    }
}