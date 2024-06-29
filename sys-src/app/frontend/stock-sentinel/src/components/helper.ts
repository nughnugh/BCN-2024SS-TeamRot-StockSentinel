import thumbsUp from "$lib/assets/thumbsUp.png";
import thumbsDown from "$lib/assets/thumbsDown.png";
import thumbNeutral from "$lib/assets/thumbNeutral.png";

export function chooseThumb(sentiment: string){
    if(Number (sentiment) > 0.1){
        return thumbsUp;
    } else if (Number (sentiment) < 0){
        return thumbsDown;
    } else if(Number (sentiment) <= 0.1){
        return thumbNeutral;
    }
}